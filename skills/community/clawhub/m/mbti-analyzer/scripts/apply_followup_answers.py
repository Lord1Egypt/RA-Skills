#!/usr/bin/env python3
"""Apply follow-up answers, rebuild evidence, rerun inference, and rerender reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from build_evidence_pool import build_pool
from infer_mbti import infer_payload
from mbti_common import (
    AXIS_SIDES,
    detect_language_mix,
    iso_now,
    load_json,
    read_jsonl,
    resolve_path,
    shorten,
    split_into_segments,
    stable_id,
    write_json,
    write_jsonl,
)
from render_report import write_reports


VALID_AXES = {axis for axis, _, _ in AXIS_SIDES}


def parse_answer_arg(raw: str) -> Dict[str, str]:
    if "=" not in raw:
        raise ValueError(f"Expected AXIS=answer format, got {raw!r}")
    axis, answer = raw.split("=", 1)
    axis = axis.strip()
    answer = answer.strip()
    if axis not in VALID_AXES:
        raise ValueError(f"Unknown axis {axis!r}; expected one of {sorted(VALID_AXES)}")
    if not answer:
        raise ValueError(f"Answer for {axis} cannot be empty.")
    return {"axis": axis, "answer": answer}


def load_answers(answers_file: Path | None, inline_answers: List[str]) -> List[Dict[str, str]]:
    answers: List[Dict[str, str]] = []
    if answers_file is not None:
        payload = load_json(answers_file)
        if isinstance(payload, dict) and "answers" in payload:
            payload = payload["answers"]
        elif isinstance(payload, dict):
            payload = [{"axis": axis, "answer": text} for axis, text in payload.items()]
        if not isinstance(payload, list):
            raise ValueError("answers file must be a list, an axis->answer mapping, or an object with an 'answers' list.")
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError("Each answer entry must be an object with 'axis' and 'answer'.")
            axis = str(item.get("axis", "")).strip()
            answer = str(item.get("answer", "")).strip()
            if axis not in VALID_AXES or not answer:
                raise ValueError(f"Invalid answer entry: {item!r}")
            answers.append({"axis": axis, "answer": answer})
    for raw in inline_answers:
        answers.append(parse_answer_arg(raw))
    deduped: Dict[str, Dict[str, str]] = {}
    for item in answers:
        deduped[item["axis"]] = item
    return list(deduped.values())


def followup_prompt_map(analysis_payload: Dict) -> Dict[str, str]:
    prompts = {}
    for item in analysis_payload.get("followup_items", []):
        axis = item.get("axis")
        question = item.get("question")
        if axis in VALID_AXES and question:
            prompts[axis] = question
    return prompts


def followup_record(axis: str, answer: str, output_dir: Path) -> Dict:
    timestamp = iso_now()
    source_path = str(output_dir / "followup_answers.json")
    return {
        "record_id": stable_id([source_path, axis, answer]),
        "source_type": "followup-answers",
        "source_path": source_path,
        "location": f"followup:{axis}",
        "timestamp": timestamp,
        "speaker": "user",
        "conversation_id": "followup-answers",
        "content": answer,
    }


def merge_followup_records(records: List[Dict], answers: List[Dict[str, str]], output_dir: Path) -> List[Dict]:
    merged_followups: Dict[str, Dict] = {}
    base_records: List[Dict] = []
    for record in records:
        if record.get("source_type") == "followup-answers" and str(record.get("location", "")).startswith("followup:"):
            axis = str(record["location"]).split(":", 1)[1]
            merged_followups[axis] = record
        else:
            base_records.append(record)
    for item in answers:
        merged_followups[item["axis"]] = followup_record(item["axis"], item["answer"], output_dir)
    combined = base_records + [merged_followups[axis] for axis in sorted(merged_followups)]
    return combined


def summarize_sources(records: List[Dict], source_summary: Dict) -> Dict:
    approved = list(dict.fromkeys(source_summary.get("approved_source_types", []) + ["followup-answers"]))
    sources = {}
    for source_type in approved:
        matching = [record for record in records if record["source_type"] == source_type]
        if not matching:
            continue
        sources[source_type] = {
            "record_count": len(matching),
            "example_locations": [record["location"] for record in matching[:3]],
            "language_mix": detect_language_mix(" ".join(record["content"][:400] for record in matching[:5])),
            "sample_preview": [shorten(record["content"], 120) for record in matching[:2]],
        }
    return {
        "generated_at": iso_now(),
        "workspace_root": source_summary.get("workspace_root"),
        "openclaw_home": source_summary.get("openclaw_home"),
        "approved_source_types": approved,
        "record_count": len(records),
        "segment_estimate": sum(len(split_into_segments(record["content"])) for record in records),
        "sources": sources,
    }


def answers_payload(answers: List[Dict[str, str]], prompt_map: Dict[str, str]) -> Dict:
    return {
        "generated_at": iso_now(),
        "answers": [
            {
                "axis": item["axis"],
                "question": prompt_map.get(item["axis"], ""),
                "answer": item["answer"],
            }
            for item in answers
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply MBTI follow-up answers and rerun analysis.")
    parser.add_argument("--raw-records", required=True, help="Path to existing raw_records.jsonl")
    parser.add_argument("--source-summary", required=True, help="Path to existing source_summary.json")
    parser.add_argument("--analysis", required=True, help="Path to existing analysis_result.json")
    parser.add_argument("--output-dir", required=True, help="Directory where updated artifacts should be written")
    parser.add_argument("--answers-file", help="Optional JSON file with follow-up answers")
    parser.add_argument("--answer", action="append", default=[], help="Inline follow-up answer in AXIS=answer form; may be repeated")
    parser.add_argument("--quote-mode", choices=["summary", "none"], default="summary", help="Quote mode for rerendered report")
    args = parser.parse_args()

    output_dir = resolve_path(args.output_dir)
    answers_file = resolve_path(args.answers_file) if args.answers_file else None
    answers = load_answers(answers_file, args.answer)
    if not answers:
        parser.error("Provide at least one answer via --answer or --answers-file.")

    raw_records_path = resolve_path(args.raw_records)
    source_summary_path = resolve_path(args.source_summary)
    analysis_path = resolve_path(args.analysis)

    raw_records = read_jsonl(raw_records_path)
    source_summary = load_json(source_summary_path)
    analysis_payload = load_json(analysis_path)
    prompt_map = followup_prompt_map(analysis_payload)

    merged_records = merge_followup_records(raw_records, answers, output_dir)
    updated_summary = summarize_sources(merged_records, source_summary)
    evidence_payload = build_pool(merged_records, updated_summary)
    updated_analysis = infer_payload(evidence_payload, updated_summary)

    write_jsonl(output_dir / "raw_records.jsonl", merged_records)
    write_json(output_dir / "source_summary.json", updated_summary)
    write_json(output_dir / "followup_answers.json", answers_payload(answers, prompt_map))
    write_json(output_dir / "evidence_pool.json", evidence_payload)
    write_json(output_dir / "analysis_result.json", updated_analysis)
    write_reports(updated_analysis, evidence_payload, output_dir, args.quote_mode, auto_open=True)


if __name__ == "__main__":
    main()
