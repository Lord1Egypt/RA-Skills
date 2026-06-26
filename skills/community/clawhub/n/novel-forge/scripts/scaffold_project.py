#!/usr/bin/env python3
"""Create a Novel Forge project scaffold."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "novel-project"


def parse_models_json(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid --models-json: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("invalid --models-json: expected a JSON object mapping roles to provider/model-id strings")
    return {str(k): str(v) for k, v in data.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    parser.add_argument("--genre", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--target-chapters", type=int, default=50)
    parser.add_argument("--chapter-min", type=int, default=2000)
    parser.add_argument("--chapter-max", type=int, default=4000)
    parser.add_argument("--out-dir", default="novel")
    parser.add_argument("--resume-from", default="")
    parser.add_argument("--resume-mode", default="new", choices=["new", "continue", "truncated", "checkpoint"])
    parser.add_argument("--execution-mode", default="multi-agent", choices=["single-agent", "multi-agent"])
    parser.add_argument("--latest-chapter-index", type=int, default=0)
    parser.add_argument("--partial-draft", default="")
    parser.add_argument("--models-json", default="")
    args = parser.parse_args()

    slug = slugify(args.title)
    root = Path(args.out_dir).expanduser().resolve() / slug
    chapters = root / "chapters"
    state_dir = root / "state"
    root.mkdir(parents=True, exist_ok=True)
    chapters.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    chapter_number = max(1, args.latest_chapter_index + 1)
    project = {
        "project": {
            "title": args.title,
            "genre": args.genre,
            "audience": args.audience,
            "targetChapters": args.target_chapters,
            "chapterWordRange": [args.chapter_min, args.chapter_max],
            "status": "draft",
            "executionMode": args.execution_mode,
            "premise": "",
            "tabooList": [],
            "bootstrapLocked": False,
            "latestChapterIndex": args.latest_chapter_index,
            "lastCheckpoint": "",
            "resumeFrom": args.resume_from,
            "resumeMode": args.resume_mode,
        },
        "models": parse_models_json(args.models_json),
        "canon": {"hard": [], "soft": [], "world": {}, "characters": [], "timeline": [], "factions": []},
        "planning": {"outline": {}, "volumes": [], "chapters": [], "currentBeat": {}, "partialDrafts": []},
        "style": {"candidates": [], "selected": "", "rules": []},
        "memory": {
            "fullSummary": "",
            "recentSummaries": [],
            "openLoops": [],
            "characterStates": {},
            "foreshadowing": [],
            "recoverySummary": "",
            "lastKnownState": args.partial_draft,
        },
    }

    current_state = {
        "project": {
            "title": args.title,
            "genre": args.genre,
            "audience": args.audience,
            "status": "draft",
            "executionMode": args.execution_mode,
            "latestChapterIndex": args.latest_chapter_index,
            "nextChapterIndex": chapter_number,
        },
        "workflow": {
            "step": "idle",
            "chapterIndex": args.latest_chapter_index,
            "nextChapterIndex": chapter_number,
        },
        "recoveryCheckpoint": {
            "resumeMode": args.resume_mode,
            "lastStableSentenceOrBeat": "",
            "knownCanonFacts": [],
            "unknownsThatMustNotBeInvented": [],
            "partialDraftSource": args.partial_draft,
            "nextAction": "continue recovery" if args.resume_from else "start project bootstrap",
            "userConfirmationRequired": bool(args.resume_from),
        },
        "chapter": {
            "currentChapterIndex": args.latest_chapter_index,
            "nextChapterIndex": chapter_number,
        },
    }

    (root / "project.json").write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "worldbuilding.md").write_text("# Worldbuilding\n\n", encoding="utf-8")
    (root / "characters.md").write_text("# Characters\n\n", encoding="utf-8")
    (root / "outline.md").write_text("# Outline\n\n", encoding="utf-8")
    (root / "style.md").write_text("# Style\n\n", encoding="utf-8")
    (root / "memory.md").write_text("# Memory\n\n", encoding="utf-8")
    (state_dir / "current.json").write_text(json.dumps(current_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (chapters / f"{chapter_number:04d}.md").write_text(f"# Chapter {chapter_number}\n\n", encoding="utf-8")
    if args.resume_from:
        (root / "resume.md").write_text(
            "# Resume Notes\n\n"
            "## Recovery checkpoint\n"
            f"- resumeMode: {args.resume_mode}\n"
            f"- resumeFrom: {args.resume_from}\n"
            f"- latestChapterIndex: {args.latest_chapter_index}\n"
            f"- nextChapter: {chapter_number}\n"
            "- lastStableSentenceOrBeat: \n"
            "- knownCanonFacts: []\n"
            "- unknownsThatMustNotBeInvented: []\n"
            f"- partialDraftSource: {args.partial_draft}\n"
            "- nextAction: continue recovery\n"
            "- userConfirmationRequired: yes\n",
            encoding="utf-8",
        )

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
