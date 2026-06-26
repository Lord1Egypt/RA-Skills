#!/usr/bin/env python3
"""Build a Mew design request body for a holiday promo poster."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HOLIDAY_PROMPTS = {
    "double-11": (
        "Double 11 e-commerce poster, bold sale atmosphere, strong red-black commerce palette, large discount numerals, "
        "price-burst feeling, high urgency, sharp typography, high-conversion marketplace energy. "
        "Do not make it look soft, minimal, or gift-card-like."
    ),
    "christmas": (
        "Christmas promotional poster, warm festive premium atmosphere, red green gold palette, ribbon and ornament cues, "
        "soft holiday glow, giftable feeling, elegant celebratory composition. "
        "Do not make it look like a loud bargain board or a generic shopping festival."
    ),
    "618": (
        "618 shopping festival poster, dynamic mid-year commerce energy, vivid sale palette, bold deal communication, "
        "clean but lively layout, strong campaign momentum. "
        "Do not make it look like Christmas, Valentine's Day, or a plain catalog page."
    ),
    "new-year": (
        "New Year promotional poster, festive red and gold celebration, prosperity cues, fireworks or festive light atmosphere, "
        "renewal and kickoff feeling, premium celebratory composition. "
        "Do not make it look like a generic sale sheet with no seasonal identity."
    ),
    "valentines-day": (
        "Valentine's Day promo poster, romantic polished atmosphere, pink red and ivory palette, soft glow, giftable elegance, "
        "heart or ribbon cues used tastefully, emotionally warm presentation. "
        "Do not make it look harsh, overly noisy, or like a standard marketplace discount board."
    ),
    "black-friday": (
        "Black Friday poster, high-contrast premium urgency, black gold or black neon palette, aggressive discount focus, "
        "bold commerce punch, sharp spotlight feeling. "
        "Do not make it look cute, pastel, or softly festive."
    ),
}

STYLE_PROMPTS = {
    "mesh-gradient": (
        "Mesh gradient poster style, irregular soft color blooms, airy blended light spots, frosted glass text panels, "
        "premium youthful finish, elegant translucent atmosphere. "
        "Make the mesh-gradient style unmistakable with clear diffused light blooms, translucent frosted text carriers, airy negative space, and soft premium glow. "
        "Do not make it look noisy, geometric-heavy, or like a crowded sale board."
    ),
    "memphis": (
        "Memphis style promotional poster, saturated clash colors, bold dots, zigzags, rings, playful geometry, "
        "dense energetic composition, festive loud retail atmosphere. "
        "Make the Memphis style unmistakable with dense geometric decorations, filled visual space, loud celebratory rhythm, and high-energy clash color combinations. "
        "Do not make it look minimalist, too premium-calm, or under-decorated."
    ),
    "c4d-render": (
        "C4D 3D render poster style, product displayed on a realistic pedestal or display scene, floating decorative objects, "
        "premium material rendering, strong light-shadow depth, expensive polished look. "
        "Make the C4D rendered style unmistakable with an obvious display pedestal or spatial set, polished materials, dimensional props, and premium rendered lighting. "
        "Do not make it look flat, hand-drawn, or like a plain typography poster."
    ),
    "editorial-layout": (
        "Editorial magazine layout poster style, generous whitespace, bold typography hierarchy, large color-block composition, "
        "fashion-forward layout rhythm, elegant and design-led. "
        "Make the editorial style unmistakable with magazine-like layout structure, clear typography contrast, controlled whitespace, and restrained sophisticated composition. "
        "Do not make it look cluttered, childish, or overloaded with geometric decorations."
    ),
    "doodle-illustration": (
        "Doodle illustration promotional poster, real product photo mixed with hand-drawn marks, playful sketch accents, "
        "friendly warm rhythm, approachable visual storytelling. "
        "Make the doodle style unmistakable with visible hand-drawn intervention, handwritten accents, playful sketch marks, and a real-photo-plus-doodle combination. "
        "Do not make it look too rigid, hyper-luxury, or like a pure 3D render."
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a design request body for a holiday promo poster.",
    )
    parser.add_argument("--holiday", required=True, choices=sorted(HOLIDAY_PROMPTS))
    parser.add_argument("--style", required=True, choices=sorted(STYLE_PROMPTS))
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--headline", required=True)
    parser.add_argument("--subheadline")
    parser.add_argument("--offer")
    parser.add_argument("--cta")
    parser.add_argument("--selling-point", action="append", default=[])
    parser.add_argument(
        "--product-image",
        action="append",
        default=[],
        metavar="URL|TAG",
        help="Repeatable product image entry. TAG is optional.",
    )
    parser.add_argument("--brand-color")
    parser.add_argument("--audience")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=-1)
    parser.add_argument("--output")
    return parser.parse_args()


def parse_asset_images(items: list[str]) -> list[dict[str, str]]:
    asset_images: list[dict[str, str]] = []
    for item in items:
        url, separator, tag = item.partition("|")
        url = url.strip()
        tag = tag.strip() if separator else ""
        if not url:
            raise ValueError("Each --product-image entry must include a URL.")
        payload: dict[str, str] = {"url": url}
        if tag:
            payload["tag"] = tag
        asset_images.append(payload)
    return asset_images


def build_user_query(args: argparse.Namespace) -> str:
    sections = [
        "Create a single high-conversion promotional poster in Chinese unless the provided copy is clearly another language.",
        f"Holiday campaign: {args.holiday}",
        f"Poster style: {args.style}",
        f"Product name: {args.product_name}",
        f"Main headline: {args.headline}",
    ]
    if args.subheadline:
        sections.append(f"Subheadline: {args.subheadline}")
    if args.offer:
        sections.append(f"Offer: {args.offer}")
    if args.cta:
        sections.append(f"CTA: {args.cta}")
    if args.selling_point:
        sections.append("Selling points:\n" + "\n".join(f"- {item}" for item in args.selling_point))
    sections.append(
        "Make the product the visual hero, keep the campaign message highly legible, and make both the holiday theme and the chosen poster style obvious at first glance."
    )
    sections.append(
        "Layout safety: reserve a dedicated text-safe area for the headline, offer, and CTA. Do not let the product overlap, cover, or visually swallow any important text."
    )
    sections.append(
        "Place pricing and CTA inside a clean high-contrast region or clear text panel so the business message remains readable at first glance."
    )
    sections.append(
        "Edge safety: keep all copy away from the canvas edges and decorative borders, especially at the bottom. Do not let any line of text touch, cross, or get cut by a frame, ribbon, block edge, or trim edge."
    )
    sections.append(
        "Spacing safety: keep obvious vertical breathing room between the headline block and the product hero. Do not place the product directly under the title or make the top of the product crowd the headline."
    )
    sections.append(
        "Contour safety: treat the product silhouette as a no-text zone. Keep slogans, supporting copy, and small text away from corners, protruding edges, straps, bezels, or other visible product outlines."
    )
    sections.append(
        "When the product is diagonal or has a complex outline, place copy inside a separate text panel or dedicated text column rather than near the product edge."
    )
    if args.style == "mesh-gradient":
        sections.append(
            "Style lock: make the poster clearly read as mesh gradient with diffused color blooms, airy translucency, and frosted text panels. Avoid crowded promotional geometry."
        )
    elif args.style == "memphis":
        sections.append(
            "Style lock: make the poster clearly read as Memphis with dense dots, zigzags, rings, clash colors, and a full lively composition. Avoid sparse premium minimalism."
        )
    elif args.style == "c4d-render":
        sections.append(
            "Style lock: make the poster clearly read as C4D 3D render with an obvious pedestal or spatial display set, dimensional props, and premium rendered materials. Avoid flat collage feeling."
        )
    elif args.style == "editorial-layout":
        sections.append(
            "Style lock: make the poster clearly read as editorial magazine layout with stronger typography hierarchy, visible whitespace, and clean color-block composition. Avoid cluttered sale-board noise."
        )
    elif args.style == "doodle-illustration":
        sections.append(
            "Style lock: make the poster clearly read as doodle illustration with visible hand-drawn marks, playful sketch overlays, and a warm approachable tone. Avoid hyper-polished luxury render staging."
        )
    return "\n\n".join(sections)


def build_design_concept(args: argparse.Namespace) -> str:
    parts = [HOLIDAY_PROMPTS[args.holiday], STYLE_PROMPTS[args.style]]
    if args.brand_color:
        parts.append(f"Use brand accents inspired by {args.brand_color}.")
    if args.audience:
        parts.append(f"Tailor visual tone for {args.audience}.")
    parts.append(
        "Use the provided product images as must-include assets. Keep one strong hero product focus, clean hierarchy, and poster-ready typography. Treat both the selected holiday and the selected poster style as hard constraints."
    )
    parts.append(
        "Protect typography readability with obvious text-safe zones, dedicated copy blocks, or clean negative space. The hero product must not overlap the headline, offer, CTA, or key selling points."
    )
    parts.append(
        "When the composition is visually rich, use a clear panel, calm background region, or structured layout column for text so pricing and call-to-action stay fully legible."
    )
    parts.append(
        "Maintain generous outer margins for all text and add an explicit bottom safe area so the lowest line of copy is never clipped or sliced by the poster edge or any decorative frame."
    )
    parts.append(
        "Create distinct visual zoning between the headline area and the product area, with enough vertical separation that the composition feels calm, premium, and not cramped."
    )
    parts.append(
        "Treat the full product contour as protected space and keep copy outside that silhouette. Use an isolated text panel, copy column, or clean shape-backed text area when needed."
    )
    parts.append(
        "If the first result looks generic or style-drifted, strengthen the missing style traits directly rather than broadening the prompt."
    )
    return " ".join(parts)


def main() -> int:
    args = parse_args()
    if not args.product_image:
        raise SystemExit("At least one --product-image is required.")

    payload = {
        "userQuery": build_user_query(args),
        "designConcept": build_design_concept(args),
        "assetImages": parse_asset_images(args.product_image),
        "width": args.width,
        "height": args.height,
    }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
