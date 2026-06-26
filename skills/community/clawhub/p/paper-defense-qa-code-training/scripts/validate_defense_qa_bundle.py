#!/usr/bin/env python3
"""Validate a paper-defense Q&A bundle.

Usage:
  python scripts/validate_defense_qa_bundle.py --root ./paper_defense_bundle --paper-slug my-paper
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_MD = [
    "defense_scope_cn.md",
    "claim_evidence_map_cn.md",
    "paper_attack_surface_cn.md",
    "code_training_audit_cn.md",
    "defense_qa_bank_cn.md",
    "answer_playbook_cn.md",
    "mock_defense_script_cn.md",
    "backup_slide_plan_cn.md",
    "evidence_gap_triage_cn.md",
    "visual_qa_storyboard_cn.md",
    "visual_image_prompt_pack_cn.md",
    "visual_generation_handoff_cn.md",
    "visual_card_copy_cn.md",
]

REQUIRED_SECTIONS = [
    "答辩范围与证据状态",
    "论文一句话主张与最安全表述",
    "核心贡献的可防守版本",
    "高风险问题总览",
    "论文层面问题与回答",
    "方法 / 公式 / 理论问题与回答",
    "实验 / 消融 / 基线问题与回答",
    "代码与训练过程问题与回答",
    "可复现性与工程实现问题与回答",
    "局限性 / 失败模式 / 伦理风险问题与回答",
    "未来工作与研究边界问题与回答",
    "最不该说的话",
    "备份页与证据材料清单",
    "模拟答辩脚本",
    "最后 10 分钟速记卡",
    "图文答辩卡片与生图提示词",
]

VALID_EVIDENCE_LABELS = {
    "paper_grounded",
    "code_grounded",
    "experiment_log_grounded",
    "review_grounded",
    "inferred",
    "missing_evidence",
    "external_context",
}


def fail(errors: list[str]) -> int:
    print("Validation failed:")
    for error in errors:
        print(f"- {error}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="paper_defense_bundle")
    parser.add_argument("--paper-slug", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    defense_dir = root / "generated" / "defense" / args.paper_slug
    errors: list[str] = []

    if not defense_dir.exists():
        errors.append(f"Defense directory missing: {defense_dir}")
        return fail(errors)

    for name in REQUIRED_MD:
        path = defense_dir / name
        if not path.exists():
            errors.append(f"Missing required Markdown: {path}")
        elif path.stat().st_size == 0:
            errors.append(f"Empty required Markdown: {path}")

    main_report = defense_dir / "defense_qa_bank_cn.md"
    if main_report.exists():
        text = main_report.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"Main report missing section: {section}")

    qa_path = defense_dir / "defense_qa_bank_cn.json"
    if not qa_path.exists():
        errors.append(f"Missing JSON QA bank: {qa_path}")
    else:
        try:
            data = json.loads(qa_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON: {qa_path}: {exc}")
            data = None
        if data is not None:
            for key in ["paper", "generation_context", "qa_items", "evidence_gaps", "dangerous_questions"]:
                if key not in data:
                    errors.append(f"JSON missing top-level key: {key}")
            qa_items = data.get("qa_items", []) if isinstance(data, dict) else []
            if not isinstance(qa_items, list):
                errors.append("qa_items must be a list")
            for idx, item in enumerate(qa_items):
                prefix = f"qa_items[{idx}]"
                for key in ["q_id", "question_cn", "audience", "attack_axis", "priority", "answer_short_cn", "evidence_labels", "confidence", "what_not_to_overclaim"]:
                    if key not in item:
                        errors.append(f"{prefix} missing key: {key}")
                labels = item.get("evidence_labels", [])
                if not isinstance(labels, list) or not labels:
                    errors.append(f"{prefix} evidence_labels must be non-empty list")
                else:
                    bad = [label for label in labels if label not in VALID_EVIDENCE_LABELS]
                    if bad:
                        errors.append(f"{prefix} has invalid evidence labels: {bad}")
                if item.get("priority") in {"P0", "P1"}:
                    if not item.get("backup_slide"):
                        errors.append(f"{prefix} is {item.get('priority')} but lacks backup_slide")
                    if not item.get("follow_up_experiment_or_code_check"):
                        errors.append(f"{prefix} is {item.get('priority')} but lacks follow_up_experiment_or_code_check")

    visual_path = defense_dir / "visual_qa_storyboard_cn.json"
    if not visual_path.exists():
        errors.append(f"Missing visual storyboard JSON: {visual_path}")
    else:
        try:
            visual_data = json.loads(visual_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON: {visual_path}: {exc}")
            visual_data = None
        if visual_data is not None:
            policy = visual_data.get("visual_policy", {})
            if policy.get("text_first_then_image") is not True:
                errors.append("visual_policy.text_first_then_image must be true")
            cards = visual_data.get("cards", [])
            if not isinstance(cards, list):
                errors.append("visual storyboard cards must be a list")
            for idx, card in enumerate(cards):
                prefix = f"visual_cards[{idx}]"
                for key in ["card_id", "linked_q_ids", "card_type", "question_cn", "spoken_answer_summary_cn", "evidence_labels", "boundary_cn", "image_prompt_cn", "generation_status"]:
                    if key not in card:
                        errors.append(f"{prefix} missing key: {key}")
                if card.get("generation_status") == "image_generated":
                    # This is allowed only after a separate image-generation stage. The bundle should still carry prompts.
                    if not card.get("image_prompt_cn"):
                        errors.append(f"{prefix} image_generated but lacks original image_prompt_cn")
                elif card.get("generation_status") not in {"text_ready", "image_pending"}:
                    errors.append(f"{prefix} invalid generation_status: {card.get('generation_status')}")
                if not card.get("linked_q_ids"):
                    errors.append(f"{prefix} must link to at least one Q_ID")

    if errors:
        return fail(errors)

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
