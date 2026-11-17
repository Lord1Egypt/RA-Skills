#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kb-dashboard · 看板渲染脚本

读取 agent 用 ima-mcp 拉取并整理好的结构 JSON，套用 assets/template.html
注入数据，输出一份自包含、可双击打开的 HTML 看板。

用法:
  python3 build_dashboard.py --data <结构.json> [--out <输出.html>] [--template <模板.html>]
  python3 build_dashboard.py --demo   [--out <输出.html>]     # 无 ima-mcp 也可端到端演示

输入 JSON 结构 (DATA):
{
  "generated_at": "2026-09-02 15:36",          # 快照时间字符串
  "scope": "main|company|material|all",          # 范围
  "libraries": [                                 # 一个或多个库
    {
      "id": "<你的主库ID>",
      "name": "<你的知识库名称>",
      "note": "可选·诚实边界说明",
      "kpis": {"topFolders":9,"totalDocs":172,"methodCards":101,"metaLayer":15,"emptyAreas":3,"express":"薄"},
      "tree": [                                  # 结构树(根的子节点列表)
        {"name":"元层","count":15,"items":["..."]},
        {"name":"方法论中枢","count":101,"children":[{"name":"定位/品类","count":15},...]},
        {"name":"哲学","count":0,"empty":true}
      ],
      "topCounts": [["元层",15],["方法论中枢",101],...],     # 各顶层夹文档数(柱状图)
      "methodStage": [["定位/品类",15],...],                # 方法卡四环节(饼图,可空)
      "graph": {"nodes":[{"name":"...","count":N,"cat":0,"color":"#hex"}],"links":[{"source":0,"target":1}]}
    }
  ]
}
"""
import argparse
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")
ECHARTS_PATH = os.path.join(HERE, "..", "assets", "echarts.min.js")

DEMO_DATA = {
    "generated_at": "demo",
    "scope": "main",
    "note": "演示数据（--demo 生成），用于离线预览看板效果",
    "libraries": [{
        "id": "demo_kb",
        "name": "演示知识库",
        "kpis": {"topFolders": 5, "totalDocs": 86, "methodCards": 42, "metaLayer": 8, "emptyAreas": 2, "express": "薄"},
        "tree": [
            {"name": "元层", "count": 8, "items": ["示例卡A", "示例卡B", "示例卡C"]},
            {"name": "方法论中枢", "count": 42, "children": [
                {"name": "定位/品类", "count": 12}, {"name": "策略/品牌战略", "count": 15},
                {"name": "识别设计", "count": 8}, {"name": "营销传播", "count": 7}]},
            {"name": "项目实战", "count": 6, "items": ["实战项目示例"]},
            {"name": "案例库", "count": 30, "children": [{"name": "餐饮", "count": 18}, {"name": "快消", "count": 12}]},
            {"name": "待建区", "count": 0, "empty": True}
        ],
        "topCounts": [["元层", 8], ["方法论中枢", 42], ["项目实战", 6], ["案例库", 30], ["待建区", 0]],
        "methodStage": [["定位/品类", 12], ["策略/品牌战略", 15], ["识别设计", 8], ["营销传播", 7]],
        "graph": {
            "nodes": [
                {"name": "演示知识库", "count": 86, "cat": 0},
                {"name": "元层", "count": 8, "cat": 1},
                {"name": "方法论中枢", "count": 42, "cat": 1},
                {"name": "项目实战", "count": 6, "cat": 1},
                {"name": "案例库", "count": 30, "cat": 1},
                {"name": "定位/品类", "count": 12, "cat": 2},
                {"name": "策略/品牌战略", "count": 15, "cat": 2},
                {"name": "餐饮", "count": 18, "cat": 2}
            ],
            "links": [{"source": 0, "target": 1}, {"source": 0, "target": 2}, {"source": 0, "target": 3},
                      {"source": 0, "target": 4}, {"source": 2, "target": 5}, {"source": 2, "target": 6},
                      {"source": 4, "target": 7}]
        }
    }]
}


def load_echarts_inline():
    """读取包内 echarts.min.js，返回内联脚本内容。缺失时返回 None（v1.1.1 起不再回退在线 CDN，由调用方报错退出）。"""
    if os.path.exists(ECHARTS_PATH):
        with open(ECHARTS_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return None


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("顶层必须是 JSON 对象")
    libs = data.get("libraries")
    if not isinstance(libs, list) or not libs:
        raise ValueError("必须包含非空的 libraries 数组")
    for i, lib in enumerate(libs):
        for key in ("id", "name", "kpis"):
            if key not in lib:
                raise ValueError("libraries[%d] 缺少必填字段: %s" % (i, key))
        k = lib["kpis"]
        for key in ("topFolders", "totalDocs", "methodCards", "metaLayer", "emptyAreas"):
            if key not in k:
                # 补默认，避免渲染崩
                k[key] = 0
        if "express" not in k:
            k["express"] = "—"
    if "generated_at" not in data:
        data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    if "scope" not in data:
        data["scope"] = "single"
    return data


def render(data, template_path, out_path):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    placeholder = "/*DATA_PLACEHOLDER*/"
    if placeholder not in tpl:
        raise ValueError("模板中未找到 %s 注入点" % placeholder)
    # 用紧凑但可读的中文 JSON 注入；ensure_ascii=False 保留中文
    injected = json.dumps(data, ensure_ascii=False, indent=2)
    html = tpl.replace(placeholder, injected)
    # 内嵌 ECharts：产物完全离线自包含（v1.1.1 起不再回退在线 CDN，杜绝任何远程脚本加载）
    echarts_js = load_echarts_inline()
    if echarts_js and "/*ECHARTS_INLINE*/" in html:
        html = html.replace("/*ECHARTS_INLINE*/", echarts_js)
    elif not echarts_js:
        print("[错误] 包内 assets/echarts.min.js 缺失，无法生成离线自包含看板。", file=sys.stderr)
        print("       本 skill 不回退在线 CDN。请从官方发布包恢复 assets/echarts.min.js（Apache-2.0）后重跑。", file=sys.stderr)
        sys.exit(1)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="生成 ima 知识库看板 HTML（无参数运行打印引导；--demo 零依赖端到端体验）")
    ap.add_argument("--data", default=None, help="结构 JSON 路径（与 --demo 二选一）")
    ap.add_argument("--demo", action="store_true", help="使用内置演示数据端到端生成（无需 ima-mcp）")
    ap.add_argument("--selftest", action="store_true", help="零依赖自检：包完整性+数据校验器+demo端到端（无 ima-mcp 环境先跑这条）")
    ap.add_argument("--out", default=None, help="输出 HTML 路径(默认 ./kb_dashboard_YYYY-MM-DD.html)")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE, help="模板 HTML 路径")
    args = ap.parse_args()

    if args.selftest:
        ok = True
        for f in (DEFAULT_TEMPLATE, ECHARTS_PATH):
            if os.path.exists(f):
                print("[自检] 资源存在: %s (%d KB)" % (os.path.basename(f), os.path.getsize(f)//1024))
            else:
                print("[自检][失败] 缺失: %s" % f); ok = False
        import copy as _copy
        try:
            validate(_copy.deepcopy(DEMO_DATA))
            print("[自检] 数据校验器(内置演示数据): 通过")
        except Exception as e:
            print("[自检][失败] 演示数据未过校验: %s" % e); ok = False
        import tempfile, subprocess
        with tempfile.TemporaryDirectory() as td:
            tmp_out = os.path.join(td, "selftest.html")
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--demo", "--out", tmp_out],
                               capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(tmp_out) and os.path.getsize(tmp_out) > 100_000:
                h = open(tmp_out, encoding="utf-8").read()
                if "echarts" in h and "{{" not in h:
                    print("[自检] demo 端到端: 通过 (%d KB, echarts 内嵌, 无占位符残留)" % (os.path.getsize(tmp_out)//1024))
                else:
                    print("[自检][失败] demo 产物异常(缺 echarts 或有占位符残留)"); ok = False
            else:
                print("[自检][失败] demo 运行失败: %s" % (r.stderr or "")[:200]); ok = False
        print("[自检] 结论: %s" % ("全部通过，本 skill 在无 ima-mcp 环境下可正常运行" if ok else "存在失败项，请检查包完整性"))
        return

    if args.demo:
        import copy
        data = copy.deepcopy(DEMO_DATA)
        data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    elif args.data:
        try:
            data = validate(load_json(args.data))
        except Exception as e:
            print("❌ 数据校验失败: %s" % e, file=sys.stderr)
            sys.exit(1)
    else:
        # 无参数：友好引导而非报错退出（沙箱/首次运行先看这里）
        print("两种运行方式：")
        print("  1) 零依赖体验（无需 ima-mcp/数据）：python3 build_dashboard.py --demo")
        print("     → 用内置演示数据端到端生成一份示例看板 HTML")
        print("  2) 正式生成：先从 ima 导出库结构 JSON，再执行")
        print("     python3 build_dashboard.py --data 结构.json [--out 看板.html]")
        print("数据格式与进阶用法见 SKILL.md。")
        return

    if args.out is None:
        args.out = "kb_dashboard_%s.html" % datetime.now().strftime("%Y-%m-%d")

    try:
        out = render(data, args.template, args.out)
    except Exception as e:
        print("❌ 渲染失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(out) / 1024.0
    print("✅ 看板已生成: %s (%.1f KB, %d 个库)" % (out, size, len(data["libraries"])))


if __name__ == "__main__":
    main()
