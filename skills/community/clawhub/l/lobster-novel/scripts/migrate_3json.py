#!/usr/bin/env python3
"""
migrate_3json.py — V5–V10 小说项目 3JSON → story-state.json 一键迁移

读取 project_dir 下的 chapter_appearances.json / character_roster.json / hooks.json，
自动检测版本格式，生成统一的 story-state.json。

Usage:
    python3 migrate_3json.py <project_dir>
    python3 migrate_3json.py /path/to/novels/V10_灰港镇的异客
    python3 migrate_3json.py --all          # 迁移 novels/ 下所有项目
    python3 migrate_3json.py --check         # 只检查不写入
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

# ── 确保能找到 core/ ──────────────────────────────────────────
_base = Path(__file__).resolve().parent.parent
for p in [str(_base), str(_base / "core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from core.story_state import StoryState, CharacterState, HookState, ChapterRecord, StrandState


# ═══════════════════════════════════════════════════════════════
#  Chapter number parsing helpers
# ═══════════════════════════════════════════════════════════════

CH_RE = re.compile(r"ch(\d+)", re.IGNORECASE)


def _parse_chapter_num(raw: Any) -> int:
    """Parse chapter number from various formats:
    - int: 1, 20
    - str: "Ch001", "v10ch001", "ch1"
    - str: "V5Ch001"
    """
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        m = CH_RE.search(raw)
        if m:
            return int(m.group(1))
        # Try bare number
        try:
            return int(raw)
        except ValueError:
            pass
    return 0


def _clean_title(raw: str) -> str:
    """Remove volume/chapter prefix from title like '[V5Ch001] 标题' → '标题'."""
    return re.sub(r"^\[?[Vv]\d+[Cc][Hh]\d+\]?\s*", "", raw).strip()


def _name_to_id(name: str) -> str:
    """Convert character name to a stable ID."""
    safe = name.strip().replace("·", "_").replace(" ", "_")
    return f"char_{safe}"


# ═══════════════════════════════════════════════════════════════
#  Format detectors & loaders
# ═══════════════════════════════════════════════════════════════


def _detect_format(data: Any, filename: str) -> str:
    """Detect which format the data uses."""
    if filename == "chapter_appearances.json":
        if isinstance(data, list):
            return "list_v5"  # V5 style: [{chapter, characters, key_events}]
        if isinstance(data, dict):
            # V10: {volume_key: {Ch001: {title, characters: {...}}}}
            for k, v in data.items():
                if isinstance(v, dict) and any(c.startswith("Ch") for c in v):
                    return "dict_v10"
                if isinstance(v, list):
                    # Could be V9 style: {entries: [...], v9ch031: [...]}
                    pass  # falls through to dict_unknown
            # V9: {entries: [{chapter, title, characters, key_events}], ...}
            if "entries" in data:
                return "dict_v9"
            # V8 style: {characters: [...]}
            if "characters" in data and isinstance(data.get("characters"), list):
                return "list_v8"
            return "dict_unknown"

    if filename == "character_roster.json":
        if isinstance(data, list):
            return "list"
        if isinstance(data, dict):
            if "characters" in data:
                return "dict_v10"  # V10: {characters: {...}, carry_over: {...}}
            return "dict_v5"  # V5/V9: {char_name: {...}}
        return "unknown"

    if filename == "hooks.json":
        if isinstance(data, list):
            return "list"  # Both V5+V10 style: list
        if isinstance(data, dict):
            return "dict"
        return "unknown"

    return "unknown"


# ═══════════════════════════════════════════════════════════════
#  Normalizers: load raw data → normalized internal structures
# ═══════════════════════════════════════════════════════════════


def _normalize_characters(raw: dict | list, fmt: str) -> dict[str, dict[str, Any]]:
    """Normalize character_roster → {id: {name, role, first_appearance, last_appearance, status, state, key_items}}."""
    result: dict[str, dict[str, Any]] = {}

    if fmt == "dict_v10":
        # V10: {characters: {name: {...}}, ...}
        chars = raw.get("characters", {})
    elif fmt in ("dict_v5", "dict_v9"):
        chars = raw
    elif fmt == "list":
        chars = {}
        for entry in raw:
            name = entry.get("name", entry.get("id", ""))
            chars[name] = entry
    else:
        chars = raw if isinstance(raw, dict) else {}

    for name, info in chars.items():
        if not isinstance(info, dict):
            continue
        cid = _name_to_id(name)
        role = info.get("role", "配角")
        raw_first = info.get("first_appearance", 0)
        raw_last = info.get("last_appearance", 0)
        first = _parse_chapter_num(raw_first) if raw_first else 0
        last = _parse_chapter_num(raw_last) if raw_last else first

        state = info.get("state", info.get("description", ""))
        if isinstance(state, dict):
            state = str(state)
        key_items = info.get("key_items", [])
        if not isinstance(key_items, list):
            key_items = []

        result[cid] = {
            "id": cid,
            "name": name,
            "role": {"主角": "主角", "双主角": "主角", "主角同伴": "核心角色",
                     "配角": "配角", "异客": "异客",
                     "protagonist": "主角", "mentor": "核心角色",
                     "supporting": "配角"}.get(role, "配角"),
            "first_appearance": max(first, 0),
            "last_appearance": max(last, 0),
            "status": info.get("status", "active"),
            "state": state[:200] if state else "",
            "key_items": key_items[:10],
        }

    return result


def _normalize_chapters(raw: dict | list, fmt: str) -> dict[int, dict[str, Any]]:
    """Normalize chapter_appearances → {num: {number, title, word_count, scene, characters_present, key_events}}."""
    result: dict[int, dict[str, Any]] = {}
    entries: list[dict] = []

    if fmt == "list_v5":
        raw_entries = raw if isinstance(raw, list) else []
        for e in raw_entries:
            num = e.get("chapter", 0)
            if isinstance(num, str):
                num = _parse_chapter_num(num)
            if num <= 0:
                continue
            chars = e.get("characters", [])
            if isinstance(chars, dict):
                chars = list(chars.keys())
            entries.append({
                "number": num,
                "title": _clean_title(e.get("title", "")),
                "word_count": e.get("word_count", 0),
                "scene": e.get("scene", e.get("locations", [None])[0] if isinstance(e.get("locations"), list) else ""),
                "characters_present": chars,
                "key_events": e.get("key_events", []),
            })
    elif fmt == "list_v8":
        # list_v8: {characters: [...], other keys} — 不含章节级数据，跳过
        return result
    elif fmt == "dict_v9":
        raw_entries = raw.get("entries", []) if isinstance(raw, dict) else []
        for e in raw_entries:
            num = _parse_chapter_num(e.get("chapter", ""))
            if num <= 0:
                continue
            chars = e.get("characters", [])
            if isinstance(chars, dict):
                chars = list(chars.keys())
            entries.append({
                "number": num,
                "title": _clean_title(e.get("title", "")),
                "word_count": e.get("word_count", 0),
                "scene": e.get("scene", ""),
                "characters_present": chars,
                "key_events": e.get("key_events", []),
            })
    elif fmt == "dict_v10":
        # {volume_key: {Ch001: {...}, ...}}
        for volume_key, chapters_dict in raw.items():
            if not isinstance(chapters_dict, dict):
                continue
            for ch_key, ch_data in chapters_dict.items():
                num = _parse_chapter_num(ch_key)
                if num <= 0:
                    continue
                title = _clean_title(ch_data.get("title", ch_data.get("chapter_title", "")))
                chars_raw = ch_data.get("characters", [])
                if isinstance(chars_raw, dict):
                    chars = list(chars_raw.keys())
                elif isinstance(chars_raw, list):
                    chars = chars_raw
                else:
                    chars = []
                events = ch_data.get("key_events", [])
                scene = ch_data.get("scene", "")
                if isinstance(scene, dict):
                    # Per-character scenes — take first
                    scenes = [s for s in scene.values() if isinstance(s, str)]
                    scene = scenes[0] if scenes else ""
                entries.append({
                    "number": num,
                    "title": title,
                    "word_count": ch_data.get("word_count", 0),
                    "scene": scene,
                    "characters_present": chars,
                    "key_events": events if isinstance(events, list) else [],
                })
    elif fmt == "dict_unknown":
        if isinstance(raw, dict):
            for k, v in raw.items():
                if isinstance(v, dict) and "characters" in v:
                    entries.append(_normalize_entry_guess(k, v))
                elif isinstance(v, list):
                    # {ch031: [char_names]}
                    num = _parse_chapter_num(k)
                    if num > 0:
                        entries.append({
                            "number": num, "title": "", "word_count": 0,
                            "scene": "", "characters_present": v, "key_events": [],
                        })

    for entry in entries:
        num = entry.get("number", 0)
        if num <= 0:
            continue
        result[num] = {
            "number": num,
            "title": entry.get("title", ""),
            "word_count": entry.get("word_count", 0),
            "scene": entry.get("scene", ""),
            "characters_present": entry.get("characters_present", []),
            "key_events": entry.get("key_events", []),
        }

    return result


def _normalize_entry_guess(key: str, data: dict) -> dict:
    """Guess chapter entry structure from unknown dict format."""
    num = _parse_chapter_num(key)
    chars = data.get("characters", [])
    if isinstance(chars, dict):
        chars = list(chars.keys())
    return {
        "number": num,
        "title": _clean_title(data.get("title", data.get("chapter_title", ""))),
        "word_count": data.get("word_count", 0),
        "scene": data.get("scene", ""),
        "characters_present": chars,
        "key_events": data.get("key_events", []),
    }


def _normalize_hooks(raw: list | dict, fmt: str) -> list[dict[str, Any]]:
    """Normalize hooks → [{id, description, type, chapter, status, expected_payoff}]."""
    result: list[dict[str, Any]] = []
    entries: list[dict] = []

    if fmt == "list":
        entries = raw if isinstance(raw, list) else []
    elif fmt == "dict":
        # Try nested hooks key first (卷六 format: {hooks: [...], metadata})  
        if isinstance(raw, dict) and "hooks" in raw and isinstance(raw["hooks"], list):
            entries = raw["hooks"]
        else:
            entries = [v for v in raw.values() if isinstance(v, dict)]

    for h in entries:
        if not isinstance(h, dict):
            continue

        # Detect V9 format: {hook, desc, planted, payoff, status}
        hook_desc = (
            h.get("description", h.get("desc", h.get("hook", "")))
        )

        # Unique-ish ID
        hid = h.get("id", "")
        if not hid:
            # Use md5 of description for deterministic ID
            import hashlib
            hid = f"migrated_hook_{hashlib.md5(hook_desc.encode('utf-8')).hexdigest()[:10]}"

        # Chapter
        ch_raw = h.get("chapter", h.get("planted", h.get("planted_chapter", 0)))
        chapter = _parse_chapter_num(ch_raw)

        # Type
        htype = h.get("type", h.get("tag", "悬念"))

        # Status
        raw_status = h.get("status", "活跃")
        status_map = {"active": "活跃", "兑现": "兑现", "resolved": "兑现",
                      "open": "活跃", "pending": "活跃", "evolved": "活跃",
                      "completed": "兑现", "done": "兑现", "finished": "兑现"}
        status = status_map.get(raw_status.lower(), "活跃") if isinstance(raw_status, str) else "活跃"

        # Expected payoff
        payoff = h.get("expected_payoff", h.get("payoff", h.get("expected_payoff_chapter", "")))

        result.append({
            "id": hid,
            "description": hook_desc[:300],
            "type": htype,
            "chapter_created": max(chapter, 0),
            "chapter_resolved": None,
            "status": status,
            "expected_payoff": str(payoff) if payoff else "",
        })

    return result


# ═══════════════════════════════════════════════════════════════
#  Main migration
# ═══════════════════════════════════════════════════════════════


def migrate_project(project_dir: str | Path, dry_run: bool = False) -> dict[str, Any]:
    """
    Migrate 3JSON → story-state.json for one project directory.

    Returns a report dict with counts and any warnings.
    """
    project = Path(project_dir)
    report: dict[str, Any] = {
        "project": project.name,
        "dry_run": dry_run,
        "warnings": [],
        "characters_migrated": 0,
        "chapters_migrated": 0,
        "hooks_migrated": 0,
        "notes": "",
    }

    # Load bible.json for novel title/volume
    title = project.name
    bible_path = project / "bible.json"
    if bible_path.exists():
        try:
            bible = json.load(bible_path.read_text(encoding="utf-8"))
            title = bible.get("title", title)
        except (json.JSONDecodeError, OSError):
            pass

    # ── Load chapter_appearances.json ─────────────────────────
    chapters: dict[int, dict] = {}
    ca_path = project / "chapter_appearances.json"
    if ca_path.exists():
        try:
            raw_ca = json.loads(ca_path.read_text(encoding="utf-8"))
            ca_fmt = _detect_format(raw_ca, "chapter_appearances.json")
            chapters = _normalize_chapters(raw_ca, ca_fmt)
            report["chapter_format"] = ca_fmt
        except (json.JSONDecodeError, OSError) as e:
            report["warnings"].append(f"chapter_appearances.json: {e}")

    # ── Load character_roster.json ────────────────────────────
    characters: dict[str, dict] = {}
    cr_path = project / "character_roster.json"
    if cr_path.exists():
        try:
            raw_cr = json.loads(cr_path.read_text(encoding="utf-8"))
            cr_fmt = _detect_format(raw_cr, "character_roster.json")
            characters = _normalize_characters(raw_cr, cr_fmt)
            report["character_format"] = cr_fmt
        except (json.JSONDecodeError, OSError) as e:
            report["warnings"].append(f"character_roster.json: {e}")

    # ── Load hooks.json ───────────────────────────────────────
    hooks: list[dict] = []
    hk_path = project / "hooks.json"
    if hk_path.exists():
        try:
            raw_hk = json.loads(hk_path.read_text(encoding="utf-8"))
            hk_fmt = _detect_format(raw_hk, "hooks.json")
            hooks = _normalize_hooks(raw_hk, hk_fmt)
            report["hook_format"] = hk_fmt
        except (json.JSONDecodeError, OSError) as e:
            report["warnings"].append(f"hooks.json: {e}")

    # ── Build StoryState ──────────────────────────────────────
    state = StoryState(novel_title=title, volume=project.name)

    # Characters
    for cid, c in characters.items():
        state.characters[cid] = CharacterState(
            id=c["id"],
            name=c["name"],
            role=c["role"],
            first_appearance=c["first_appearance"],
            last_appearance=c["last_appearance"],
            status=c["status"],
            state=c["state"],
            key_items=c["key_items"],
        )
    report["characters_migrated"] = len(characters)

    # Chapters
    for num in sorted(chapters):
        ch = chapters[num]
        rec = ChapterRecord(
            number=num,
            title=ch["title"],
            word_count=ch["word_count"],
            scene=ch["scene"],
            characters_present=ch["characters_present"],
            key_events=ch["key_events"],
            strand_weights={},
        )
        state.chapters[num] = rec
    report["chapters_migrated"] = len(chapters)
    if chapters:
        report["notes"] += f"章节范围 Ch{min(chapters)}–Ch{max(chapters)}"

    # Hooks
    for h in hooks:
        hid = h["id"]
        state.hooks[hid] = HookState(
            id=hid,
            description=h["description"],
            type=h["type"],
            chapter_created=h["chapter_created"],
            chapter_resolved=h.get("chapter_resolved"),
            status=h["status"],
            expected_payoff=h["expected_payoff"],
        )
    report["hooks_migrated"] = len(hooks)

    # Strands (rough estimate — real strand weights should be set after migration)
    if chapters:
        # Count chapters with key_events (quest-significant) vs scene (non-quest)
        quest_count = sum(1 for ch in chapters.values() if ch.get("key_events"))
        total = max(len(chapters), 1)
        quest_ratio = round(quest_count / total, 2)
        # Divide remaining equally between fire and constellation
        remaining = 1.0 - quest_ratio
        state.strands = StrandState(
            quest_ratio=quest_ratio,
            fire_ratio=round(remaining / 2, 2),
            constellation_ratio=round(remaining / 2, 2),
        )

    # ── Save ──────────────────────────────────────────────────
    if not dry_run:
        state.save(str(project))
        report["story_state_path"] = str(project / "story-state.json")
    else:
        report["story_state_path"] = "(dry-run, not written)"

    return report


def check_project(project_dir: str | Path) -> dict[str, Any]:
    """Quick check: which 3JSON files exist and are valid."""
    project = Path(project_dir)
    result = {"project": project.name, "files": {}}
    for fn in ["chapter_appearances.json", "character_roster.json", "hooks.json", "story-state.json"]:
        path = project / fn
        status = "missing"
        if path.exists():
            size = path.stat().st_size
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                fmt = _detect_format(data, fn)
                if isinstance(data, list):
                    count = len(data)
                elif isinstance(data, dict):
                    count = len(data)
                else:
                    count = 0
                status = f"✅ {fmt} ({count} items, {size:,} bytes)"
            except json.JSONDecodeError:
                status = f"❌ invalid JSON ({size:,} bytes)"
        result["files"][fn] = status
    return result


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

def _print_report(report: dict) -> None:
    """Pretty-print migration report."""
    dry = " (DRY RUN)" if report.get("dry_run") else ""
    print(f"\n{'='*50}")
    print(f"  迁移报告: {report['project']}{dry}")
    print(f"{'='*50}")
    print(f"  角色: {report['characters_migrated']} 个")
    print(f"  章节: {report['chapters_migrated']} 个 {report.get('notes', '')}")
    print(f"  伏笔: {report['hooks_migrated']} 个")
    if report.get("chapter_format"):
        print(f"  chapter格式: {report['chapter_format']}")
    if report.get("character_format"):
        print(f"  character格式: {report['character_format']}")
    if report.get("hook_format"):
        print(f"  hook格式: {report['hook_format']}")
    if report["warnings"]:
        print(f"\n  ⚠️ 警告 ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"    - {w}")
    print(f"  输出: {report.get('story_state_path', '(无')}")
    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="3JSON → story-state.json 一键迁移")
    parser.add_argument("project_dir", nargs="?", help="小说项目目录")
    parser.add_argument("--all", action="store_true", help="迁移 novels/ 下所有项目")
    parser.add_argument("--check", action="store_true", help="只检查不写入")
    parser.add_argument("--dry-run", action="store_true", help="预览迁移结果但不写入")
    args = parser.parse_args()

    novels_dir = Path(__file__).resolve().parent.parent.parent.parent / "novels"

    if args.check:
        targets = [novels_dir / d for d in sorted(os.listdir(novels_dir))
                   if (novels_dir / d).is_dir()] if args.all else [Path(args.project_dir)]
        for t in targets:
            r = check_project(t)
            print(f"\n📁 {r['project']}")
            for fn, status in r["files"].items():
                print(f"  {fn:<35} {status}")
        sys.exit(0)

    if args.all:
        targets = sorted([
            novels_dir / d for d in os.listdir(novels_dir)
            if (novels_dir / d).is_dir() and (novels_dir / d / "chapter_appearances.json").exists()
        ])
    else:
        if not args.project_dir:
            parser.print_help()
            sys.exit(1)
        targets = [args.project_dir]

    for t in targets:
        report = migrate_project(t, dry_run=args.dry_run)
        _print_report(report)
