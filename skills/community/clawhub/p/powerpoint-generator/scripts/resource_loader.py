#!/usr/bin/env python3
"""Resource Loader -- 资源路由器，按需加载 Markdown 片段和图片清单

三种模式：
- menu: 列出所有可用资源
- resolve: 按字段加载资源
- images: 列出所有可用图片

用法:
  python resource_loader.py menu --field card_type=text --output runtime/card-text.md
  python resource_loader.py resolve --field layout=single_focus --output runtime/layout.md
  python resource_loader.py images --dir OUTPUT_DIR/images/ --output runtime/image-list.md
"""

import argparse
import json
import sys
from pathlib import Path


# -------------------------------------------------------------------
# 内置资源注册表
# -------------------------------------------------------------------
RESOURCES = {
    # 卡片类型
    "card_type=text": {
        "path": "references/card-types/text.md",
        "description": "文本内容卡片",
    },
    "card_type=data": {
        "path": "references/card-types/data.md",
        "description": "数据展示卡片",
    },
    "card_type=list": {
        "path": "references/card-types/list.md",
        "description": "列表卡片",
    },
    "card_type=tag_cloud": {
        "path": "references/card-types/tag_cloud.md",
        "description": "标签云卡片",
    },
    "card_type=process": {
        "path": "references/card-types/process.md",
        "description": "流程卡片",
    },
    "card_type=timeline": {
        "path": "references/card-types/timeline.md",
        "description": "时间线卡片",
    },
    "card_type=comparison": {
        "path": "references/card-types/comparison.md",
        "description": "对比卡片",
    },
    "card_type=quote": {
        "path": "references/card-types/quote.md",
        "description": "引用卡片",
    },
    "card_type=stat_block": {
        "path": "references/card-types/stat_block.md",
        "description": "统计块卡片",
    },
    "card_type=feature_grid": {
        "path": "references/card-types/feature_grid.md",
        "description": "特性网格卡片",
    },
    "card_type=image_text": {
        "path": "references/card-types/image_text.md",
        "description": "图文叠加卡片",
    },
    "card_type=data_highlight": {
        "path": "references/card-types/data_highlight.md",
        "description": "大数据高亮卡片",
    },
    # 布局类型
    "layout=single_focus": {
        "path": "references/layouts/single_focus.md",
        "description": "单一焦点布局",
    },
    "layout=50_50_symmetric": {
        "path": "references/layouts/50_50_symmetric.md",
        "description": "50/50 对称布局",
    },
    "layout=asymmetric_two_col": {
        "path": "references/layouts/asymmetric_two_col.md",
        "description": "非对称两栏布局",
    },
    "layout=three_col_equal": {
        "path": "references/layouts/three_col_equal.md",
        "description": "三栏等宽布局",
    },
    "layout=primary_secondary": {
        "path": "references/layouts/primary_secondary.md",
        "description": "主次结合布局",
    },
    "layout=hero_with_subs": {
        "path": "references/layouts/hero_with_subs.md",
        "description": "英雄式+子项布局",
    },
    "layout=mixed_grid": {
        "path": "references/layouts/mixed_grid.md",
        "description": "混合网格布局",
    },
}


def resolve_resource(field: str, base_dir: Path = Path(".")) -> tuple[str, bool]:
    """按字段加载资源内容。"""
    # 标准化字段
    field_normalized = field.lower().strip()

    # 直接匹配
    if field_normalized in RESOURCES:
        res = RESOURCES[field_normalized]
        res_path = base_dir / res["path"]
        if res_path.exists():
            content = res_path.read_text(encoding="utf-8")
            return content, True
        # 资源路径不存在时返回描述
        return f"[Resource: {res['description']}]", False

    # 模糊匹配
    for key, res in RESOURCES.items():
        _, value = key.split("=")
        if value in field_normalized or field_normalized in value:
            res_path = base_dir / res["path"]
            if res_path.exists():
                content = res_path.read_text(encoding="utf-8")
                return content, True
            return f"[Resource: {res['description']}]", False

    return f"[Unknown resource: {field}]", False


def list_menu() -> str:
    """列出所有可用资源（按分类）。"""
    lines = ["# Resource Menu\n"]
    current_category = None

    for key, res in sorted(RESOURCES.items()):
        category, _ = key.split("=")
        if category != current_category:
            current_category = category
            lines.append(f"\n## {category.replace('_', ' ').title()}\n")
        lines.append(f"- `{key}` -- {res['description']}")

    return "\n".join(lines)


def list_images(image_dir: Path) -> str:
    """列出目录下所有图片。"""
    if not image_dir.exists():
        return f"[Image directory not found: {image_dir}]"

    images = sorted(image_dir.glob("*"))
    if not images:
        return f"[No images found in {image_dir}]"

    lines = [f"# Image List: {image_dir}\n"]
    for img in images:
        if img.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            lines.append(f"- {img.name} ({img.stat().st_size // 1024}KB)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Resource Loader -- Dynamic Resource Router")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # menu 子命令
    menu_parser = subparsers.add_parser("menu", help="List all available resources")

    # resolve 子命令
    resolve_parser = subparsers.add_parser("resolve", help="Resolve resource by field")
    resolve_parser.add_argument("--field", "-f", required=True, help="Resource field (e.g. card_type=text)")
    resolve_parser.add_argument("--output", "-o", type=Path, help="Output file")
    resolve_parser.add_argument("--base-dir", "-b", type=Path, default=Path("."),
                              help="Base directory for resources")

    # images 子命令
    images_parser = subparsers.add_parser("images", help="List all images in directory")
    images_parser.add_argument("--dir", "-d", type=Path, required=True, help="Image directory")
    images_parser.add_argument("--output", "-o", type=Path, help="Output file")

    args = parser.parse_args()

    if args.command == "menu":
        output = list_menu()
        print(output)

    elif args.command == "resolve":
        content, found = resolve_resource(args.field, args.base_dir)
        output = f"<!-- {args.field} -->\n{content}"
        if not found:
            print(f"WARNING: Resource not found: {args.field}", file=sys.stderr)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
            print(f"Resolved: {args.output}")
        else:
            print(output)

    elif args.command == "images":
        output = list_images(args.dir)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
            print(f"Image list: {args.output}")
        else:
            print(output)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
