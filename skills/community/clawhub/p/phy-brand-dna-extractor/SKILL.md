---
name: brand-dna-extractor
description: Extract brand identity (colors, typography, visual style, imagery) from any website URL. Scrapes the site, analyzes CSS/images with K-means and VLM, and returns a structured brand profile. Use when you need to understand a brand's visual language before generating on-brand content.
metadata: {"category": "brand-analysis", "tags": ["brand", "colors", "typography", "visual-style", "scraping", "vlm"], "runtime": "python", "env": ["OPENAI_API_KEY", "GOOGLE_GENAI_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]}
---

# Brand DNA Extractor

Extract a structured brand identity profile from any website URL. Analyzes colors, typography, and visual style to produce a reusable brand profile for on-brand content generation.

## Environment Variables

```bash
export OPENAI_API_KEY="your_openai_key"          # for VLM visual analysis (fallback)
export GOOGLE_GENAI_API_KEY="your_gemini_key"    # for VLM visual analysis (primary)
export SUPABASE_URL="your_supabase_url"          # optional: for caching results
export SUPABASE_KEY="your_supabase_key"          # optional: service role key
```

## What It Extracts

| Component | Details |
|-----------|---------|
| **Color palette** | Primary, secondary, accent, background, and text colors — sourced from CSS variables, computed styles, and K-means image clustering |
| **Typography** | Heading and body fonts, weights, sources (Google Fonts, Adobe Fonts, system) |
| **Visual style** | Mood descriptors, photography styles, composition notes, lighting characterization, brand personality, target audience signals |
| **Imagery** | Logo, favicon, hero images, product images, other images — classified and ranked |

## Python Usage

```python
import asyncio
from brand_dna_extractor.extractor import BrandDNAExtractor, extract_brand_dna

# Quick extraction
async def main():
    result = await extract_brand_dna(
        url="https://example.com",
        user_id="optional-user-id",
        force_refresh=False,
    )

    if result.success:
        dna = result.brand_dna
        print(dna.color_palette.dominant_color)       # "#2563EB"
        print(dna.typography.primary_font.family)     # "Inter"
        print(dna.visual_style.moods)                 # ["warm minimalism", "approachable"]
        print(dna.visual_style.brand_personality)     # "Confident and calm..."
    else:
        print(result.error)

asyncio.run(main())

# Full control
extractor = BrandDNAExtractor(
    vlm_provider="gemini",      # "gemini" (default) or "openai"
    enable_storage=True,        # cache results in Supabase
    enable_embeddings=False,    # skip CLIP embedding generation
)

result = await extractor.extract(
    url="https://example.com",
    include_subpages=True,      # also scrape about/product pages
    max_subpages=5,
    force_refresh=False,
)
```

## 5-Step Extraction Pipeline

### Step 1: Website Scraping

Uses a two-tier scraping strategy:

**Primary — DOM Structure Scraper** (`SimpleScraper`)
- Fast HTTP requests with structured HTML parsing
- Extracts CSS variables, computed styles, stylesheets, JSON-LD data
- Optimized for Shopify stores (reads product JSON-LD)
- Follows `include_subpages` to crawl up to `max_subpages` additional URLs

**Fallback — Playwright Scraper** (`PlaywrightScraper`)
- Activates when simple scraper yields < 3 gallery/product images
- Handles JavaScript-rendered content
- Optional dependency: `pip install playwright && playwright install`

### Step 2: Image Extraction and Classification

Images are classified into types:

| Type | Description |
|------|-------------|
| `logo` | Site logo (detected by position, alt text, size) |
| `favicon` | Site favicon |
| `hero` | Large above-the-fold banner images |
| `product` | Product photography |
| `lifestyle` | Contextual/lifestyle imagery |
| `other` | Remaining UI images |

Up to 100 images extracted; top 30 product + 30 other retained.

### Step 3: Color Analysis

Multi-source color extraction and classification:

```
CSS custom properties (--primary-color, --brand-color, etc.)
    +
Computed element styles (headerBackground, ctaBackground, linkColor, etc.)
    +
K-means clustering on logo pixels (3 colors)
    +
K-means clustering on hero/product images (3 colors each, up to 5 images)
    ↓
Deduplicate (Euclidean distance threshold = 30)
    ↓
Classify by lightness/saturation:
  L > 0.9  → background
  L < 0.15 → text
  S > 0.6  → accent
  source=primary → primary
  else     → secondary
```

**`ColorPalette` output:**
```python
palette.dominant_color        # "#2563EB" (hex string)
palette.primary_colors        # List[ColorInfo] (up to 3)
palette.secondary_colors      # List[ColorInfo] (up to 3)
palette.accent_colors         # List[ColorInfo] (up to 2)
palette.background_colors     # List[ColorInfo] (up to 2)
palette.text_colors           # List[ColorInfo] (up to 2)
```

**`ColorInfo` fields:** `hex`, `rgb`, `hsl`, `role`, `source`, `name`, `frequency`, `css_property`

### Step 4: Typography Analysis

Font detection from three sources:

**CSS Computed Fonts**
- Parses `font-family` declarations from computed element styles
- Classifies by role: heading, body, cta, nav
- Identifies system fonts vs custom fonts

**Google Fonts** (detected from stylesheet URLs)
- Parses both old (`/css?family=`) and new (`/css2?family=`) API formats
- Extracts family names and weight variants

**Adobe Fonts / Typekit** (detected from stylesheet URLs)
- Flags usage of `use.typekit.net` or `use.adobe.com`

**`Typography` output:**
```python
typography.primary_font         # FontInfo — main body font
typography.secondary_font       # FontInfo — heading font (if different)
typography.heading_fonts        # List[FontInfo]
typography.body_fonts           # List[FontInfo]
typography.accent_fonts         # List[FontInfo]
typography.google_fonts_urls    # List[str]
typography.detected_from_google_fonts  # bool
typography.detected_from_adobe_fonts   # bool
```

**`FontInfo` fields:** `family`, `weight`, `role`, `source`, `fallbacks`, `url`

### Step 5: Visual Style Analysis (VLM)

Up to 5 representative images (prioritized: hero > product > lifestyle) are analyzed by a VLM using a structured creative director prompt.

**Analysis dimensions:**
1. Visual mood and atmosphere (3-5 compound descriptors)
2. Photography/visual style (2-3 technical descriptors)
3. Composition analysis (negative space, focal point, depth)
4. Lighting characterization (quality, direction, color temperature)
5. Texture and material language
6. Dominant subjects
7. Brand personality inference
8. Target audience signals

**VLM provider selection:**
- Default: Gemini (`gemini-3-flash-preview` or env `GEMINI_MODEL`)
- Fallback: OpenAI Vision (env `OPENAI_MODEL`)
- Automatic retry with exponential backoff (3 attempts)

**`VisualStyle` output:**
```python
style.moods                  # List[str] — top 5 by frequency across images
style.photography_styles     # List[str] — top 3
style.composition_notes      # str — aggregated composition analysis
style.lighting_style         # str
style.texture_notes          # str
style.dominant_subjects      # List[str] — top 5
style.brand_personality      # str — 2-3 sentences
style.target_audience_hint   # str — 2-3 sentences
style.confidence_score       # float — 0.0-1.0 (higher with more images analyzed)
style.images_analyzed        # int
```

## `BrandDNA` Object

```python
@dataclass
class BrandDNA:
    url: str
    domain: str
    logo: Optional[ExtractedImage]
    favicon: Optional[ExtractedImage]
    hero_images: List[ExtractedImage]
    product_images: List[ExtractedImage]
    other_images: List[ExtractedImage]
    color_palette: ColorPalette
    typography: Typography
    visual_style: VisualStyle
    id: Optional[str]                 # UUID if stored in database
    style_embedding: Optional[List[float]]  # CLIP embedding if enabled
```

## Caching

When `enable_storage=True` and Supabase credentials are configured, results are automatically cached by domain.

```python
# Force re-extraction (ignore cache)
result = await extractor.extract(url, force_refresh=True)

# Retrieve cached result by domain
from brand_dna_extractor.extractor import get_brand_dna_by_domain
dna = await get_brand_dna_by_domain("example.com")

# Retrieve by stored ID
from brand_dna_extractor.extractor import get_brand_dna
dna = await get_brand_dna("uuid-string")
```

## Error Handling

`BrandDNAResponse` always returns a result object:

```python
result = await extractor.extract(url)

result.success         # bool
result.brand_dna       # BrandDNA | None
result.error           # str | None — human-readable error description
result.from_cache      # bool — True if returned from cache
```

Common failure modes:
- Both scrapers fail (site blocks bots, requires login)
- VLM API quota exhausted
- URL is not a public website

## Installation

```bash
pip install aiohttp Pillow numpy scikit-learn openai google-generativeai
# Optional for JS-heavy sites:
pip install playwright && playwright install chromium
```

## Example Output

```python
BrandDNA(
    domain="allbirds.com",
    color_palette=ColorPalette(
        dominant_color="#2B2B2B",
        primary_colors=[ColorInfo(hex="#2B2B2B", role="primary"), ...],
        accent_colors=[ColorInfo(hex="#E8D5C0", role="accent"), ...],
    ),
    typography=Typography(
        primary_font=FontInfo(family="Flanders Sans", weight="400", source="css"),
        detected_from_google_fonts=False,
    ),
    visual_style=VisualStyle(
        moods=["warm minimalism", "earthy authenticity", "understated confidence"],
        photography_styles=["lifestyle documentary", "naturalistic color treatment"],
        brand_personality="Calm and purposeful, with a commitment to sustainability...",
        target_audience_hint="Environmentally conscious millennials and Gen Z...",
        confidence_score=0.83,
        images_analyzed=5,
    ),
)
```
