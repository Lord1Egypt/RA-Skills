#!/usr/bin/env python3
"""CLI: 模板填充模式"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kai_docx_generator.engine.template_filler import TemplateFiller


def main():
    parser = argparse.ArgumentParser(
        description="用数据填充 .docx 模板中的占位符"
    )
    parser.add_argument("template", help="模板 .docx 文件路径")
    parser.add_argument(
        "--data", required=True,
        help="数据 JSON 文件或 YAML Front Matter 文件路径"
    )
    parser.add_argument("--output", required=True, help="输出 .docx 文件路径")
    parser.add_argument(
        "--strict", action="store_true",
        help="存在未替换占位符时返回非零退出码"
    )

    args = parser.parse_args()

    # Check template exists
    if not os.path.exists(args.template):
        print(f"错误: 模板文件不存在: {args.template}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Load data
    data_path = args.data
    if not os.path.exists(data_path):
        print(f"错误: 数据文件不存在: {data_path}", file=sys.stderr)
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Try JSON first
    if content.startswith("{"):
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"错误: JSON 解析失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Try YAML
        try:
            import yaml
            # Extract YAML front matter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 2:
                    data = yaml.safe_load(parts[1]) or {}
                else:
                    print("错误: YAML Front Matter 格式无效", file=sys.stderr)
                    sys.exit(1)
            else:
                data = yaml.safe_load(content) or {}
        except ImportError:
            print("错误: 需要安装 pyyaml 或使用 JSON 格式的数据文件", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"错误: YAML 解析失败: {e}", file=sys.stderr)
            sys.exit(1)

    filler = TemplateFiller(args.template)
    stats = filler.fill(data)
    filler.save(args.output)

    # Report
    print(f"已生成: {args.output}")
    print(f"  替换: {len(stats['replaced'])} 个占位符")
    if stats["unreplaced"]:
        print(f"  未替换: {', '.join(stats['unreplaced'])}")
    if stats["extra"]:
        print(f"  多余字段: {', '.join(stats['extra'])}")

    if args.strict and stats["unreplaced"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
