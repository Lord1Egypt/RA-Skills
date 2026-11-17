#!/usr/bin/env python3
"""Build an iA Presenter bundle (.iapresenter) from a Markdown file.

Usage:
  new_deck.py SOURCE.md "OUT.iapresenter" [--theme NAME] [--preset NAME]
              [--assets DIR ...] [--convert-images] [--force] [--open]

- SOURCE.md is copied to OUT.iapresenter/text.md
- info.json is written with the theme ("template") and preset
- every "/assets/<file>" referenced in the deck is looked up in the --assets dirs
  (and next to SOURCE.md) and copied into OUT.iapresenter/assets/
- --convert-images rewrites classic "![alt](path)" images into content blocks
- --force overwrites an existing bundle's text.md / info.json (assets are merged)
- --open opens the result in iA Presenter (macOS)

Theme names are lowercased automatically ("New York" -> "new york").
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ASSET_RE = re.compile(r"^/assets/(.+?)\s*$", re.M)
MD_IMAGE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<path>[^)\s]+)(?:\s+\"[^\"]*\")?\)\s*$", re.M)


def find_file(name, search_dirs):
    for d in search_dirs:
        cand = os.path.join(d, name)
        if os.path.isfile(cand):
            return cand
    return None


def convert_images(text, search_dirs, copies):
    def repl(m):
        path = m.group("path")
        alt = m.group("alt").strip()
        if path.startswith(("http://", "https://")):
            block = path
        else:
            local = path
            if local.startswith("/assets/"):
                local = local[len("/assets/"):]
            src = find_file(local, search_dirs) or find_file(os.path.basename(local), search_dirs)
            base = os.path.basename(local)
            if src:
                copies[base] = src
            block = "/assets/" + base
        if alt:
            block += "\ntitle: " + alt
        return block
    return MD_IMAGE_RE.sub(repl, text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--theme", default=None, help='theme name, e.g. "tokyo", "new york", "helvetica"')
    ap.add_argument("--preset", default="Default")
    ap.add_argument("--assets", action="append", default=[], help="directory to search for /assets/ files (repeatable)")
    ap.add_argument("--convert-images", action="store_true", help="rewrite ![alt](path) into content blocks")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--open", action="store_true", help="open in iA Presenter when done")
    args = ap.parse_args()

    src = os.path.abspath(args.source)
    if not os.path.isfile(src):
        sys.exit(f"error: source not found: {src}")
    out = os.path.abspath(args.out)
    if not out.endswith(".iapresenter"):
        out += ".iapresenter"

    exists = os.path.isdir(out)
    if exists and not args.force:
        sys.exit(f"error: {out} exists (use --force to overwrite text.md/info.json)")
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)

    with open(src, encoding="utf-8") as f:
        text = f.read()
    if not text.endswith("\n"):
        text += "\n"

    search_dirs = [os.path.abspath(d) for d in args.assets] + [os.path.dirname(src), os.path.join(os.path.dirname(src), "assets")]
    copies = {}
    if args.convert_images:
        text = convert_images(text, search_dirs, copies)

    for name in ASSET_RE.findall(text):
        name = name.strip()
        if name in copies:
            continue
        found = find_file(name, search_dirs)
        if found:
            copies[name] = found

    missing = []
    for name in sorted(set(ASSET_RE.findall(text))):
        name = name.strip()
        dst = os.path.join(out, "assets", name)
        if name in copies:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.abspath(copies[name]) != os.path.abspath(dst):
                shutil.copy2(copies[name], dst)
        elif not os.path.isfile(dst):
            missing.append(name)

    with open(os.path.join(out, "text.md"), "w", encoding="utf-8") as f:
        f.write(text)

    info_path = os.path.join(out, "info.json")
    info = {}
    if exists and os.path.isfile(info_path):
        try:
            with open(info_path, encoding="utf-8") as f:
                info = json.load(f)
        except Exception:
            info = {}
    info.setdefault("type", "net.daringfireball.markdown")
    info.setdefault("creatorIdentifier", "net.ia.presenter")
    info.setdefault("version", 2)
    info.setdefault("transient", False)
    block = info.setdefault("net.ia.presenter", {})
    if args.theme:
        block["template"] = args.theme.strip().lower()
        block["preset"] = args.preset
    elif "template" not in block:
        block["template"] = "helvetica"
        block["preset"] = args.preset
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
        f.write("\n")

    slides = len([l for l in text.splitlines() if l.strip() == "---"]) + 1
    print(f"wrote {out}")
    print(f"  slides: {slides}   theme: {block.get('template')}   preset: {block.get('preset')}")
    print(f"  assets copied: {len(copies)}")
    if missing:
        print("  MISSING assets (referenced but not found):")
        for m in missing:
            print("   - /assets/" + m)
    if args.open:
        if sys.platform == "darwin":
            subprocess.run(["open", "-a", "iA Presenter", out])
        else:
            print("  --open ignored: not macOS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
