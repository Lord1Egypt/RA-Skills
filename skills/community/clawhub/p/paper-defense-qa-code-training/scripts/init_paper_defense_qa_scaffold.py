#!/usr/bin/env python3
"""Initialize a paper-defense Q&A scaffold.

Usage:
  python scripts/init_paper_defense_qa_scaffold.py --root ./paper_defense_bundle --paper-slug my-paper --paper-title "My Paper"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


def slugify(value: str) -> str:
    keep = []
    last_dash = False
    for ch in value.lower():
        if ch.isalnum():
            keep.append(ch)
            last_dash = False
        elif not last_dash:
            keep.append("-")
            last_dash = True
    return "".join(keep).strip("-") or "paper"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="paper_defense_bundle")
    parser.add_argument("--paper-slug", default="")
    parser.add_argument("--paper-title", default="Untitled Paper")
    parser.add_argument("--venue", default="")
    parser.add_argument("--year", default="")
    args = parser.parse_args()

    root = Path(args.root)
    slug = args.paper_slug or slugify(args.paper_title)
    defense_dir = root / "generated" / "defense" / slug
    metadata_dir = root / "metadata"
    reports_dir = root / "reports"

    for directory in [defense_dir, metadata_dir, reports_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    focus_spec = {
        "paper_id": slug,
        "paper_slug": slug,
        "paper_title": args.paper_title,
        "venue": args.venue,
        "year": args.year,
        "paper_subfield": "",
        "defense_context": "lab_meeting",
        "target_audience": ["advisor", "peer", "reviewer"],
        "available_time_minutes": 30,
        "expected_qna_minutes": 30,
        "risk_tolerance": "conservative",
        "input_artifacts": {
            "deep_read_report_path": "",
            "paper_pdf_path": "",
            "supplement_path": "",
            "openreview_digest_path": "",
            "code_repo_path": "",
            "training_logs_dir": "",
            "configs_dir": "",
            "checkpoints_dir": "",
            "slides_path": ""
        },
        "known_weaknesses": [],
        "known_sensitive_points": [],
        "must_prepare_axes": [
            "novelty", "soundness", "experiments", "code", "training", "reproducibility", "limitations"
        ],
        "output_language": "zh-CN",
        "visual_mode": {
            "enabled": False,
            "text_first_then_image": True,
            "target_environment": "chatgpt_web",
            "preferred_image_model": "Codex imagegen skill first when running inside Codex; otherwise ChatGPT Images 2.0 / gpt-image-2 when available",
            "series_style": "clean academic infographic, PPT-friendly, consistent layout",
            "aspect_ratio": "16:9",
            "max_cards": 12,
            "prioritize_questions": ["P0", "P1", "code", "training", "reproducibility", "limitations"],
            "exact_text_policy": "overlay exact equations/code/text outside generated image when precision matters"
        }
    }
    write_text(metadata_dir / "defense_focus_spec.json", json.dumps(focus_spec, ensure_ascii=False, indent=2))

    status = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "paper_slug": slug,
        "status": "initialized",
        "required_outputs": [
            "defense_scope_cn.md",
            "claim_evidence_map_cn.md",
            "paper_attack_surface_cn.md",
            "code_training_audit_cn.md",
            "defense_qa_bank_cn.md",
            "defense_qa_bank_cn.json",
            "answer_playbook_cn.md",
            "mock_defense_script_cn.md",
            "backup_slide_plan_cn.md",
            "evidence_gap_triage_cn.md",
            "visual_qa_storyboard_cn.md",
            "visual_qa_storyboard_cn.json",
            "visual_image_prompt_pack_cn.md",
            "visual_generation_handoff_cn.md",
            "visual_card_copy_cn.md"
        ],
        "blockers": []
    }
    write_text(metadata_dir / "defense_generation_status.json", json.dumps(status, ensure_ascii=False, indent=2))

    markdown_files = {
        "defense_scope_cn.md": f"# {args.paper_title}：答辩范围与证据状态\n\n待填。\n",
        "claim_evidence_map_cn.md": "# Claim-Evidence Map\n\n| Claim | Evidence | Evidence label | Strength | Caveat | Likely question | Safe answer posture |\n|---|---|---|---|---|---|---|\n",
        "paper_attack_surface_cn.md": "# 论文层面攻击面\n\n待填。\n",
        "code_training_audit_cn.md": "# 代码与训练过程审计\n\n待填。\n",
        "defense_qa_bank_cn.md": f"# {args.paper_title}：答辩问答与代码/训练审计包\n\n## 1. 答辩范围与证据状态\n\n待填。\n\n## 2. 论文一句话主张与最安全表述\n\n待填。\n\n## 3. 核心贡献的可防守版本\n\n待填。\n\n## 4. 高风险问题总览\n\n待填。\n\n## 5. 论文层面问题与回答\n\n待填。\n\n## 6. 方法 / 公式 / 理论问题与回答\n\n待填。\n\n## 7. 实验 / 消融 / 基线问题与回答\n\n待填。\n\n## 8. 代码与训练过程问题与回答\n\n待填。\n\n## 9. 可复现性与工程实现问题与回答\n\n待填。\n\n## 10. 局限性 / 失败模式 / 伦理风险问题与回答\n\n待填。\n\n## 11. 未来工作与研究边界问题与回答\n\n待填。\n\n## 12. 最不该说的话\n\n待填。\n\n## 13. 备份页与证据材料清单\n\n待填。\n\n## 14. 模拟答辩脚本\n\n待填。\n\n## 15. 最后 10 分钟速记卡\n\n待填。\n\n## 16. 图文答辩卡片与生图提示词\n\n待填。\n",
        "answer_playbook_cn.md": "# 答辩回答 Playbook\n\n待填。\n",
        "mock_defense_script_cn.md": "# 模拟答辩脚本\n\n待填。\n",
        "backup_slide_plan_cn.md": "# 备份页计划\n\n| Question | Backup slide title | Content | Evidence | When to show |\n|---|---|---|---|---|\n",
        "evidence_gap_triage_cn.md": "# 证据缺口三角化\n\n| Gap | Risk | Affected questions | Recommended fix |\n|---|---|---|---|\n",
        "visual_qa_storyboard_cn.md": "# 图文答辩卡片 Storyboard\n\n本文件只准备文字 storyboard，不直接生成图片。\n",
        "visual_image_prompt_pack_cn.md": "# Visual Image Prompt Pack\n\n后续可以单独使用下面这句请求生图：请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。\n",
        "visual_generation_handoff_cn.md": "# Visual Generation Handoff\n\n## ChatGPT 网页版提问方式\n\n请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。\n\n## Codex / CLI / API 提醒\n\n如果在 Codex 内使用，实际生图时优先调用 imagegen skill；非 Codex 场景再使用 ChatGPT Images 2.0 / gpt-image-2 或用户批准的高级文生图 API。不要把文字问答生成和图片生成调用混在同一步。\n",
        "visual_card_copy_cn.md": "# 图文卡片文案\n\n待填。\n"
    }
    for filename, content in markdown_files.items():
        write_text(defense_dir / filename, content)

    qa_json = {
        "paper": {
            "paper_id": slug,
            "paper_title": args.paper_title,
            "paper_slug": slug,
            "venue": args.venue,
            "year": args.year,
            "subfield": ""
        },
        "generation_context": {
            "defense_context": "lab_meeting",
            "target_audience": ["advisor", "peer", "reviewer"],
            "input_artifacts": [],
            "missing_artifacts": [],
            "risk_tolerance": "conservative"
        },
        "qa_items": [],
        "evidence_gaps": [],
        "dangerous_questions": []
    }
    write_text(defense_dir / "defense_qa_bank_cn.json", json.dumps(qa_json, ensure_ascii=False, indent=2))

    visual_storyboard = {
        "paper": {
            "paper_slug": slug,
            "paper_title": args.paper_title,
            "venue": args.venue,
            "year": args.year
        },
        "visual_policy": {
            "text_first_then_image": True,
            "target_environment": "chatgpt_web",
            "preferred_model": "Codex imagegen skill first when running inside Codex; otherwise ChatGPT Images 2.0 / gpt-image-2 when available",
            "style_brief": "clean academic infographic, PPT-friendly, consistent icon system",
            "aspect_ratio": "16:9",
            "exact_text_policy": "Use generated images for layout/metaphor; overlay exact equations, code, and dense text later.",
            "generation_reminder_cn": "先交付文字版问答和提示词，后续单独请求 create image 模式或 API 生图。"
        },
        "cards": []
    }
    write_text(defense_dir / "visual_qa_storyboard_cn.json", json.dumps(visual_storyboard, ensure_ascii=False, indent=2))

    handoff = f"# Stage Delivery Handoff\n\n- Paper: {args.paper_title}\n- Slug: {slug}\n- Status: initialized\n- Next: fill defense Q&A bank, optionally generate visual storyboard, and run validation.\n"
    write_text(reports_dir / "stage_delivery_handoff.md", handoff)

    print(f"Initialized defense scaffold at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
