#!/usr/bin/env python3
"""Contract Validator -- 校验各阶段产物的合同完整性

支持的合同类型：
- outline: 大纲合同
- style: 风格定义合同
- search: 资料搜集合同
- delivery-manifest: 交付清单合同

用法:
  python contract_validator.py outline OUTPUT_DIR/outline.txt
  python contract_validator.py style OUTPUT_DIR/style.json
  python contract_validator.py delivery OUTPUT_DIR/
"""

import argparse
import json
import sys
from pathlib import Path


# -------------------------------------------------------------------
# 合同定义
# -------------------------------------------------------------------
CONTRACTS = {
    "outline": {
        "required_keys": ["ppt_outline"],
        "parts_required": True,
        "min_parts": 1,
    },
    "style": {
        "required_keys": ["style_id", "style_name", "background", "card", "text", "accent"],
        "style_ids": [
            "dark_tech", "xiaomi_orange", "blue_white", "royal_red",
            "fresh_green", "luxury_purple", "minimal_gray", "vibrant_rainbow",
            "gradient_blue", "warm_sunset", "nordic_white", "cyber_punk",
            "elegant_gold", "ocean_depth", "retro_film", "corporate_blue"
        ],
    },
    "search": {
        "required_keys": ["queries", "results"],
        "min_results": 3,
    },
    "delivery-manifest": {
        "required_keys": ["slides", "style", "outline", "output_files"],
        "slides_required": True,
    }
}


def validate_outline(data: dict) -> tuple[bool, list]:
    """校验大纲合同。"""
    issues = []
    contract = CONTRACTS["outline"]

    for key in contract["required_keys"]:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    outline = data.get("ppt_outline", {})
    parts = outline.get("parts", [])
    if not isinstance(parts, list) or len(parts) < contract["min_parts"]:
        issues.append(f"Parts must be a list with at least {contract['min_parts']} items")
    else:
        for i, part in enumerate(parts):
            if not isinstance(part, dict):
                issues.append(f"Part {i} must be a dict")
                continue
            if "part_title" not in part:
                issues.append(f"Part {i} missing 'part_title'")
            if "pages" not in part:
                issues.append(f"Part {i} missing 'pages'")
            else:
                pages = part["pages"]
                if not isinstance(pages, list):
                    issues.append(f"Part {i} 'pages' must be a list")
                else:
                    for j, page in enumerate(pages):
                        if not isinstance(page, dict):
                            issues.append(f"Part {i} page {j} must be a dict")
                            continue
                        if "title" not in page:
                            issues.append(f"Part {i} page {j} missing 'title'")

    cover = outline.get("cover", {})
    if cover and not isinstance(cover, dict):
        issues.append("'cover' must be a dict")
    elif cover and "title" not in cover:
        issues.append("Cover missing 'title'")

    return len(issues) == 0, issues


def validate_style(data: dict) -> tuple[bool, list]:
    """校验风格定义合同。"""
    issues = []
    contract = CONTRACTS["style"]

    for key in contract["required_keys"]:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    if "style_id" in data and "style_ids" in contract:
        if data["style_id"] not in contract["style_ids"]:
            issues.append(f"Invalid style_id: {data['style_id']}. Must be one of {contract['style_ids']}")

    # 检查 CSS 变量是否完整
    if "accent" in data:
        if not isinstance(data["accent"], dict):
            issues.append("accent must be a dict with primary/secondary arrays")
        else:
            if "primary" not in data["accent"]:
                issues.append("accent missing 'primary' color array")
            if "secondary" not in data["accent"]:
                issues.append("accent missing 'secondary' color array")

    return len(issues) == 0, issues


def validate_search(data: dict) -> tuple[bool, list]:
    """校验资料搜集合同。"""
    issues = []
    contract = CONTRACTS["search"]

    for key in contract["required_keys"]:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    if "results" in data and isinstance(data["results"], list):
        if len(data["results"]) < contract["min_results"]:
            issues.append(f"Need at least {contract['min_results']} search results, got {len(data['results'])}")

    return len(issues) == 0, issues


def validate_delivery(data: dict) -> tuple[bool, list]:
    """校验交付清单合同。"""
    issues = []
    contract = CONTRACTS["delivery-manifest"]

    for key in contract["required_keys"]:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    if "slides" in data:
        slides = data["slides"]
        if not isinstance(slides, list) or len(slides) == 0:
            issues.append("slides must be a non-empty list")
        for i, slide in enumerate(slides):
            if not isinstance(slide, dict):
                issues.append(f"Slide {i} must be a dict")
                continue
            if "file" not in slide:
                issues.append(f"Slide {i} missing 'file'")

    return len(issues) == 0, issues


def validate_file(contract_type: str, file_path: Path) -> tuple[bool, list]:
    """根据合同类型校验文件。"""
    if not file_path.exists():
        return False, [f"File not found: {file_path}"]

    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    validators = {
        "outline": validate_outline,
        "style": validate_style,
        "search": validate_search,
        "delivery": validate_delivery,
    }

    if contract_type not in validators:
        return False, [f"Unknown contract type: {contract_type}"]

    return validators[contract_type](data)


def main():
    parser = argparse.ArgumentParser(description="Contract Validator")
    parser.add_argument("contract_type", choices=["outline", "style", "search", "delivery"],
                        help="Type of contract to validate")
    parser.add_argument("path", type=Path, help="File or directory to validate")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")

    args = parser.parse_args()

    if args.contract_type == "delivery":
        manifest_path = args.path / "delivery-manifest.json"
        if args.path.is_file():
            manifest_path = args.path
        valid, issues = validate_file("delivery", manifest_path)
    else:
        valid, issues = validate_file(args.contract_type, args.path)

    if valid:
        print(f"✅ {args.contract_type} contract validation PASSED")
        sys.exit(0)
    else:
        print(f"❌ {args.contract_type} contract validation FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
