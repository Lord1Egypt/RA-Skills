#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


DEFAULT_PRODUCTS = [
    {
        "id": "ui-kit-pro",
        "name": "UI Kit Pro",
        "price": 79,
        "category": "design",
        "tagline": "Premium components and sections for fast launches.",
    },
    {
        "id": "ai-workflow-pack",
        "name": "AI Workflow Pack",
        "price": 129,
        "category": "ai",
        "tagline": "Reusable prompts, automations, and workflow recipes.",
    },
    {
        "id": "creator-launch-box",
        "name": "Creator Launch Box",
        "price": 149,
        "category": "growth",
        "tagline": "Landing pages, funnel copy, and launch assets.",
    },
]


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "neway-site"


def infer_site_name(prompt: str) -> str:
    cleaned = prompt.strip()
    if not cleaned:
        return "NewayStudio"
    if len(cleaned) <= 60 and " " not in cleaned:
        return cleaned
    if ":" in cleaned:
        cleaned = cleaned.split(":", 1)[0]
    words = cleaned.split()
    return " ".join(words[:4]).strip() or "NewayStudio"


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_tokens(root: Path, replacements: dict[str, str]) -> None:
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for key, value in replacements.items():
            content = content.replace(key, value)
        file_path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a Neway Commerce OS project from the base template."
    )
    parser.add_argument("prompt", help="Short product or business prompt.")
    parser.add_argument(
        "--output",
        required=True,
        help="Directory where the generated project should be written.",
    )
    parser.add_argument(
        "--brand",
        default="NewayStudio",
        help="Brand name to inject into the project.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_dir = skill_root / "templates" / "base"
    if not template_dir.exists():
        raise SystemExit(f"Template directory not found: {template_dir}")

    site_name = infer_site_name(args.prompt)
    slug = slugify(site_name)
    output_dir = Path(args.output).resolve() / slug

    if output_dir.exists():
        shutil.rmtree(output_dir)

    shutil.copytree(template_dir, output_dir)

    replacements = {
        "__SITE_NAME__": site_name,
        "__BRAND_NAME__": args.brand,
        "__SITE_SLUG__": slug,
        "__PROMPT__": args.prompt,
    }
    replace_tokens(output_dir, replacements)

    products_path = output_dir / "src" / "data" / "products.json"
    products_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(products_path, DEFAULT_PRODUCTS)

    brief_path = output_dir / "NEWAY_BRIEF.md"
    brief_path.write_text(
        "\n".join(
            [
                f"# {site_name}",
                "",
                f"Brand: {args.brand}",
                f"Prompt: {args.prompt}",
                "",
                "## Generated defaults",
                "- Multi-product digital storefront",
                "- AI shopping concierge",
                "- Mock-to-stripe checkout path",
                "- Account and admin views",
                "- EdgeOne deployment files",
                "",
                "## Implementation note",
                "This scaffold is demo-ready as a structure and UI shell.",
                "Production integrations still need to be connected where mock or stub logic is present.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"[OK] Generated project at {output_dir}")


if __name__ == "__main__":
    main()
