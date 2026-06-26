---
name: content-type-router
description: Detect and route to the correct visual content type (hero shot, poster, infographic, etc.) from a text description or output type hint. Use when you need to classify a content generation request into a structured type with layout rules, visual mode, and generation hints.
metadata: {"category": "content-routing", "tags": ["content-type", "routing", "image-generation", "classification", "layout"], "runtime": "python"}
---

# Content Type Router

Classify a content generation request into a structured content type configuration that provides layout rules, visual mode constraints, typography rules, and generation hints for downstream image generation.

## Overview

The router maps natural language descriptions (and optional industry/type hints) to one of 17 predefined content type configurations across 4 categories:

| Category | Slugs |
|----------|-------|
| `product_focused` | `hero_shot`, `lifestyle_shot`, `flat_lay`, `detail_closeup`, `scale_shot`, `unboxing` |
| `typography_heavy` | `poster`, `sale_promo`, `countdown`, `quote_graphic`, `announcement` |
| `educational` | `infographic`, `comparison_chart`, `process_howto`, `carousel_educational` |
| `social_proof` | `testimonial_graphic`, `before_after`, `ugc_repost` |

## Visual Modes

Every content type has one of three visual modes that determine text handling:

| Mode | Slug | Behavior |
|------|------|----------|
| Pure Visual | `pure_visual` | NO text on image — pure photography, composition, and lighting |
| Educational | `educational` | Minimal text allowed (data labels, steps) — up to ~35% of area |
| CTA | `cta` | Text is required — headlines, body, and call-to-action |

## Content Type Reference

### Product-Focused (`pure_visual`)

**`hero_shot`** — Single product on clean background, hero positioning
- Focal point: center | Coverage: 60-80% | Background: white/gradient
- Hints: studio lighting, no props, Amazon/Shopify listing standard

**`lifestyle_shot`** — Product in real-world context showing aspiration
- Focal point: rule-of-thirds | Coverage: 30-50% | Background: contextual
- Hints: natural lighting, authentic mood, story-driven

**`flat_lay`** — Top-down arrangement of multiple items
- Focal point: center | Coverage: 65-75% | Camera: overhead (90°)
- Hints: 3-12 items, cohesive palette, intentional negative space

**`detail_closeup`** — Macro shot for texture and craftsmanship
- Focal point: center | Coverage: 80-95% | Camera: macro
- Hints: shallow depth of field, premium material visibility

**`scale_shot`** — Product with size reference object
- Focal point: center | Coverage: 40-70% | Reference: hand or common object

**`unboxing`** — Product with packaging, reveal aesthetic
- Focal point: center | Coverage: 50-80% | Mood: anticipation/premium

### Typography-Heavy (`cta`)

**`poster`** — Designed travel/event poster with headline and imagery
- Text zone: overlay | Fonts: headline + body | Max 7-word headline

**`sale_promo`** — Promotional graphic with discount/offer messaging
- Text zone: prominent | Single CTA required | Max 35% text area

**`countdown`** — Time-limited offer with countdown element
- Text zone: center | Urgency language | Date/time element required

**`quote_graphic`** — Brand quote or testimonial as designed asset
- Text zone: center | Single quote | Minimal supporting context

**`announcement`** — Product launch or news announcement graphic
- Text zone: structured | Hierarchy: news > detail > CTA

### Educational (`educational`)

**`infographic`** — Data visualization with labeled information
- Text: labels and data points | Max ~35% text area | Clear visual hierarchy

**`comparison_chart`** — Side-by-side comparison of options
- Layout: split | Labels required | Clear differentiation

**`process_howto`** — Step-by-step visual guide
- Layout: sequential | Step numbers | 3-7 steps recommended

**`carousel_educational`** — Multi-frame educational series (single frame rules)
- Consistent style across frames | Progressive information reveal

### Social Proof (`cta` or `educational`)

**`testimonial_graphic`** — Customer quote with attribution
- Quote text required | Customer name/handle | Optional product image

**`before_after`** — Side-by-side transformation visual
- Split composition | Clear before/after labeling | High contrast difference

**`ugc_repost`** — User-generated content styled for brand repost
- Authentic feel | Minimal brand overlay | Source attribution

## Detection API

### Python Usage

```python
from content_types.registry import (
    detect_content_type,
    get_content_type_config,
    get_industry_content_types,
    get_content_types_by_visual_mode,
    get_content_types_by_category,
    get_all_content_types,
)
from content_types.base import VisualMode

# Detect from description
slug, confidence = detect_content_type(
    description="I need a product shot on white background for Amazon",
    industry="ecommerce",
)
# → ("hero_shot", 0.95)

# Get full config with layout rules and generation hints
config = get_content_type_config(slug)
prompt_context = config.to_prompt_context()  # Inject into LLM prompt
negative_prompts = config.get_negative_prompt_string()  # For image gen

# Industry-based recommendations
types = get_industry_content_types("beauty")
# → [HeroShot, BeforeAfter, FlatLay]

# Filter by visual mode
pure_visual_types = get_content_types_by_visual_mode(VisualMode.PURE_VISUAL)

# Filter by category
product_types = get_content_types_by_category("product_focused")
```

### Detection Logic

1. If `output_type` exactly matches a slug → confidence 1.0
2. Keyword scoring across all registered types
3. Normalized score with multi-match bonus
4. If confidence < 0.3 → fall back to industry default
5. Ultimate fallback: `lifestyle_shot`

### Detection Return

```python
(slug: str, confidence: float)
# confidence: 0.0-1.0
# 0.3+ = usable, 0.7+ = high confidence
```

## `ContentTypeConfig` Structure

```python
@dataclass
class ContentTypeConfig:
    name: str                          # Human-readable name
    slug: str                          # Machine key: "hero_shot"
    category: str                      # "product_focused" | "typography_heavy" | etc.
    definition: str                    # One-line definition for LLM context
    visual_mode: VisualMode            # PURE_VISUAL | EDUCATIONAL | CTA
    layout: LayoutRules                # Focal point, coverage, background, camera angle
    typography: Optional[TypographyRules]  # Headline words, weight, CTA rules
    generation_hints: List[str]        # Positive requirements for image gen prompt
    negative_prompts: List[str]        # What to avoid (comma-joined for diffusion)
    detection_keywords: List[str]      # Keyword matching corpus
    common_industries: List[str]       # Industry affinity
    aspect_ratios: List[str]           # Recommended ratios: ["4:5", "1:1"]
```

## `LayoutRules` Structure

```python
@dataclass
class LayoutRules:
    focal_point: str           # "center" | "upper_third" | "rule_of_thirds" | "left" | "right"
    text_zone: Optional[str]   # "bottom_40_percent" | "top_20_percent" | "overlay" | None
    subject_coverage_min: float  # Min % of frame for main subject
    subject_coverage_max: float  # Max % of frame for main subject
    text_area_max: float       # Max % of frame for text (0.0 = no text)
    logo_zone: str             # "corner" | "bottom_center" | "none"
    whitespace_min: float      # Minimum negative space target
    camera_angle: Optional[str]  # "eye_level" | "overhead" | "low_angle" | "macro"
    background: Optional[str]  # "white" | "gradient" | "contextual" | "lifestyle"
```

## Industry Defaults

| Industry | Top 3 Content Types |
|----------|---------------------|
| travel | poster, lifestyle_shot, carousel_educational |
| dtc | hero_shot, lifestyle_shot, ugc_repost |
| fashion | lifestyle_shot, flat_lay, ugc_repost |
| beauty | hero_shot, before_after, flat_lay |
| food | flat_lay, lifestyle_shot, process_howto |
| saas | infographic, comparison_chart, testimonial_graphic |
| luxury | hero_shot, detail_closeup, lifestyle_shot |
| health | before_after, testimonial_graphic, infographic |

## Database Mode

The registry supports optional DB-backed content types (for per-brand customization):

```bash
export USE_DB_CONTENT_TYPES=true  # Enable DB mode
```

When enabled, types load from a `content_types` Supabase table with brand-specific overrides. Falls back to code-defined types on DB errors.

```python
# Invalidate cache after DB updates
from content_types.registry import invalidate_cache
invalidate_cache()

# Enable/disable at runtime
from content_types.registry import enable_db_mode
enable_db_mode(True)
```

## Integration Pattern

Inject the config into image generation prompts:

```python
slug, confidence = detect_content_type(description, industry=industry)
config = get_content_type_config(slug)

# Build generation prompt
system_context = config.to_prompt_context()
negative = config.get_negative_prompt_string()

# Pass to image generation
generate_image(
    prompt=f"{system_context}\n\n{user_prompt}",
    negative_prompt=negative,
    aspect_ratio=config.aspect_ratios[0],
)
```
