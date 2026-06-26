"""
parse_mindmap.py
────────────────────────────────────────────────────────────────
解析 Claude 生成的 PlantUML mindmap，提取所有包含 files 的节点。
这些节点用于 Stage 3：为每个节点生成 Mermaid 子流程图。

用法：
  python parse_mindmap.py <mindmap_file>
  echo "<mindmap_str>" | python parse_mindmap.py -

输出（stdout）：
  JSON 数组：[{"name": "节点名", "key": "唯一key", "files": ["path/to/file"]}]

退出码：
  0 = 成功（即使节点为空）
  1 = 输入文件不存在
"""

import argparse
import json
import re
import sys


def _merge_multiline_json(mindmap_str: str) -> str:
    """
    将 mindmap 文本中跨行的 JSON 合并回单行。
    模型有时会把 {"name": "x", "files": [\n  "a",\n  "b"\n]} 拆成多行输出。
    """
    result_lines = []
    buf = ""
    depth = 0
    for line in mindmap_str.splitlines():
        if depth == 0:
            open_pos = line.find("{")
            if open_pos == -1:
                result_lines.append(line)
                continue
            buf = line
            depth = buf.count("{") - buf.count("}")
            if depth == 0:
                result_lines.append(buf)
                buf = ""
        else:
            buf += " " + line.strip()
            depth = buf.count("{") - buf.count("}")
            if depth == 0:
                result_lines.append(buf)
                buf = ""
    if buf:
        result_lines.append(buf)
    return "\n".join(result_lines)


def _get_node_key(node_name: str, files: list) -> str:
    clean_files = sorted(re.sub(r"[^a-zA-Z0-9]", "_", f) for f in files)
    return re.sub(r"[^a-zA-Z0-9]", "_", node_name) + "_" + "_".join(clean_files)


def parse_mindmap_nodes(mindmap_str: str) -> list:
    """从 mindmap 文本提取所有包含 files 的节点，返回带 key 的列表。"""
    nodes = []
    for line in _merge_multiline_json(mindmap_str).splitlines():
        line = line.strip()
        if not line or line.startswith("@"):
            continue
        json_start = line.find("{")
        json_end = line.rfind("}")
        if json_start == -1 or json_end == -1:
            continue
        try:
            data = json.loads(line[json_start:json_end + 1])
            if data.get("files"):
                key = _get_node_key(data["name"], data["files"])
                nodes.append({
                    "name": data["name"],
                    "key": key,
                    "files": data["files"],
                })
        except Exception:
            pass
    return nodes


def main():
    parser = argparse.ArgumentParser(description="解析 mindmap，提取节点列表")
    parser.add_argument("input", help="mindmap 文本文件路径，或 '-' 从 stdin 读取")
    args = parser.parse_args()

    if args.input == "-":
        mindmap_str = sys.stdin.read()
    else:
        import os
        if not os.path.exists(args.input):
            print(f"ERROR: 文件不存在: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(args.input, encoding="utf-8") as f:
            mindmap_str = f.read()

    nodes = parse_mindmap_nodes(mindmap_str)
    print(json.dumps(nodes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
