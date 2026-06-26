# Macaron Card Design Reference

## Colour Palette

| Name | Background | Accent | Text | Light |
|------|-----------|--------|------|-------|
| Pink | `#FFF0F3` | `#FF8FAB` | `#C9184A` | `#FFB5C2` |
| Blue | `#F0F4FF` | `#8FC7FF` | `#1A56DB` | `#B5D8FF` |
| Green | `#F0FFF2` | `#8FD9A5` | `#0E6B2E` | `#B5E8C3` |
| Yellow | `#FFF9F0` | `#FFD68F` | `#B45309` | `#FFE5B4` |
| Purple | `#F8F0FF` | `#C2A8FF` | `#6D28D9` | `#D4BFFF` |
| Orange | `#FFF6F0` | `#FFB88F` | `#C2410C` | `#FFD1B5` |
| Mint | `#F0FFFB` | `#8FD5CE` | `#0F766E` | `#B5E5E0` |
| Lavender | `#F5F0FF` | `#D4BFFF` | `#7C3AED` | `#E8D5FF` |

Default palette per card type:
- **book** → mint / blue / pink
- **concept** → purple / lavender / blue
- **quote** → pink / orange / purple
- **compare** → blue / mint / green

## Available Aspect Ratios

| Ratio | Width × Height |
|-------|---------------|
| 1:1 | 800 × 800 |
| 3:4 | 750 × 1000 |
| 4:3 | 1000 × 750 |
| 9:16 | 720 × 1280 |
| 16:9 | 1280 × 720 |
| 2:3 | 700 × 1050 |

Default is **3:4**.

## Card Type Content Fields

### book — Book Recommendation Card
```json
{
  "title": "Book Title",
  "author": "Author",
  "cover_description": "One-line review / cover description",
  "recommendation_reason": "Reason for recommendation",
  "key_takeaway": "Key takeaway in one sentence",
  "rating": "4.5",
  "tags": ["Tag 1", "Tag 2"],
  "ratio": "3:4"
}
```

### concept — Concept Card
```json
{
  "concept_name": "Concept Name",
  "definition": "One-line definition",
  "examples": ["Example 1", "Example 2"],
  "related_concepts": ["Related Concept 1", "Related Concept 2"],
  "ratio": "3:4"
}
```

### quote — Quote Card
```json
{
  "quote_text": "Quote content",
  "author": "Author / Source",
  "source": "Origin",
  "context": "Background note (optional)",
  "ratio": "3:4"
}
```

### compare — Comparison Card
```json
{
  "topic": "Comparison Topic",
  "left_label": "Side A Label",
  "left_items": ["A Trait 1", "A Trait 2"],
  "right_label": "Side B Label",
  "right_items": ["B Trait 1", "B Trait 2"],
  "conclusion": "Conclusion (optional)",
  "ratio": "3:4"
}
```