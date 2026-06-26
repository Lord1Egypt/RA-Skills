#!/usr/bin/env python3
"""
Generate a standardized product description brief from a JSON input.

Takes a structured JSON with product details and outputs a markdown brief
that the skill (or a copywriter) can use as a starting point.

Usage:
    python scripts/generate_description_brief.py --in brief.json --out brief.md
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class ProductBrief:
    product_name: str = ""
    category: str = ""
    price: str = ""
    features: List[str] = field(default_factory=list)
    differentiators: List[str] = field(default_factory=list)
    audience: str = ""
    pain_point: str = ""
    tone: str = ""
    keywords: List[str] = field(default_factory=list)
    platform: str = ""
    constraints: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    return [str(value).strip()]


def parse_brief(data: Dict[str, Any]) -> ProductBrief:
    return ProductBrief(
        product_name=str(data.get("product_name", "")).strip(),
        category=str(data.get("category", "")).strip(),
        price=str(data.get("price", "")).strip(),
        features=_as_list(data.get("features")),
        differentiators=_as_list(data.get("differentiators")),
        audience=str(data.get("audience", "")).strip(),
        pain_point=str(data.get("pain_point", "")).strip(),
        tone=str(data.get("tone", "")).strip(),
        keywords=_as_list(data.get("keywords")),
        platform=str(data.get("platform", "")).strip(),
        constraints=_as_list(data.get("constraints")),
        certifications=_as_list(data.get("certifications")),
    )


def to_markdown(brief: ProductBrief) -> str:
    name = brief.product_name or "[Product Name]"

    def bullets(items: List[str], placeholder: str) -> str:
        if not items:
            return f"- {placeholder}\n"
        return "".join(f"- {x}\n" for x in items)

    md = []
    md.append(f"# Product Description Brief: {name}\n")

    md.append("## Snapshot\n")
    md.append(f"- **Product**: {name}\n")
    md.append(f"- **Category**: {brief.category or '[category]'}\n")
    md.append(f"- **Price**: {brief.price or '[price]'}\n")
    md.append(f"- **Platform**: {brief.platform or '[Shopify / Amazon / Etsy / etc.]'}\n")
    md.append(f"- **Audience**: {brief.audience or '[who buys this]'}\n")
    md.append(f"- **Tone**: {brief.tone or '[confident, warm, clinical, playful…]'}\n")
    kw_line = ", ".join(brief.keywords) if brief.keywords else "[primary keyword]"
    md.append(f"- **Target keywords**: {kw_line}\n\n")

    md.append("## Pain point / desired outcome\n\n")
    md.append(f"{brief.pain_point or '[What problem does this solve? What does the customer want?]'}\n\n")

    md.append("## Features & specs\n\n")
    md.append(bullets(brief.features, "[list features, materials, dimensions, ingredients]"))
    md.append("\n")

    md.append("## Differentiators (why this, not a competitor)\n\n")
    md.append(bullets(brief.differentiators, "[what makes this product different]"))
    md.append("\n")

    md.append("## Certifications / trust signals\n\n")
    md.append(bullets(brief.certifications, "[awards, certifications, lab results, reviews count]"))
    md.append("\n")

    md.append("## Constraints\n\n")
    md.append(bullets(brief.constraints, "[word count limits, platform rules, claims to avoid]"))
    md.append("\n")

    md.append("## Requested outputs\n\n")
    md.append("- [ ] SEO product title (60–80 chars)\n")
    md.append("- [ ] Product description (300–500 words)\n")
    md.append("- [ ] Bullet-point highlights (5–7)\n")
    md.append("- [ ] Meta description (150–160 chars)\n")
    md.append("- [ ] Emotional hooks & power words\n")
    md.append("- [ ] Mobile formatting notes\n")

    return "".join(md)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a product description brief markdown from a JSON input."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Path to input JSON.")
    parser.add_argument("--out", dest="out_path", required=True, help="Path to output markdown.")
    args = parser.parse_args()

    in_path = Path(args.in_path).expanduser()
    out_path = Path(args.out_path).expanduser()

    data = json.loads(in_path.read_text(encoding="utf-8"))
    brief = parse_brief(data)
    md = to_markdown(brief)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Brief written to {out_path}")


if __name__ == "__main__":
    main()
