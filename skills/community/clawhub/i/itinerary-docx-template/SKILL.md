---
name: itinerary-docx-template
description: Generate tourism itinerary DOCX by replacing only matched itinerary sections inside a provided Chinese template document. Use when the user sends a simplified route text like "1南宁接 ... 住XX酒店" and asks to keep original template styling/terms while updating day-by-day schedule, scenic descriptions, meals, and hotels.
---

# Itinerary DOCX Template Filler

Fill a Chinese travel-agency template DOCX from simplified itinerary lines, while preserving template style.

## Workflow

1. Save user simplified content into a UTF-8 `.txt` file (one day per line).
2. Run `scripts/fill_from_simplified.py` with:
   - `--template` source template docx
   - `--content` simplified txt
   - `--output` output docx
3. Send resulting `.docx` back to user.

## Simplified input format

One line per day:

- `1南宁接 三街两巷 中山路小吃街 住南宁丽呈瑞轩酒店（会展店）`
- `2明仕田园 太平古城 住崇左维纳斯度假酒店`
- `3德天瀑布 蓝洞咖啡 住龙州观堂酒店`

Rules:
- Leading number = day number.
- `住...` segment = hotel.
- Remaining tokens after day head are scenic spots.

## Notes

- Keep template clauses/terms unchanged; replace only itinerary-related paragraphs.
- If `python-docx` is missing, install via `python -m pip install python-docx`.
- This script is tuned for the user's current template layout and paragraph anchors.
