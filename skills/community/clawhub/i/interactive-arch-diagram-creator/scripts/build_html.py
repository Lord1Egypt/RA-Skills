"""
build_html.py
────────────────────────────────────────────────────────────────
将 mindmap 字符串和 flowchart 字典填充到 HTML 模板，生成独立静态网页。

用法：
  python build_html.py \\
    --repo-name   "my-project" \\
    --mindmap     mindmap.txt \\
    --flowchart   flowchart.json \\
    --edges       edges.json \\
    --meta        meta.json \\
    --template    /path/to/arch_diagram_static.html \\
    --output      /path/to/output/

参数说明：
  --repo-name   仓库名称（显示在页面标题）
  --mindmap     包含 PlantUML mindmap 字符串的文本文件
  --flowchart   包含 {nodeKey: mermaidCode} 字典的 JSON 文件（可选，不传则空对象）
  --edges       包含节点间关系的 JSON 文件（可选），格式：
                [{"from": "节点名A", "to": "节点名B", "label": "调用"}, ...]
                只允许上层节点指向下层节点（用户侧 → 数据侧方向）
  --meta        包含仓库元信息的 JSON 文件（可选），由 scan_repo.py --stats-output 生成
                格式: {"repo_name": ..., "description": ..., "file_count": ...,
                        "total_loc": ..., "tech_stack": [{"lang": ..., "count": ..., "loc": ...}]}
  --description 仓库简介文本（可选，会覆盖 meta 中的 description 字段）
  --template    HTML 模板文件路径（默认：同目录下 ../assets/arch_diagram_static.html）
  --output      输出目录（默认：./output）

输出：
  <output>/<repo_name_safe>.html

退出码：
  0 = 成功
  1 = 模板或输入文件不存在
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

_THIS_DIR = Path(__file__).parent.resolve()
_DEFAULT_TEMPLATE = _THIS_DIR.parent / "assets" / "arch_diagram_static.html"


def build_html(repo_name: str, mindmap_str: str, flowchart_data: dict,
               edges_data: list, meta: dict, template_path: Path, output_dir: Path) -> Path:
    if not template_path.exists():
        print(f"ERROR: 模板文件不存在: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text(encoding="utf-8")
    template = template.replace("<!--REPO_NAME-->", repo_name)
    template = template.replace(
        "<!--MINDMAP_DATA_JSON-->",
        json.dumps(mindmap_str, ensure_ascii=False)
    )
    template = template.replace(
        "<!--FLOWCHART_DATA_JSON-->",
        json.dumps(flowchart_data, ensure_ascii=False)
    )
    template = template.replace(
        "<!--EDGES_DATA_JSON-->",
        json.dumps(edges_data, ensure_ascii=False)
    )
    template = template.replace(
        "<!--REPO_META_JSON-->",
        json.dumps(meta, ensure_ascii=False)
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", repo_name)
    out_file = output_dir / f"{safe_name}.html"
    out_file.write_text(template, encoding="utf-8")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="填充 HTML 模板，生成静态架构图网页")
    parser.add_argument("--repo-name", required=True, help="仓库名称")
    parser.add_argument("--mindmap", required=True, help="mindmap 文本文件路径")
    parser.add_argument("--flowchart", default="", help="flowchart JSON 文件路径（可选）")
    parser.add_argument("--edges", default="", help="节点关系 JSON 文件路径（可选），格式：[{from, to, label}]")
    parser.add_argument("--meta", default="", help="仓库元信息 JSON 文件路径（可选，由 scan_repo.py --stats-output 生成）")
    parser.add_argument("--description", default="", help="仓库简介文本（可选，覆盖 meta 中的 description）")
    parser.add_argument("--template", default=str(_DEFAULT_TEMPLATE), help="HTML 模板文件路径")
    parser.add_argument("--output", default="./output", help="输出目录")
    args = parser.parse_args()

    mindmap_path = Path(args.mindmap)
    if not mindmap_path.exists():
        print(f"ERROR: mindmap 文件不存在: {args.mindmap}", file=sys.stderr)
        sys.exit(1)
    mindmap_str = mindmap_path.read_text(encoding="utf-8").strip()

    flowchart_data = {}
    if args.flowchart:
        fc_path = Path(args.flowchart)
        if fc_path.exists():
            with open(fc_path, encoding="utf-8") as f:
                flowchart_data = json.load(f)
        else:
            print(f"WARNING: flowchart 文件不存在，使用空对象: {args.flowchart}", file=sys.stderr)

    edges_data = []
    if args.edges:
        edges_path = Path(args.edges)
        if edges_path.exists():
            with open(edges_path, encoding="utf-8") as f:
                edges_data = json.load(f)
        else:
            print(f"WARNING: edges 文件不存在，使用空数组: {args.edges}", file=sys.stderr)

    # 读取 meta 信息
    meta: dict = {}
    if args.meta:
        meta_path = Path(args.meta)
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
        else:
            print(f"WARNING: meta 文件不存在，使用空对象: {args.meta}", file=sys.stderr)

    # 保证 meta 有基础字段
    meta.setdefault("repo_name", args.repo_name)
    meta.setdefault("file_count", 0)
    meta.setdefault("total_loc", 0)
    meta.setdefault("tech_stack", [])

    # --description 覆盖
    if args.description:
        meta["description"] = args.description

    out_file = build_html(
        repo_name=args.repo_name,
        mindmap_str=mindmap_str,
        flowchart_data=flowchart_data,
        edges_data=edges_data,
        meta=meta,
        template_path=Path(args.template),
        output_dir=Path(args.output),
    )

    print(f"SUCCESS: {out_file}")


if __name__ == "__main__":
    main()
