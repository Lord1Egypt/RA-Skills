r"""
workflow_router.py — 语义路由 + 路由验证钩子

三层结构：
  1. 路由分析 — 根据用户输入匹配流程线或独立模式
  2. 验证钩子 — 检查路由结果是否与输入语义一致，不一致则降级/报警
  3. 文件大小钩子 — 检测大文件，强制分块处理

输出模式:
  - workflow: 四流程线之一，走严格步骤守卫，不可跳过
  - standalone: 独立模式，AI 自行决断，无守卫

用法:
  python scripts/workflow_router.py "用 article 模板生成论文" --verify
  python scripts/workflow_router.py "帮我把这篇旧文章转成 lualatex" --check-size
  python scripts/workflow_router.py "加个表格到现有文档" --json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ── 文件大小阈值 ──────────────────────────────────────────
LARGE_FILE_THRESHOLD = 500 * 1024  # 500KB
HUGE_FILE_THRESHOLD = 2 * 1024 * 1024  # 2MB


# ── 路由规则 ──────────────────────────────────────────────
# (匹配模式, 路由结果, 标签, 参数提取函数, 期望语义方向)
TRIGGER_RULES = [
    # ═══ Line 1: 新建文档 ═══
    (r"生成.*文档|新建.*文章|写一篇|创建.*tex|用.*模板|template|从零",
     "line1", "新建文档",
     lambda t: {
         "template": _extract(t, r"(?:用|使用|基于|以)\s*(\w+)", "article"),
         "author": _extract(t, r"作者[是为：:]?\s*(\S+)", ""),
         "title": _extract(t, r"(?:标题|题目|名为?)[是为：:]?\s*([^，,\s]+)", "文档"),
         "engine": "lualatex",
     },
     "期望用户从头开始生成一篇新文档"),

    # ═══ Line 2: 改造 ═══
    (r"转[换化]|convert|改造|迁移|pdf[lL]aTeX.*[转换]|老.*文章|旧.*文档|lualatex.*用|换成",
     "line2", "改造",
     lambda t: {
         "source": _extract_path(t),
         "branch": _detect_branch(t),
         "engine": "lualatex",
     },
     "期望处理一篇现有文章，可能需要引擎转换"),

    # ═══ Line 3: 增量编辑 ═══
    (r"插[入加增]|追加|添加|增加|inject|加(表格|图片|图|环境|命令)|写到一半|现有.*加|增量|塞进|补[充上]",
     "line3", "增量编辑",
     lambda t: {
         "source": _extract_path(t),
         "component": _extract_component(t),
         "position": _extract_position(t),
     },
     "期望向已有 .tex 文件中插入内容，不破坏原文"),

    # ═══ Line 4: 组件复用 ═══
    (r"拆[分解]|提取|入库|extract|refactor|组件|复用|manifest|拆出来|存起来",
     "line4", "组件复用",
     lambda t: {
         "source": _extract_path(t),
         "mode": "extract" if _contains_any(t, ["拆", "提取", "extract"]) else "refactor",
     },
     "期望拆解或组织 LaTeX 组件，为复用做准备"),

    # ═══ 独立模式 ═══
    (r"编译|验证|validate|检查.*编译|跑.*tex|单独|就这一个|只是|独立|单个",
     "standalone", "独立模式",
     lambda t: {"source": _extract_path(t)},
     "独立的操作，不需要流程线约束"),
]


# ── 工具函数 ──────────────────────────────────────────────

def _contains_any(text: str, keywords: list) -> bool:
    return any(k in text for k in keywords)


def _extract(text: str, pattern: str, default: str = "") -> str:
    m = re.search(pattern, text)
    return m.group(1) if m else default


def _extract_path(text: str) -> str:
    m = re.search(r"['\"]([^'\"]+\.tex)['\"]", text)
    if m:
        return m.group(1)
    m = re.search(r"(\S+\.tex)", text)
    if m:
        return m.group(1)
    return ""


def _extract_component(text: str) -> str:
    comp_map = {
        "表格": "table-style", "表": "table-style",
        "图片": "figure-insert", "图": "figure-insert",
        "环境": "mylist", "命令": "title-commands",
        "样式": "section-style", "页眉": "header-footer", "页脚": "header-footer",
    }
    for kw, comp in comp_map.items():
        if kw in text:
            return comp
    return "table-style"


def _extract_position(text: str) -> str:
    m = re.search(r"(?:在|于)\s*['\"]([^'\"]+)['\"](?:\s*之?[后前])", text)
    pattern = m.group(1) if m else ""
    if "开始" in text or "begin" in text.lower():
        return "at-begin-document"
    if "结束" in text or "end{document}" in text:
        return "at-end-document"
    if pattern:
        return pattern
    return "at-end-document"


def _detect_branch(text: str) -> str:
    if _contains_any(text, ["入库", "拆", "组件", "extract"]):
        if _contains_any(text, ["同时", "也要", "并且", "and"]):
            return "both"
        return "library"
    return "output"


# ── 语义验证钩子 ──────────────────────────────────────────

def verify(route_result: dict, original_input: str) -> dict:
    """验证路由结果与输入语义是否一致
    
    Returns:
        {verified, conflicts, adjusted_workflow, reason}
    """
    wf = route_result["workflow"]
    label = route_result["label"]
    confidence = route_result["confidence"]

    # 一致性检查清单
    issues = []

    # 检查1: line1 (新建) 不应该有源文件路径
    if wf == "line1" and _extract_path(original_input):
        issues.append("输入包含 .tex 文件路径但匹配了「新建文档」，可能应为改造或增量")

    # 检查2: line2 (改造) 应该指定源文件
    if wf == "line2" and not _extract_path(original_input):
        issues.append("输入匹配了「改造」但未指定源文件，将需要补充文件路径")

    # 检查3: line3 (增量) 应该有插入意图
    if wf == "line3" and not _contains_any(original_input, ["插", "加", "添", "补", "塞", "inject"]):
        issues.append("输入匹配了「增量编辑」但缺乏明确的插入意图词")

    # 检查4: line4 (组件复用) 应该指向已有内容
    if wf == "line4" and not _contains_any(original_input, ["拆", "提取", "extract", "组件"]):
        issues.append("输入匹配了「组件复用」但缺乏拆解/提取关键词")

    # 处理结果
    result = {
        "verified": len(issues) == 0,
        "workflow": wf,
        "confidence": confidence,
        "issues": issues,
    }

    if issues and confidence != "high":
        # 低置信度且有冲突 → 降级为独立模式
        result["workflow"] = "standalone"
        result["adjusted"] = True
        result["reason"] = f"低置信度({confidence})且有语义冲突，降级为独立模式"
        result["original_workflow"] = wf

    return result


# ── 文件大小钩子 ──────────────────────────────────────────

def check_file_size(file_path: str) -> dict:
    """检查文件大小，返回处理建议"""
    if not file_path or not os.path.isfile(file_path):
        return {"status": "no_file", "size": 0, "suggestion": ""}

    size = os.path.getsize(file_path)
    status = "normal"
    suggestion = ""
    lines_hint = ""

    if size > HUGE_FILE_THRESHOLD:
        status = "huge"
        suggestion = "⚠ 文件过大(>{:.1f}MB)，必须使用 --lines 限定行范围".format(
            size / 1024 / 1024)
        lines_hint = "建议: --lines 1-500 分块处理"
    elif size > LARGE_FILE_THRESHOLD:
        status = "large"
        suggestion = "⚡ 文件较大({:.0f}KB)，建议使用 --lines 限定行范围".format(
            size / 1024)
        lines_hint = "建议: --lines 1-500 或根据需求调整"

    return {
        "status": status,
        "size": size,
        "size_readable": _format_size(size),
        "suggestion": suggestion,
        "lines_hint": lines_hint,
    }


def _format_size(size: int) -> str:
    if size > 1024 * 1024:
        return f"{size / 1024 / 1024:.1f}MB"
    if size > 1024:
        return f"{size / 1024:.0f}KB"
    return f"{size}B"


# ── 主路由 ────────────────────────────────────────────────

def route(text: str) -> dict:
    """路由主函数"""
    result = {
        "workflow": "",
        "mode": "",
        "label": "",
        "params": {},
        "confidence": "low",
        "steps": [],
    }

    for pattern, workflow, label, param_fn, _ in TRIGGER_RULES:
        if re.search(pattern, text, re.IGNORECASE):
            result["workflow"] = workflow
            result["label"] = label
            result["params"] = param_fn(text)
            result["confidence"] = "high"
            break

    # 未匹配 → 兜底
    if not result["workflow"]:
        path = _extract_path(text)
        if path:
            result["workflow"] = "standalone"
            result["label"] = "独立模式（路径匹配兜底）"
            result["params"] = {"source": path}
            result["confidence"] = "low"
        else:
            result["workflow"] = "standalone"
            result["label"] = "独立模式（通用兜底）"
            result["params"] = {}
            result["confidence"] = "low"

    # 确定 mode
    result["mode"] = "workflow" if result["workflow"].startswith("line") else "standalone"

    # 步骤链
    result["steps"] = WORKFLOW_STEPS.get(result["workflow"], [
        {"step": 1, "name": "standalone", "desc": "独立操作，无步骤约束"}
    ])

    return result


WORKFLOW_STEPS = {
    "line1": [
        {"step": 1, "name": "template", "desc": "选择/配置模板"},
        {"step": 2, "name": "inject_params", "desc": "注入标题/作者等参数"},
        {"step": 3, "name": "compose", "desc": "组合生成 .tex"},
        {"step": 4, "name": "validate", "desc": "编译验证"},
    ],
    "line2": [
        {"step": 1, "name": "convert", "desc": "pdfLaTeX → LuaLaTeX"},
        {"step": 2, "name": "branch", "desc": "入库/输出/两者都要"},
    ],
    "line3": [
        {"step": 1, "name": "inject", "desc": "注入组件"},
        {"step": 2, "name": "validate", "desc": "编译验证"},
    ],
    "line4": [
        {"step": 1, "name": "extract", "desc": "拆解组件"},
        {"step": 2, "name": "compose", "desc": "组合使用"},
        {"step": 3, "name": "template", "desc": "保存为模板"},
        {"step": 4, "name": "reuse", "desc": "--template 复用"},
    ],
    "standalone": [
        {"step": 1, "name": "standalone", "desc": "独立操作，无步骤约束"},
    ],
}


# ── CLI ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="语义路由 + 路由验证钩子 + 文件大小钩子")
    parser.add_argument("input", nargs="?", default="", help="用户输入文本")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--verify", action="store_true",
                        help="启用语义验证钩子，检查路由与输入的语义一致性")
    parser.add_argument("--check-size", default="",
                        help="启用文件大小钩子，检查指定文件的体积")
    parser.add_argument("--list-rules", action="store_true", help="列出所有匹配规则")

    args = parser.parse_args()

    if args.list_rules:
        print("路由规则:")
        print(f"  {'路由':<12s} {'匹配模式'}")
        print(f"  {'-'*55}")
        for pattern, wf, label, _, desc in TRIGGER_RULES:
            print(f"  {wf:<12s} {pattern[:42]:<44s} {label}")
        return

    if not args.input and not args.check_size:
        parser.print_help()
        sys.exit(1)

    # ── 文件大小钩子 ──────────────────────────────────
    if args.check_size:
        r = check_file_size(args.check_size)
        print(f"[size] 文件: {args.check_size}")
        print(f"[size] 大小: {r['size_readable']} ({r['size']} bytes)")
        print(f"[size] 状态: {r['status']}")
        if r['suggestion']:
            print(f"[size] {r['suggestion']}")
        if r['lines_hint']:
            print(f"[size] {r['lines_hint']}")
        if r['status'] == 'huge':
            print(f"[size] ⛔ 强制要求使用 --lines 参数。不加将拒绝执行。")
        return

    # ── 路由分析 + 验证钩子 ────────────────────────────
    route_result = route(args.input)
    output = dict(route_result)  # 浅拷贝

    if args.verify:
        v = verify(route_result, args.input)
        output["verify"] = v

        # 如果验证降级
        if v.get("adjusted"):
            output["workflow"] = v["workflow"]
            output["mode"] = "standalone"

    output["original_input"] = args.input

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print("=" * 55)
        print("  语义路由结果")
        print("=" * 55)
        print(f"  输入: {args.input[:60]}{'...' if len(args.input) > 60 else ''}")
        print(f"  路由: {output['workflow']} ({output['label']})")
        print(f"  模式: {'📋 流程线（严格步骤守卫）' if output['mode'] == 'workflow' else '🔧 独立模式（AI 自主）'}")
        print(f"  置信度: {output['confidence']}")

        if output["params"]:
            print(f"  参数: {json.dumps(output['params'], ensure_ascii=False)}")

        if args.verify:
            v = output.get("verify", {})
            if not v.get("verified", True):
                print(f"\n  ⚠ 语义验证发现 {len(v.get('issues', []))} 个冲突:")
                for issue in v["issues"]:
                    print(f"    - {issue}")
                if v.get("adjusted"):
                    print(f"  → 已降级为独立模式: {v.get('reason', '')}")

        if output["steps"]:
            mode_label = "步骤序列" if output["mode"] == "workflow" else "操作"
            print(f"\n  {mode_label}:")
            for s in output["steps"]:
                print(f"    {s['step']}. {s['name']} — {s['desc']}")

        # 文件大小提示（如果 params 中有 source）
        source = output.get("params", {}).get("source", "")
        if source:
            fr = check_file_size(source)
            if fr["status"] != "normal" and fr["status"] != "no_file":
                print(f"\n  [size] {fr['suggestion']}")
                if fr["lines_hint"]:
                    print(f"  [size] {fr['lines_hint']}")

        print("=" * 55)


if __name__ == "__main__":
    main()
