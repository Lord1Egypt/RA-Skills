#!/usr/bin/env python3
"""Build a normalized payload for Agent legal/compliance review."""

import argparse
import json
from pathlib import Path

from PIL import Image


DEFAULT_REFERENCE_FILES = [
    "compliance-rules.md",
    "forbidden-words.md",
    "common-cases.md",
    "advertising-law.md",
    "gb-28050-2025-nutrition-labeling.md",
    "gb-7718-2025-food-labeling.md",
]


MANDATORY_REVIEW_DIMENSIONS = [
    {
        "id": "absolute_or_market_position",
        "name": "绝对化/市场地位/领先宣称",
        "signals": ["领导者", "第一", "领先", "优选", "严选", "好牛奶"],
        "review_focus": "核查是否有完整数据来源、统计口径、时间、地域和品类范围。",
    },
    {
        "id": "health_or_function_implication",
        "name": "普通食品健康/功效暗示",
        "signals": ["守护", "自护", "安心", "健康", "免疫", "全天候"],
        "review_focus": "普通食品不得暗示保健、疾病预防治疗或持续健康保护效果。",
    },
    {
        "id": "nutrition_or_ingredient_claim",
        "name": "营养成分/配料数据宣称",
        "signals": ["蛋白", "钙", "低GI", "含量", "倍", "减少", "100mL"],
        "review_focus": "核查是否符合 GB 28050，是否有比较对象、检测报告和同屏限定条件。",
    },
    {
        "id": "certification_or_authority_endorsement",
        "name": "认证/科研/专家/机构背书",
        "signals": ["认证", "专家", "教授", "博士", "大学", "研究", "推荐", "证书"],
        "review_focus": "核查授权、合作范围和是否构成对产品品质/功效的权威背书。",
    },
    {
        "id": "quality_process_or_unverifiable_claim",
        "name": "品质过程/无法证实的因果表达",
        "signals": ["严格检验", "工序", "好奶", "幸福奶牛", "相信", "守护"],
        "review_focus": "核查强品质保证、因果关系和消费者可验证性。",
    },
    {
        "id": "small_print_or_citation_boundary",
        "name": "脚注/引证/限制条件展示",
        "signals": ["数据来源", "文献", "注", "报告", "检测"],
        "review_focus": "核查限制条件是否就近、清晰、字号足够，能否支撑主视觉宣称。",
    },
]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_references(reference_dir, names, max_chars_per_file):
    summaries = []
    for name in names:
        path = Path(reference_dir) / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        summaries.append({
            "name": name,
            "path": str(path),
            "excerpt": text[:max_chars_per_file],
            "truncated": len(text) > max_chars_per_file,
        })
    return summaries


def build_payload(
    image_path,
    ocr_regions,
    rule_risks,
    rules_data,
    review_mode,
    reference_dir,
    reference_names=None,
    max_reference_chars=2400,
):
    image = Image.open(image_path)
    reference_names = reference_names or DEFAULT_REFERENCE_FILES
    return {
        "schema_version": "1.1",
        "review_mode": review_mode,
        "image": {
            "path": str(image_path),
            "width": image.size[0],
            "height": image.size[1],
        },
        "ocr": ocr_regions,
        "ocr_text": "\n".join(
            item.get("text", "").strip()
            for item in ocr_regions
            if item.get("text", "").strip()
        ),
        "rule_risks": rule_risks,
        "knowledge": {
            "risk_rules": rules_data,
            "references": summarize_references(reference_dir, reference_names, max_reference_chars),
        },
        "agent_task": {
            "goal": "基于 OCR 全文、规则候选和知识库，从广告审核法务视角复核并扩展风险点。",
            "allowed_actions": ["keep", "exclude", "adjust", "merge", "add"],
            "must_scan_ocr_text": True,
            "must_add_rule_misses": True,
            "do_not_passthrough_rule_risks_only": True,
            "mandatory_review_dimensions": MANDATORY_REVIEW_DIMENSIONS,
            "low_count_policy": "如果最终风险少于 4 条，必须在 notes 中逐项说明已检查哪些维度以及为什么不构成风险。",
            "required_output": "agent_risks.json",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="构建给 Agent 复核使用的 payload JSON")
    parser.add_argument("image_path", help="图片路径")
    parser.add_argument("ocr_json", help="OCR JSON 路径")
    parser.add_argument("rule_risks_json", help="规则命中风险 JSON 路径")
    parser.add_argument("rules_json", help="风险规则 JSON 路径")
    parser.add_argument("output_json", help="输出 agent_payload.json 路径")
    parser.add_argument("--review-mode", default="balanced", help="审核模式")
    parser.add_argument("--reference-dir", default=str(Path(__file__).resolve().parent.parent / "references"),
                        help="知识库目录")
    parser.add_argument("--reference", action="append", dest="references",
                        help="要放入 payload 的 reference 文件名，可重复传入")
    parser.add_argument("--max-reference-chars", type=int, default=2400,
                        help="每个 reference 最多截取字符数")
    args = parser.parse_args()

    payload = build_payload(
        Path(args.image_path),
        load_json(args.ocr_json),
        load_json(args.rule_risks_json),
        load_json(args.rules_json),
        args.review_mode,
        args.reference_dir,
        args.references,
        args.max_reference_chars,
    )
    Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Payload: {args.output_json}")
    print(f"OCR regions: {len(payload['ocr'])}")
    print(f"Rule risks: {len(payload['rule_risks'])}")
    print(f"References: {len(payload['knowledge']['references'])}")


if __name__ == "__main__":
    main()
