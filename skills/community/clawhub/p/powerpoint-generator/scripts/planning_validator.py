#!/usr/bin/env python3
"""Planning Validator -- 校验单页和全量 Planning JSON 的 schema 与 density_contract

用法:
  python planning_validator.py OUTPUT_DIR/planning.json
  python planning_validator.py OUTPUT_DIR/planning.json --page 3
  python planning_validator.py OUTPUT_DIR/planning.json --strict
"""

import argparse
import json
import sys
from pathlib import Path


# -------------------------------------------------------------------
# 常量
# -------------------------------------------------------------------
DENSITY_LEVELS = ["low", "medium", "high"]

CARD_TYPES = [
    "text", "data", "list", "tag_cloud", "process",
    "timeline", "comparison", "quote", "stat_block",
    "feature_grid", "image_text", "data_highlight"
]

LAYOUTS = [
    "single_focus", "50_50_symmetric", "asymmetric_two_col",
    "three_col_equal", "primary_secondary", "hero_with_subs", "mixed_grid"
]


# -------------------------------------------------------------------
# 校验规则
# -------------------------------------------------------------------
def validate_page_planning(page_data: dict, page_num: int, strict: bool = False) -> list:
    """校验单页 planning JSON。"""
    issues = []

    # 必须字段
    required = ["page_number", "page_type", "title", "layout_hint", "cards"]
    for key in required:
        if key not in page_data:
            issues.append(f"Page {page_num}: missing required key '{key}'")

    # page_number 一致性
    if "page_number" in page_data and page_data["page_number"] != page_num:
        issues.append(f"Page {page_num}: page_number mismatch (expected {page_num}, got {page_data['page_number']})")

    # page_type 校验
    valid_page_types = ["cover", "section", "content", "end"]
    if "page_type" in page_data and page_data["page_type"] not in valid_page_types:
        issues.append(f"Page {page_num}: invalid page_type '{page_data['page_type']}'. Must be one of {valid_page_types}")

    # layout_hint 校验
    if "layout_hint" in page_data:
        layout = page_data["layout_hint"]
        if isinstance(layout, str) and layout not in LAYOUTS:
            issues.append(f"Page {page_num}: invalid layout_hint '{layout}'. Must be one of {LAYOUTS}")
        if isinstance(layout, dict) and "type" in layout:
            if layout["type"] not in LAYOUTS:
                issues.append(f"Page {page_num}: invalid layout type '{layout['type']}'")

    # cards 校验
    if "cards" in page_data:
        cards = page_data["cards"]
        if not isinstance(cards, list):
            issues.append(f"Page {page_num}: cards must be a list")
        elif len(cards) == 0:
            issues.append(f"Page {page_num}: at least 1 card required")
        else:
            card_types_in_page = set()
            data_cards = 0
            for j, card in enumerate(cards):
                if not isinstance(card, dict):
                    issues.append(f"Page {page_num}: card {j} must be a dict")
                    continue
                if "card_type" not in card:
                    issues.append(f"Page {page_num}: card {j} missing 'card_type'")
                elif card["card_type"] not in CARD_TYPES:
                    issues.append(f"Page {page_num}: card {j} invalid type '{card['card_type']}'")
                else:
                    card_types_in_page.add(card["card_type"])
                    if card["card_type"] == "data":
                        data_cards += 1

            # 内容页至少 3 张卡片
            if page_data.get("page_type") == "content" and len(cards) < 3:
                issues.append(f"Page {page_num}: content page must have at least 3 cards, got {len(cards)}")

            # 内容页至少 2 种 card_type
            if page_data.get("page_type") == "content" and len(card_types_in_page) < 2:
                issues.append(f"Page {page_num}: content page must have at least 2 different card_types, got {card_types_in_page}")

            # 内容页至少 1 张 data 卡片
            if page_data.get("page_type") == "content" and data_cards == 0:
                issues.append(f"Page {page_num}: content page must have at least 1 data card")

    # density_contract 校验（strict 模式）
    if strict and "density_contract" in page_data:
        dc = page_data["density_contract"]
        if not isinstance(dc, dict):
            issues.append(f"Page {page_num}: density_contract must be a dict")
        else:
            if "max_cards" in dc:
                if not isinstance(dc["max_cards"], int) or dc["max_cards"] < 1:
                    issues.append(f"Page {page_num}: density_contract.max_cards must be a positive integer")
                elif "cards" in page_data and len(page_data["cards"]) > dc["max_cards"]:
                    issues.append(f"Page {page_num}: exceeds max_cards ({dc['max_cards']})")

            if "max_charts" in dc:
                if not isinstance(dc["max_charts"], int) or dc["max_charts"] < 0:
                    issues.append(f"Page {page_num}: density_contract.max_charts must be a non-negative integer")

            if "min_body_font_px" in dc:
                if not isinstance(dc["min_body_font_px"], (int, float)) or dc["min_body_font_px"] < 6:
                    issues.append(f"Page {page_num}: density_contract.min_body_font_px must be >= 6")

    return issues


def validate_planning_file(file_path: Path, page_num: int = None, strict: bool = False) -> tuple[bool, list]:
    """校验 planning JSON 文件。"""
    if not file_path.exists():
        return False, [f"File not found: {file_path}"]

    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    issues = []

    # 支持单页（dict）和全量（list）两种格式
    if isinstance(data, list):
        for i, page in enumerate(data):
            page_num = page.get("page_number", i + 1)
            page_issues = validate_page_planning(page, page_num, strict)
            issues.extend(page_issues)
    elif isinstance(data, dict):
        page_num = page_num or data.get("page_number", 0)
        issues = validate_page_planning(data, page_num, strict)
    else:
        return False, ["Planning JSON must be a dict or list of page objects"]

    return len(issues) == 0, issues


def main():
    parser = argparse.ArgumentParser(description="Planning Validator")
    parser.add_argument("planning_file", type=Path, help="Planning JSON file or directory")
    parser.add_argument("--page", type=int, help="Validate specific page number")
    parser.add_argument("--strict", action="store_true", help="Enable strict density_contract validation")
    parser.add_argument("--summary", action="store_true", help="Show summary only")

    args = parser.parse_args()

    # 如果是目录，找 planning.json
    if args.planning_file.is_dir():
        planning_path = args.planning_file / "planning.json"
    else:
        planning_path = args.planning_file

    valid, issues = validate_planning_file(planning_path, args.page, args.strict)

    if args.summary:
        if valid:
            print(f"✅ All checks passed")
        else:
            print(f"❌ {len(issues)} issue(s) found:")
            for issue in issues[:5]:
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
    else:
        if valid:
            print(f"✅ Planning validation PASSED")
        else:
            print(f"❌ Planning validation FAILED ({len(issues)} issue(s)):")
            for issue in issues:
                print(f"  - {issue}")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
