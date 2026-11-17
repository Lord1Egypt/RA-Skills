#!/usr/bin/env python3
"""Scaffold a Neway Commerce OS project from `templates/base`.

This script does exactly one thing: copy the template, substitute the four
placeholder tokens, and print the next steps. It deliberately does NOT invent
product data or a second handoff document — `src/data/products.ts` is the single
source of truth for products, and the handoff notes live in the agent's reply
(see SKILL.md, "Handoff Notes").

Usage
-----
    python scaffold_project.py "<prompt>" --output <dir> [--brand <name>] [--site-name <name>] [--slug <slug>]

Safety
------
An existing target directory is never deleted. It is renamed to
`<slug>.bak-<timestamp>` and the new project is written fresh, so a re-run can
never destroy work that is already on disk.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from datetime import datetime
from pathlib import Path

PLACEHOLDERS = {
    "__SITE_NAME__": "site_name",
    "__BRAND_NAME__": "brand",
    "__SITE_SLUG__": "slug",
    "__PROMPT__": "prompt",
}

# Filler words stripped when guessing a site name from a Latin prompt.
FILLER = {
    "please",
    "help",
    "give",
    "build",
    "make",
    "create",
    "generate",
    "design",
    "start",
    "launch",
    "setup",
    "want",
    "need",
    "a",
    "an",
    "the",
    "me",
    "my",
    "our",
    "for",
    "with",
    "and",
    "of",
    "to",
    "online",
    "web",
    "website",
    "site",
    "store",
    "storefront",
    "shop",
    "ecommerce",
    "marketplace",
    "selling",
    "sell",
}


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def fallback_slug(source: str) -> str:
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:8]
    return f"store-{digest}"


def infer_site_name(prompt: str) -> str:
    cleaned = prompt.strip()
    if not cleaned:
        return "NewayStudio"

    # Latin prompt: drop filler words and keep up to four content words.
    if re.search(r"[A-Za-z]", cleaned):
        head = cleaned.split(":", 1)[0]
        tokens = [w.strip(",.!?;:'\"()") for w in head.split()]
        tokens = [w for w in tokens if w and w.lower() not in FILLER]
        if not tokens:
            tokens = head.split()[:4]
        return " ".join(tokens[:4]).strip() or "NewayStudio"

    # Non-Latin prompt: keep the first punctuation-delimited phrase.
    # Written with escapes so no literal CJK punctuation lives in this file.
    phrase = re.split(r"[\u3000-\u303f\uff00-\uffef,.:;!?]", cleaned)[0].strip()
    return phrase[:16] or "NewayStudio"


def replace_tokens(root: Path, replacements: dict[str, str]) -> int:
    touched = 0
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = content
        for token, value in replacements.items():
            if token in updated:
                updated = updated.replace(token, value)
        if updated != content:
            file_path.write_text(updated, encoding="utf-8")
            touched += 1
    return touched


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Neway Commerce OS project.")
    parser.add_argument("prompt", help="Short product or business prompt.")
    parser.add_argument("--output", required=True, help="Directory that will hold the new project.")
    parser.add_argument("--brand", default="NewayStudio", help="Brand name injected into the project.")
    parser.add_argument("--site-name", default=None, help="Override the derived site name.")
    parser.add_argument("--slug", default=None, help="Override the derived directory slug.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_dir = skill_root / "templates" / "base"
    if not template_dir.exists():
        raise SystemExit(f"Template directory not found: {template_dir}")

    raw_name = args.site_name or infer_site_name(args.prompt)
    site_name = raw_name.strip() or "NewayStudio"
    slug = args.slug or slugify(site_name) or fallback_slug(args.prompt)
    slug = slugify(slug) or fallback_slug(args.prompt)

    output_root = Path(args.output).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_dir = output_root / slug

    backed_up: Path | None = None
    if output_dir.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backed_up = output_dir.with_name(f"{output_dir.name}.bak-{stamp}")
        output_dir.rename(backed_up)

    shutil.copytree(template_dir, output_dir)

    replacements = {
        "__SITE_NAME__": site_name,
        "__BRAND_NAME__": args.brand,
        "__SITE_SLUG__": slug,
        "__PROMPT__": args.prompt,
    }
    touched = replace_tokens(output_dir, replacements)

    print(f"[OK] Project scaffolded at {output_dir}")
    print(f"     site name : {site_name}")
    print(f"     slug      : {slug}")
    print(f"     brand     : {args.brand}")
    print(f"     files with placeholders resolved: {touched}")
    if backed_up:
        print(f"     previous directory preserved at: {backed_up}")
    print()
    print("Next steps:")
    print(f"  1. fill src/data/products.ts, src/components/AIChatWidget.tsx, src/pages/*.tsx")
    print(f"  2. python {skill_root / 'scripts' / 'validate_generated_project.py'} \"{output_dir}\"")
    print(f"  3. cd \"{output_dir}\" && npm install && npm run build")
    print("  Delivery is blocked until step 2 reports RESULT: PASS and step 3 exits 0.")


if __name__ == "__main__":
    main()
