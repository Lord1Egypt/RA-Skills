#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

SEARCH_ROOTS = [
    Path.home() / ".npm-global" / "lib" / "node_modules",
    Path("/usr/lib/node_modules"),
    Path("/usr/local/lib/node_modules"),
]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def resolve_active_install() -> Path:
    openclaw_bin = run(["bash", "-lc", "which openclaw"])
    resolved = run(["bash", "-lc", f'readlink -f "{openclaw_bin}"'])
    return Path(resolved).resolve().parent


def find_asset(kind: str) -> Path:
    active = resolve_active_install()
    base = active.parent / "dist" / "control-ui" / "assets"
    if kind == "js":
        matches = sorted(base.glob("index-*.js"))
    else:
        matches = sorted(base.glob("index-*.css"))
    if not matches:
        raise FileNotFoundError(f"No {kind} bundle found under {base}")
    return matches[0]


def extract_css_block(css_text: str, selector: str) -> Optional[str]:
    pattern = re.escape(selector) + r"\{[^}]*\}"
    m = re.search(pattern, css_text)
    return m.group(0) if m else None


def extract_js_snippets(js_text: str, theme_id: str) -> dict[str, Optional[str]]:
    snippets: dict[str, Optional[str]] = {
        "allowed_set": None,
        "alias_map": None,
        "resolver": None,
        "theme_card": None,
    }

    allowed = re.search(r"new Set\(\[[^\]]*`" + re.escape(theme_id) + r"`[^\]]*\]\)", js_text)
    if allowed:
        snippets["allowed_set"] = allowed.group(0)

    alias = re.search(r"\{[^{}]*" + re.escape(theme_id) + r":\{theme:`" + re.escape(theme_id) + r"`,mode:`dark`\}[^{}]*\}", js_text)
    if alias:
        snippets["alias_map"] = alias.group(0)

    resolver = re.search(re.escape(f"e===`{theme_id}`?n===`light`?`{theme_id}-light`:`{theme_id}`"), js_text)
    if resolver:
        start = max(0, resolver.start() - 600)
        end = min(len(js_text), resolver.end() + 1200)
        snippets["resolver"] = js_text[start:end]

    card = re.search(r"\{id:`" + re.escape(theme_id) + r"`,label:`[^`]+`,description:`[^`]+`,icon:[^}]+\}", js_text)
    if card:
        snippets["theme_card"] = card.group(0)

    return snippets


def main() -> None:
    ap = argparse.ArgumentParser(description="Backup an installed OpenClaw custom theme from the live bundle.")
    ap.add_argument("theme_id", help="Theme id, e.g. contrast")
    ap.add_argument("--output-dir", default=str(Path.cwd() / "backups"), help="Base backup directory")
    args = ap.parse_args()

    theme_id = args.theme_id.strip()
    out_base = Path(args.output_dir).expanduser().resolve()
    backup_dir = out_base / f"openclaw-{theme_id}-theme"
    backup_dir.mkdir(parents=True, exist_ok=True)

    js_path = find_asset("js")
    css_path = find_asset("css")
    js_text = js_path.read_text(encoding="utf-8", errors="ignore")
    css_text = css_path.read_text(encoding="utf-8", errors="ignore")

    dark_selector = f":root[data-theme={theme_id}]"
    light_selector = f":root[data-theme={theme_id}-light]"
    dark_block = extract_css_block(css_text, dark_selector)
    light_block = extract_css_block(css_text, light_selector)
    js_snippets = extract_js_snippets(js_text, theme_id)

    (backup_dir / "bundle-js.txt").write_text(js_text, encoding="utf-8")
    (backup_dir / "bundle-css.txt").write_text(css_text, encoding="utf-8")
    if dark_block:
        (backup_dir / f"{theme_id}.dark.css").write_text(dark_block, encoding="utf-8")
    if light_block:
        (backup_dir / f"{theme_id}.light.css").write_text(light_block, encoding="utf-8")
    (backup_dir / "js-snippets.json").write_text(json.dumps(js_snippets, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "theme_id": theme_id,
        "bundle_js": str(js_path),
        "bundle_css": str(css_path),
        "css_dark_found": bool(dark_block),
        "css_light_found": bool(light_block),
        "js_snippets_found": {k: bool(v) for k, v in js_snippets.items()},
        "backup_dir": str(backup_dir),
    }
    (backup_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
