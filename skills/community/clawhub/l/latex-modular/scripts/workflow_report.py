r"""
workflow_report.py — 结构化报告生成器

根据流程线类型和完成状态，输出 Markdown 表格报告。
所有大流程和独立模式完成后由钩子调用。
"""

import json
import os
from pathlib import Path


def _read_state(workflow_id: str) -> dict:
    """读取流程状态"""
    state_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "scripts", ".workflow")
    path = os.path.join(state_dir, f"{workflow_id}.json")
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate(workflow_id: str, extra: dict = None) -> str:
    """根据流程线和额外信息生成结构化报告"""
    state = _read_state(workflow_id)
    extra = extra or {}
    params = state.get("params", {})
    step_status = state.get("steps", {})
    all_done = state.get("all_completed", False)

    wf_labels = {
        "line1": "新建文档", "line2": "改造",
        "line3": "增量编辑", "line4": "组件复用",
        "standalone": "独立模式",
    }
    label = wf_labels.get(workflow_id, workflow_id)

    # ── 分步状态条 ──────────────────────────────────
    status_parts = []
    for s in ["✓" if step_status.get(n) == "completed" else "·" for n in
              (state.get("step_order") or step_status.keys())]:
        status_parts.append(s)
    progress = " ".join(status_parts)

    # ── 基本信息 ────────────────────────────────────
    lines = []
    lines.append(f"## latex-modular 执行报告 — {label}")
    lines.append("")
    lines.append(f"| 项目 | 内容 |")
    lines.append(f"|------|------|")

    # 流程基本信息
    if workflow_id.startswith("line"):
        lines.append(f"| 流程线 | {label} |")
    else:
        lines.append(f"| 模式 | {label} |")
    lines.append(f"| 进度 | {progress} |")
    lines.append(f"| 状态 | {'✅ 全部完成' if all_done else '🔄 部分完成'} |")

    # 引擎
    engine = extra.get("engine") or params.get("engine", "lualatex")
    lines.append(f"| 适用引擎 | {engine} |")

    # ── 按流程线分类的报告 ──────────────────────────

    # Line 1: 新建文档
    if workflow_id == "line1":
        lines.append(f"| 模板 | {extra.get('template') or params.get('template', '—')} |")
        lines.append(f"| 标题 | {extra.get('title') or params.get('title', '—')} |")
        lines.append(f"| 作者 | {extra.get('author') or params.get('author', '—')} |")
        if extra.get("output"):
            lines.append(f"| 输出路径 | `{extra['output']}` |")
        if extra.get("validation"):
            lines.append(f"| 编译结果 | {extra['validation']} |")

    # Line 2: 改造
    elif workflow_id == "line2":
        lines.append(f"| 源文件 | `{extra.get('source') or params.get('source', '—')}` |")
        lines.append(f"| 备份 | `{extra.get('source', '')}.bak` ✅ |")
        lines.append(f"| 转换结果 | `{extra.get('converted', '—')}` |")
        branch = extra.get("branch") or params.get("branch", "")
        if branch == "output":
            lines.append(f"| 分支 | 直接输出（不入库） |")
            lines.append(f"| 输出路径 | `{extra.get('output', '—')}` |")
        elif branch == "library":
            lines.append(f"| 分支 | 拆入组件库 |")
            lines.append(f"| 组件目录 | `scripts/components/` |")
        elif branch == "both":
            lines.append(f"| 分支 | 入库 + 输出 |")
            lines.append(f"| 输出路径 | `{extra.get('output', '—')}` |")
            lines.append(f"| 组件目录 | `scripts/components/` |")
        if extra.get("validation"):
            lines.append(f"| 编译结果 | {extra['validation']} |")

    # Line 3: 增量编辑
    elif workflow_id == "line3":
        lines.append(f"| 目标文件 | `{extra.get('source') or params.get('source', '—')}` |")
        lines.append(f"| 备份 | `{extra.get('source', '')}.bak` ✅ |")
        lines.append(f"| 注入组件 | {extra.get('component') or params.get('component', '—')} |")
        lines.append(f"| 插入位置 | {extra.get('position') or params.get('position', '—')} |")
        lines.append(f"| 引擎 | {params.get('engine', 'auto')} |")
        if extra.get("validation"):
            lines.append(f"| 编译结果 | {extra['validation']} |")

    # Line 4: 组件复用
    elif workflow_id == "line4":
        mode = extra.get("mode") or params.get("mode", "extract")
        lines.append(f"| 模式 | {mode} |")
        if extra.get("source"):
            lines.append(f"| 源文件 | `{extra['source']}` |")
        if extra.get("components_extracted"):
            lines.append(f"| 提取组件 | {extra['components_extracted']} |")
        if extra.get("output"):
            lines.append(f"| 生成文件 | `{extra['output']}` |")
        if extra.get("template_saved"):
            lines.append(f"| 保存模板 | {extra['template_saved']} |")
        if extra.get("validation"):
            lines.append(f"| 编译结果 | {extra['validation']} |")

    # Standalone + 通用
    else:
        if extra.get("source"):
            lines.append(f"| 文件 | `{extra['source']}` |")
        if extra.get("output"):
            lines.append(f"| 输出 | `{extra['output']}` |")
        if extra.get("operation"):
            lines.append(f"| 操作 | {extra['operation']} |")
        if extra.get("validation"):
            lines.append(f"| 编译结果 | {extra['validation']} |")

    # ── 通用补充信息 ──────────────────────────────────
    if extra.get("warnings"):
        lines.append("")
        lines.append("### ⚠ 警告")
        for w in extra["warnings"]:
            lines.append(f"- {w}")

    if extra.get("notes"):
        lines.append("")
        lines.append("### 📝 说明")
        for n in extra["notes"]:
            lines.append(f"- {n}")

    lines.append("")
    lines.append("---")
    lines.append(f"*报告由 latex-modular workflow_report.py 自动生成*")
    lines.append("")

    return "\n".join(lines)


def print_report(workflow_id: str, extra: dict = None):
    """生成并打印报告"""
    report = generate(workflow_id, extra)
    print(report)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="生成结构化执行报告")
    parser.add_argument("--workflow", "-w", required=True, help="流程线 ID")
    parser.add_argument("--json", default="", help="额外信息的 JSON 字符串")
    args = parser.parse_args()

    extra = json.loads(args.json) if args.json else {}
    print_report(args.workflow, extra)


if __name__ == "__main__":
    main()
