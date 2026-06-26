#!/usr/bin/env python3
"""Generate visual Q&A storyboard and image prompt pack from a defense QA bank.

Usage:
  python scripts/generate_visual_qa_prompt_pack.py --root ./paper_defense_bundle --paper-slug my-paper

This script prepares text artifacts only. It does not call any image API.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HIGH_VALUE_AXES = {
    "novelty",
    "method",
    "formula",
    "theory",
    "experiments",
    "ablation",
    "baseline",
    "code",
    "training",
    "reproducibility",
    "compute",
    "limitations",
    "ethics",
}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def pick_card_type(axis: str, question: str) -> str:
    q = question.lower()
    if axis in {"code"} or "code" in q or "代码" in question:
        return "equation_to_code_bridge"
    if axis in {"training", "reproducibility", "compute"} or "seed" in q or "训练" in question:
        return "training_timeline"
    if axis in {"baseline", "experiments", "ablation"} or "baseline" in q or "基线" in question:
        return "baseline_fairness_board"
    if axis in {"novelty", "related_work", "problem"} or "贡献" in question or "新" in question:
        return "claim_evidence_map"
    if axis in {"method", "formula", "theory"} or "公式" in question or "方法" in question:
        return "method_pipeline"
    if axis in {"limitations", "ethics", "future_work"} or "局限" in question or "失败" in question:
        return "limitation_boundary_card"
    return "recovery_answer_card"


def visual_concept(card_type: str) -> str:
    concepts = {
        "claim_evidence_map": "三栏图：Closest Prior Work → This Paper → Evidence + Boundary，用箭头展示可防守贡献与证据边界。",
        "attack_surface_radar": "雷达图或热力图：novelty、soundness、reproducibility、compute、ethics 五个风险维度。",
        "method_pipeline": "左到右方法流水线：输入、核心模块、训练信号、输出、推理路径。",
        "equation_to_code_bridge": "桥接图：论文公式/模块在左，代码文件、函数、config key 在右，中间用映射箭头连接。",
        "training_timeline": "训练时间线：数据 split、preprocess、train、validate、checkpoint、test、reporting。",
        "baseline_fairness_board": "公平性对照板：same data、same metric、same tuning budget、same evaluation protocol。",
        "limitation_boundary_card": "安全边界图：中心是支持结论，外圈是未验证场景和证据缺口。",
        "recovery_answer_card": "答辩恢复卡：Claim、Evidence、Boundary、Follow-up 四步回答模板。",
        "backup_slide_visual": "备用页式图解：用 appendix 风格展示证据、表格、代码路径或实验设置。",
        "qa_flashcard": "一问一答卡片：左侧问题，右侧短答，下方证据和不能过度声称。",
        "comic_metaphor": "学术漫画分镜：委员会提问、报告者用证据和边界稳健回答。",
    }
    return concepts.get(card_type, concepts["recovery_answer_card"])


def build_prompt(
    *,
    paper_title: str,
    card_type: str,
    question: str,
    answer: str,
    boundary: str,
    evidence_labels: list[str],
    style: str,
    aspect_ratio: str,
) -> str:
    labels = ", ".join(evidence_labels) if evidence_labels else "missing_evidence"
    return (
        f"Create a {aspect_ratio} clean academic infographic for a computer-science paper defense. "
        f"Paper context: {paper_title or 'target paper'}. "
        f"Card type: {card_type}. Purpose: visually explain the defense question: '{question}'. "
        f"Show a concise answer structure: Claim, Evidence, Boundary, Follow-up. "
        f"Evidence labels to represent: {labels}. "
        f"Main visual concept: {visual_concept(card_type)} "
        f"Use this answer summary as guidance, but do not fabricate citations: {answer[:400]}. "
        f"Boundary to emphasize: {boundary[:300]}. "
        f"Style: {style}; high readability; PPT-friendly; minimal clutter; consistent icons; calm academic tone. "
        "Leave blank areas for exact paper-specific section numbers, code paths, equations, or table numbers to be overlaid later. "
        "Avoid fake citations, fake table numbers, unreadable tiny text, photorealistic people, sensational claims, and decorative elements unrelated to the defense."
    )


def select_items(qa_items: list[dict[str, Any]], max_cards: int) -> list[dict[str, Any]]:
    def score(item: dict[str, Any]) -> tuple[int, int, int]:
        priority = item.get("priority", "P4")
        axis = item.get("attack_axis", "")
        priority_score = {"P0": 100, "P1": 90, "P2": 70, "P3": 40, "P4": 10}.get(priority, 0)
        axis_score = 25 if axis in HIGH_VALUE_AXES else 0
        severity_score = {"high": 20, "medium": 10, "low": 0}.get(item.get("severity", ""), 0)
        return (priority_score + axis_score + severity_score, axis_score, priority_score)

    ordered = sorted(qa_items, key=score, reverse=True)
    return ordered[:max_cards]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="paper_defense_bundle")
    parser.add_argument("--paper-slug", required=True)
    parser.add_argument("--max-cards", type=int, default=12)
    parser.add_argument("--target-environment", default="chatgpt_web", choices=["chatgpt_web", "codex_cli", "api_pipeline", "manual_ppt"])
    parser.add_argument("--preferred-model", default="Codex imagegen skill first when running inside Codex; otherwise ChatGPT Images 2.0 / gpt-image-2 when available")
    parser.add_argument("--style", default="clean academic infographic, PPT-friendly, consistent icon system, high readability")
    parser.add_argument("--aspect-ratio", default="16:9")
    args = parser.parse_args()

    root = Path(args.root)
    defense_dir = root / "generated" / "defense" / args.paper_slug
    qa_path = defense_dir / "defense_qa_bank_cn.json"
    qa = read_json(qa_path)

    paper = qa.get("paper", {})
    paper_title = paper.get("paper_title", "")
    qa_items = qa.get("qa_items", [])
    if not isinstance(qa_items, list):
        raise SystemExit("qa_items must be a list")

    cards: list[dict[str, Any]] = []
    for idx, item in enumerate(select_items(qa_items, args.max_cards), start=1):
        q_id = str(item.get("q_id", f"Q{idx:03d}"))
        question = str(item.get("question_cn", "待填问题"))
        axis = str(item.get("attack_axis", "presentation"))
        card_type = pick_card_type(axis, question)
        evidence_labels = item.get("evidence_labels", [])
        if not isinstance(evidence_labels, list) or not evidence_labels:
            evidence_labels = ["missing_evidence"]
        answer = str(item.get("answer_short_cn") or item.get("answer_long_cn") or "待填短回答。")
        boundary = str(item.get("what_not_to_overclaim") or "不要声称超过论文、代码或训练日志能支持的范围。")
        card = {
            "card_id": f"VC{idx:03d}",
            "linked_q_ids": [q_id],
            "card_type": card_type,
            "priority": item.get("priority", "P3"),
            "audience": item.get("audience", []),
            "title_cn": f"图解 {q_id}: {question[:34]}",
            "question_cn": question,
            "spoken_answer_summary_cn": answer,
            "evidence_labels": evidence_labels,
            "boundary_cn": boundary,
            "visual_concept_cn": visual_concept(card_type),
            "image_prompt_cn": build_prompt(
                paper_title=paper_title,
                card_type=card_type,
                question=question,
                answer=answer,
                boundary=boundary,
                evidence_labels=evidence_labels,
                style=args.style,
                aspect_ratio=args.aspect_ratio,
            ),
            "negative_prompt_cn": "不要生成假引用、假表号、假代码路径、无法辨认的小字、夸张宣传语或与答辩无关的装饰元素。",
            "text_overlay_plan_cn": "后期在 PPT/SVG/HTML 中叠加精确论文标题、章节号、表格号、代码路径、公式和证据标签。",
            "style_consistency_notes_cn": "保持同一画幅、图标、线条粗细、标题区域、证据标签位置和 Claim/Evidence/Boundary/Follow-up 四格结构。",
            "revision_prompt_cn": "请保留核心布局，减少装饰，增加空白区，确保后续可以覆盖准确论文文本。",
            "generation_status": "image_pending",
        }
        cards.append(card)
        item.setdefault("visual_card_ids", [])
        if card["card_id"] not in item["visual_card_ids"]:
            item["visual_card_ids"].append(card["card_id"])
        item.setdefault("visualization_hint", card["visual_concept_cn"])

    storyboard = {
        "paper": {
            "paper_slug": paper.get("paper_slug", args.paper_slug),
            "paper_title": paper_title,
            "venue": paper.get("venue", ""),
            "year": paper.get("year", ""),
        },
        "visual_policy": {
            "text_first_then_image": True,
            "target_environment": args.target_environment,
            "preferred_model": args.preferred_model,
            "style_brief": args.style,
            "aspect_ratio": args.aspect_ratio,
            "exact_text_policy": "Use generated images for layout/metaphor; overlay exact equations, code, section numbers, and dense labels later in PPT/SVG/HTML.",
            "generation_reminder_cn": "先交付文字版问答和提示词。后续单独请求 create image 模式或 API 生图。",
        },
        "cards": cards,
    }

    write_text(defense_dir / "visual_qa_storyboard_cn.json", json.dumps(storyboard, ensure_ascii=False, indent=2))
    write_text(defense_dir / "defense_qa_bank_cn.json", json.dumps(qa, ensure_ascii=False, indent=2))

    md_lines = [
        f"# {paper_title or args.paper_slug}：图文答辩卡片 Storyboard",
        "",
        "## 生图分离原则",
        "",
        "本文件只准备文字、storyboard 和提示词，不直接生成图片。后续请单独生图：在 Codex 内优先使用 `imagegen` skill；非 Codex 场景使用 ChatGPT create image 模式、ChatGPT Images 2.0 / `gpt-image-2` API，或用户批准的高级文生图 API。",
        "",
        "| Card | Linked Q | Type | Priority | Evidence | Status |",
        "|---|---|---|---|---|---|",
    ]
    for card in cards:
        md_lines.append(
            f"| {card['card_id']} | {', '.join(card['linked_q_ids'])} | {card['card_type']} | {card.get('priority','')} | {', '.join(card['evidence_labels'])} | {card['generation_status']} |"
        )
    for card in cards:
        md_lines.extend([
            "",
            f"## {card['card_id']}｜{card['title_cn']}",
            "",
            f"- **关联问题**：{', '.join(card['linked_q_ids'])}",
            f"- **问题**：{card['question_cn']}",
            f"- **口头回答摘要**：{card['spoken_answer_summary_cn']}",
            f"- **证据标签**：{', '.join(card['evidence_labels'])}",
            f"- **不能过度声称**：{card['boundary_cn']}",
            f"- **视觉概念**：{card['visual_concept_cn']}",
            f"- **文字覆盖计划**：{card['text_overlay_plan_cn']}",
            f"- **状态**：{card['generation_status']}",
        ])
    write_text(defense_dir / "visual_qa_storyboard_cn.md", "\n".join(md_lines) + "\n")

    prompt_lines = [
        f"# {paper_title or args.paper_slug}：Visual Image Prompt Pack",
        "",
        "先不要在同一步生成图片。文字问答完成后，把下面这句作为最终生图请求：请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。",
    ]
    for card in cards:
        prompt_lines.extend([
            "",
            f"## {card['card_id']}｜{card['title_cn']}",
            "",
            "```text",
            card["image_prompt_cn"],
            "```",
            "",
            f"Negative / avoid: {card['negative_prompt_cn']}",
            f"Revision prompt: {card['revision_prompt_cn']}",
        ])
    write_text(defense_dir / "visual_image_prompt_pack_cn.md", "\n".join(prompt_lines) + "\n")

    handoff = f"""# Visual Generation Handoff

## 当前状态

- Paper: {paper_title or args.paper_slug}
- Cards prepared: {len(cards)}
- Image status: image_pending
- Preferred model: {args.preferred_model}
- Target environment: {args.target_environment}

## ChatGPT 网页版提问方式

```text
请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。
```

## Codex / CLI / API 提醒

把 `visual_qa_storyboard_cn.json` 当成任务清单，把 `visual_image_prompt_pack_cn.md` 当成 prompt 列表。在 Codex 内实际生图时，优先调用 `imagegen` skill；非 Codex 场景再用 ChatGPT Images 2.0 / `gpt-image-2` 或用户批准的高级文生图 API 逐张生成。不要把文字问答生成和图片生成调用混在同一个回答步骤。
"""
    write_text(defense_dir / "visual_generation_handoff_cn.md", handoff)

    copy_lines = [f"# {paper_title or args.paper_slug}：图文卡片文案", ""]
    for card in cards:
        copy_lines.extend([
            f"## {card['card_id']}",
            f"**问题**：{card['question_cn']}",
            f"**短答**：{card['spoken_answer_summary_cn']}",
            f"**证据**：{', '.join(card['evidence_labels'])}",
            f"**边界**：{card['boundary_cn']}",
            "",
        ])
    write_text(defense_dir / "visual_card_copy_cn.md", "\n".join(copy_lines))

    print(f"Generated {len(cards)} visual cards under {defense_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
