#!/usr/bin/env python3
"""Generate a starter context pack for a Novel Forge project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_state_snapshot(
    title: str,
    genre: str,
    audience: str,
    target_chapters: int,
    chapter_min: int,
    chapter_max: int,
    resume_from: str = "",
    resume_mode: str = "new",
    latest_chapter_index: int = 0,
    partial_draft: str = "",
    execution_mode: str = "multi-agent",
) -> dict:
    chapter_number = max(1, latest_chapter_index + 1)
    return {
        "project": {
            "title": title,
            "genre": genre,
            "audience": audience,
            "targetChapters": target_chapters,
            "chapterWordRange": [chapter_min, chapter_max],
            "status": "draft",
            "executionMode": execution_mode,
            "premise": "",
            "tabooList": [],
            "bootstrapLocked": False,
            "latestChapterIndex": latest_chapter_index,
            "lastCheckpoint": "",
            "resumeFrom": resume_from,
            "resumeMode": resume_mode,
        },
        "workflow": {
            "step": "idle",
            "chapterIndex": latest_chapter_index,
            "nextChapterIndex": chapter_number,
        },
        "recoveryCheckpoint": {
            "resumeMode": resume_mode,
            "lastStableSentenceOrBeat": "",
            "knownCanonFacts": [],
            "unknownsThatMustNotBeInvented": [],
            "partialDraftSource": partial_draft,
            "nextAction": "continue recovery" if resume_from else "start project bootstrap",
            "userConfirmationRequired": bool(resume_from),
        },
        "chapter": {
            "currentChapterIndex": latest_chapter_index,
            "nextChapterIndex": chapter_number,
        },
    }


def build_pack(
    title: str,
    genre: str,
    audience: str,
    target_chapters: int,
    chapter_min: int,
    chapter_max: int,
    resume_from: str = "",
    resume_mode: str = "new",
    latest_chapter_index: int = 0,
    partial_draft: str = "",
    execution_mode: str = "multi-agent",
    models: dict | None = None,
) -> dict:
    state_current = build_state_snapshot(
        title,
        genre,
        audience,
        target_chapters,
        chapter_min,
        chapter_max,
        resume_from=resume_from,
        resume_mode=resume_mode,
        latest_chapter_index=latest_chapter_index,
        partial_draft=partial_draft,
        execution_mode=execution_mode,
    )
    return {
        "project": {
            "title": title,
            "genre": genre,
            "audience": audience,
            "targetChapters": target_chapters,
            "chapterWordRange": [chapter_min, chapter_max],
            "status": "draft",
            "executionMode": execution_mode,
            "premise": "",
            "tabooList": [],
            "bootstrapLocked": False,
            "latestChapterIndex": latest_chapter_index,
            "lastCheckpoint": "",
            "resumeFrom": resume_from,
            "resumeMode": resume_mode,
        },
        "models": models or {
            "orchestrator": "",
            "worldbuilding": "n/a",
            "characters": "n/a",
            "outline": "n/a",
            "style": "n/a",
            "writer": "n/a",
            "reviewer": "n/a",
            "memory": "n/a",
        },
        "canon": {
            "hard": [],
            "soft": [],
            "world": {},
            "characters": [],
            "timeline": [],
            "factions": [],
        },
        "planning": {
            "outline": {},
            "volumes": [],
            "chapters": [],
            "currentBeat": {},
            "partialDrafts": [],
        },
        "style": {
            "candidates": [],
            "selected": "",
            "rules": [],
        },
        "memory": {
            "fullSummary": "",
            "recentSummaries": [],
            "openLoops": [],
            "characterStates": {},
            "foreshadowing": [],
            "recoverySummary": "",
            "lastKnownState": partial_draft,
        },
        "state": {
            "current": state_current,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="Untitled Novel")
    parser.add_argument("--genre", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--target-chapters", type=int, default=50)
    parser.add_argument("--chapter-min", type=int, default=2000)
    parser.add_argument("--chapter-max", type=int, default=4000)
    parser.add_argument("--resume-from", default="")
    parser.add_argument("--resume-mode", default="new", choices=["new", "continue", "truncated", "checkpoint"])
    parser.add_argument("--latest-chapter-index", type=int, default=0)
    parser.add_argument("--partial-draft", default="")
    parser.add_argument("--execution-mode", default="multi-agent", choices=["single-agent", "multi-agent"])
    parser.add_argument("--models-json", default="")
    parser.add_argument("--out", help="Write JSON to this path instead of stdout")
    args = parser.parse_args()

    models = json.loads(args.models_json) if args.models_json else None
    pack = build_pack(
        args.title,
        args.genre,
        args.audience,
        args.target_chapters,
        args.chapter_min,
        args.chapter_max,
        resume_from=args.resume_from,
        resume_mode=args.resume_mode,
        latest_chapter_index=args.latest_chapter_index,
        partial_draft=args.partial_draft,
        execution_mode=args.execution_mode,
        models=models,
    )
    text = json.dumps(pack, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
