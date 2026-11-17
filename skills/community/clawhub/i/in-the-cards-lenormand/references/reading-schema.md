# Reading Schema — In the Cards v3.3

Defines the canonical JSON structure for persisted Lenormand readings.
Each reading is saved to `output/readings/{reading_id}.json` with a parallel `{reading_id}.md` human-readable copy.

## Top-Level Structure

```json
{
  "version": "3.3",
  "reading_id": "2026-06-20-写作方向",
  "meta": { ... },
  "cards": [ ... ],
  "interpretation": { ... }
}
```

## `meta` — Reading Metadata

```json
{
  "language": "zh",
  "spread_type": "three",
  "spread_label": "三張線性牌陣",
  "question": "我的写作方向应该是什么？",
  "date": "2026-06-20",
  "generated_at": "2026-06-20T21:35:00+08:00",
  "source": "stargazer-oracle",
  "topic_slug": "写作方向"
}
```

Fields:
- `language`: `"zh"` or `"en"` — drives all label/title language
- `spread_type`: `"yesno-1"` | `"two"` | `"three"` | `"five"` | `"nine"` | `"choice"` | `"daily"`
- `spread_label`: human-readable spread type name in the detected language
- `question`: the querent's question (null for daily)
- `date`: YYYY-MM-DD from the prompt
- `generated_at`: ISO 8601 timestamp of interpretation generation
- `source`: `"stargazer-oracle"` for compatible Stargazer’s Oracle prompts or `"freeform"` for manually supplied spreads. Existing readings may retain the legacy value `"stargazer.estework.site"`.
- `topic_slug`: 2-6 character Chinese topic identifier extracted from question

## `cards` — Card Array

Each card object:

```json
{
  "position": 1,
  "position_label": "過去 / Past",
  "card_id": 26,
  "name_zh": "書",
  "name_en": "Book",
  "slug": "book",
  "polarity": "neutral"
}
```

Position labels by spread type:
- `yesno-1`: `["抽出 / Drawn"]`
- `two`: `["1", "2"]`
- `three`: `["過去 / Past", "現在 / Present", "未來 / Future"]`
- `five`: `["1", "2", "3 / 核心 / Core", "4", "5"]`
- `nine`: Grid positions 1-9; also tagged with `grid_row` and `grid_col`
- `choice`: `["A1", "A2", "A3", "B1", "B2", "B3"]`

For `nine` (box) spread, additional fields:
```json
{
  "position": 5,
  "grid_row": 2,
  "grid_col": 2,
  "is_center": true,
  "is_significator": false,
  ...
}
```

For `choice` spread, cards are grouped:
```json
{
  "optionA_cards": [ { ... }, { ... }, { ... } ],
  "optionB_cards": [ { ... }, { ... }, { ... } ]
}
```
with a flat `cards` array combining all 6.

## `interpretation` — Structured Interpretation

```json
{
  "summary": "一句总结 / One-sentence summary",
  "chapters": [
    {
      "id": "chain-reading",
      "title": "組合解讀 · Chain Reading",
      "short_title": "組合解讀",
      "sections": [
        {
          "type": "paragraph",
          "content": "Markdown text..."
        },
        {
          "type": "combination",
          "cards": [1, 2],
          "label": "騎士 + 幸運草",
          "content": "Markdown text..."
        },
        {
          "type": "paragraph",
          "content": "Markdown text..."
        },
        {
          "type": "takeaway",
          "content": "Markdown text..."
        }
      ]
    }
  ]
}
```

### Section Types

- `paragraph` — standard body text paragraph
- `combination` — card pair callout with `cards` array (position indices), `label` (display name), and `content`
- `takeaway` — key insight box (one per chapter, at the end)

### Chapter IDs by Spread Type

| Spread | Chapter IDs |
|--------|-------------|
| yesno-1 | `["verdict"]` |
| two | `["combined-meaning"]` |
| three | `["chain-reading", "overall-meaning", "guidance"]` |
| five | `["core-theme", "chain-reading", "overall-trajectory"]` |
| nine | `["time-axis", "three-layers", "cross-method", "key-combinations", "overall-synthesis"]` |
| choice | `["option-a", "option-b", "comparison"]` |

## Verdict (yesno-1 only)

```json
{
  "verdict": "YES",
  "verdict_zh": "是",
  "verdict_en": "YES"
}
```

This goes at the top level alongside `meta`, `cards`, `interpretation`.

## Choice Options (choice only)

```json
{
  "optionA": {
    "text": "Option A description",
    "cards": [ ...3 cards... ]
  },
  "optionB": {
    "text": "Option B description",
    "cards": [ ...3 cards... ]
  }
}
```

This goes at the top level alongside `meta`, `cards`, `interpretation`.

## Index File: `output/readings/index.json`

```json
[
  {
    "reading_id": "2026-06-20-写作方向",
    "language": "zh",
    "spread_type": "three",
    "question": "我的写作方向应该是什么？",
    "date": "2026-06-20",
    "generated_at": "2026-06-20T21:35:00+08:00",
    "topic_slug": "写作方向",
    "card_names": ["騎士", "幸運草", "書"],
    "products_generated": ["a4-pdf"]
  }
]
```

The `products_generated` array tracks which product types have been generated for this reading. Update it whenever a new product is created.
