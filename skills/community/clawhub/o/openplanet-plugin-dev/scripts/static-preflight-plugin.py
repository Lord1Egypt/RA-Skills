#!/usr/bin/env python3
"""Generic static pre-flight gate for an Openplanet AngelScript plugin (MP4).

AngelScript has NO offline compiler, and each in-game verification costs a
~60 s kill+relaunch cycle. This catches most hallucinations for free before
you pay for that cycle.

ADAPT THE THREE CONSTANTS BELOW (ROOT, PLUGIN, HANDLE_TYPES) per project.

Checks, per .as file under PLUGIN:
  1. Balanced braces/parens (string literals blanked first).
  2. Every `handle.Member` access resolves in Openplanet4.json, walking the
     `p` parent chain so inherited members do not false-fail.
  3. No MP4-forbidden natives (comments stripped first, so documentation
     mentioning a forbidden call is not flagged).
  4. Icons::X restricted to a verified-safe allowlist.
  5. Every g_modules.Register(XModule()) has a matching class definition.

Exit 0 = PASS. Report it as "static pre-flight PASS -- in-game compile still
required", NEVER as "verified working".

ALWAYS prove the gate is non-vacuous: copy the tree to a temp sandbox, rewrite
ROOT, inject `UI::BeginTable("x", 2)` into one module, and assert this script
then FAILS. A pre-flight that passes everything is worse than none.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --- ADAPT PER PROJECT -------------------------------------------------------
ROOT = Path(r"C:\Users\tomekdot\Openplanet4")
PLUGIN = ROOT / "Plugins" / "mp-trainer"
REFL = ROOT / "Openplanet4.json"
MODULE_BASE = "TRModule"  # base class modules derive from

# handle expression -> (reflection namespace, class). Trailing "." means the
# prefix already includes the dot (e.g. a local named `s`).
HANDLE_TYPES = {
    "ctx.Player": ("TrackMania", "CTrackManiaPlayer"),
    "ctx.Script": ("TrackMania", "CTrackManiaScriptPlayer"),
    "ctx.Map": ("Game", "CGameCtnChallenge"),
    "ctx.App": ("Game", "CGameCtnApp"),
    "ctx.Playground": ("Game", "CGamePlayground"),
    "s.": ("TrackMania", "CTrackManiaScriptPlayer"),
    "b.": ("Game", "CGameCtnBlock"),
    "it.": ("Game", "CGameCtnAnchoredObject"),
    "wp.": ("GameData", "CGameWaypointSpecialProperty"),
}
# -----------------------------------------------------------------------------

SAFE_ICONS = {
    "Wrench", "Cube", "Cubes", "Th", "PaintBrush", "History", "MousePointer",
    "Clipboard", "VideoCamera", "Eye", "Crosshairs", "ArrowDown", "MapMarker",
    "SearchPlus", "SearchMinus", "Eraser", "Plus", "FolderOpen", "List",
    "FileCodeO", "Clock", "Exchange", "Leaf", "Repeat", "Refresh", "Undo",
    "Gamepad", "Tree", "Random", "Search", "Trash", "Sitemap", "Retweet",
    "PuzzlePiece", "Play", "Pencil", "Link", "Flask", "FlagCheckered",
    "Check", "Bolt", "BarChart", "ArrowsAlt",
}

FORBIDDEN = [
    (r"\bUI::BeginTable\b", "unreliable on MP4 -> BeginChild+SameLine"),
    (r"\bUI::Columns\b", "absent on MP4"),
    (r"\bUI::NextColumn\b", "absent on MP4"),
    (r"\bUI::InputInt3\b", "absent on MP4 -> three UI::InputInt"),
    (r"\bUI::ListBox\b", "absent on this OP build -> BeginCombo"),
    (r"\.ToLower\s*\(", "string::ToLower absent -> byte-compare helper"),
    (r"\bchar\s*\(", "char() casts unsupported on MP4"),
    (r"\bUI::CollapsingHeader\s*\([^)]*,", "takes a single string arg on MP4"),
    (r"\bIO::WriteFile\b", "does not exist -> Json::ToFile"),
    (r"\bIO::CreateDirectory\b", "use IO::CreateFolder"),
    (r"\btostring\s*\(\s*[a-z_]\w*\s*\)", "tostring(uint) ambiguous -> Text::Format(\"%d\", int(v))"),
]


def strip_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//[^\n]*", "", src)


def load_members(refl: dict, ns: str, cls: str) -> set[str]:
    node = refl["ns"].get(ns, {}).get(cls)
    if node is None:
        return set()
    out = {m["n"] for m in node.get("m", [])}
    parent, guard = node.get("p"), 0
    while parent and guard < 12:
        guard += 1
        found = None
        for _pns, pmap in refl["ns"].items():
            if isinstance(pmap, dict) and parent in pmap:
                found = pmap[parent]
                break
        if found is None:
            break
        out |= {m["n"] for m in found.get("m", [])}
        parent = found.get("p")
    return out


def check_balance(name: str, src: str, errs: list[str]) -> None:
    stripped = re.sub(r'"(?:[^"\\]|\\.)*"', '""', src)
    for open_c, close_c, label in (("{", "}", "braces"), ("(", ")", "parens")):
        delta = stripped.count(open_c) - stripped.count(close_c)
        if delta:
            errs.append(f"{name}: unbalanced {label} (delta={delta})")


def main() -> int:
    refl = json.loads(REFL.read_text(encoding="utf-8", errors="replace"))
    files = sorted(PLUGIN.rglob("*.as"))
    if not files:
        print("no .as files under", PLUGIN)
        return 1

    errs: list[str] = []
    warns: list[str] = []
    checked = 0
    sources: dict[Path, str] = {}

    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        sources[f] = raw
        code = strip_comments(raw)

        check_balance(f.name, code, errs)

        for pat, msg in FORBIDDEN:
            for m in re.finditer(pat, code):
                line = code[: m.start()].count("\n") + 1
                errs.append(f"{f.name}:{line}: FORBIDDEN {m.group(0)} -- {msg}")

        for m in re.finditer(r"Icons::(\w+)", code):
            if m.group(1) not in SAFE_ICONS:
                errs.append(f"{f.name}: Icons::{m.group(1)} not in verified-safe list")

        for prefix, (ns, cls) in HANDLE_TYPES.items():
            members = load_members(refl, ns, cls)
            if not members:
                warns.append(f"reflection class {ns}.{cls} not found")
                continue
            esc = re.escape(prefix)
            # CRITICAL: the (?<![\w.]) guard stops `s.` matching the tail of
            # `m_modules.Length` and emitting dozens of phantom errors.
            pat = r"(?<![\w.])" + esc + (r"(\w+)" if prefix.endswith(".") else r"\.(\w+)")
            for m in re.finditer(pat, code):
                name = m.group(1)
                checked += 1
                if name not in members:
                    line = code[: m.start()].count("\n") + 1
                    errs.append(f"{f.name}:{line}: {prefix}{name} NOT a member of {cls}")

    main_as = PLUGIN / "src" / "Main.as"
    registered: set[str] = set()
    if main_as.is_file():
        registered = set(re.findall(
            r"g_modules\.Register\((\w+)\(\)\)",
            strip_comments(main_as.read_text(encoding="utf-8")),
        ))
    defined: set[str] = set()
    for raw in sources.values():
        defined |= set(re.findall(rf"class\s+(\w+)\s*:\s*{MODULE_BASE}", strip_comments(raw)))
    missing = registered - defined
    if missing:
        errs.append(f"Main.as registers undefined modules: {sorted(missing)}")

    print(f"files scanned:       {len(files)}")
    print(f"member refs checked: {checked}")
    print(f"modules registered:  {sorted(registered)}")
    print(f"modules defined:     {sorted(defined)}")
    if checked < 20:
        warns.append(f"only {checked} member refs checked -- HANDLE_TYPES probably too narrow")
    if warns:
        print("\nWARNINGS:")
        for w in warns:
            print("  -", w)
    if errs:
        print("\nERRORS:")
        for e in errs:
            print("  -", e)
        print("\nVERDICT: FAIL")
        return 1
    print("\nVERDICT: PASS (static pre-flight; in-game compile still required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
