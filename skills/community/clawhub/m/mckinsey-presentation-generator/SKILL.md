---
name: mckinsey-presentation-generator
description: "McKinsey consulting-style multi-page HTML presentation generator. Creates data-rich, visually compelling slide decks with rigorous research, SVG charts, and proper source citations. TRIGGERS: McKinsey, consulting deck, presentation, PPT, slide deck, data visualization, business presentation, market analysis slides."
---

# McKinsey-Style Multi-Page Presentation Generator

## Overview

This skill produces professional McKinsey consulting-style HTML slide decks. Every presentation is data-driven, information-dense, and visually rigorous. The workflow covers end-to-end generation: research → planning → slide creation (cover, content, section dividers, TOC, summary) → deployment. All slides are rendered as static HTML with inline SVG charts — no generated images except in rare, data-driven cases.

---

## Workflow (MANDATORY ORDER — No Skipping Steps)

### Step 1: Research Phase (CRITICAL — DO FIRST)

**NEVER skip this step. Data quality determines presentation quality.**

Gather comprehensive data before any slide creation:

#### Research Objectives
- Market size, CAGR, growth rates
- Company metrics and milestones
- Competitor analysis and market share
- Historical trend data for charts
- Verified statistics with source citations

#### Information Source Prioritization

| Tier | Source Type | Examples |
|------|-------------|----------|
| 1 | Official Data/APIs | Company filings, government databases, central banks |
| 2 | Research Institutions | McKinsey, BCG, Goldman Sachs, Morgan Stanley, IMF, World Bank |
| 3 | Industry Reports | Gartner, Statista, CB Insights, PitchBook |
| 4 | News Organizations | Reuters, Bloomberg, Financial Times |
| 5 | Company Websites | Official press releases, investor relations |

#### Search Strategy

Execute multiple targeted searches:
1. "[Topic] market size 2025"
2. "[Topic] industry report"
3. "[Company] revenue growth 2025"
4. "[Topic] competitors market share"
5. "[Topic] trends forecast 2026"
6. "[Company] founding history milestones"
7. "[Topic] CAGR growth rate"
8. "[Topic] regional breakdown"

#### Data Quality Requirements

For every piece of data collected, record:
1. The specific data point (number, percentage, fact)
2. The source name (organization)
3. The publication date or data date
4. The original URL

**MANDATORY minimums before completing research:**
- [ ] At least 15 specific statistics/data points
- [ ] At least 5 different sources
- [ ] Data for each planned content slide
- [ ] Historical trend data for at least 1 chart
- [ ] Competitor comparison data
- [ ] Proper source citations in PPT format

**AVOID:**
- ❌ Unsourced claims
- ❌ Outdated data (>2 years old for fast-moving industries)
- ❌ Vague qualitative statements ("significant growth")
- ❌ Single-source critical facts

#### Research Output Format

```
## RESEARCH SUMMARY

### Topic: [Topic Name]
Research Date: [Current Date]

---

### SLIDE N: [Slide Title]

**Key Data Points:**
1. [Data point 1] - [Value]
2. [Data point 2] - [Value]

**Chart Data (if applicable):**
| Year | Value | YoY Growth |
|------|-------|------------|
| 2023 | $XX   | +XX%       |
| 2024 | $XX   | +XX%       |
| 2025 | $XX   | +XX%       |

**Source Citation:** Source: [Organization 1], [Organization 2] | [Date]

---

### ALL SOURCES

| # | Source Name | Type | Date | URL | Reliability |
|---|-------------|------|------|-----|-------------|
| 1 | [Name] | [Report/News/Official] | [Date] | [URL] | High/Medium |
```

### Step 2: Presentation Planning

Based on research findings, plan the slide structure:
- Default: 10 slides (unless user specifies otherwise)
- **Recommended structure**: Cover → Content Pages → Summary
- **Section dividers are OPTIONAL** — only include if content naturally divides into distinct sections
- For most presentations, a simple Cover + Content + Summary structure is preferred

**Typical 10-slide structure:**
- Slide 1: Cover page
- Slides 2–9: Content pages with data visualizations
- Slide 10: Summary/Conclusion

### Step 3: Generate Cover Page

- NO generated images allowed
- NO graphical elements (shapes, icons, decorations)
- Use solid colors OR subtle gradients ONLY
- Centered typography is the PRIMARY visual element
- Elegant, restrained, professional

See [Cover Page Specifications](#cover-page) below.

### Step 4: Generate Content Pages

For each content slide:
- Minimum 4 distinct content zones per page
- White background is MANDATORY default (80%+ of slides)
- SVG charts only — no generated images
- Include source citations in footer

See [Content Page Specifications](#content-page) below.

### Step 5: Generate Optional Pages

If needed, generate:
- Table of Contents (see [TOC Specifications](#table-of-contents))
- Section Dividers (see [Section Divider Specifications](#section-divider))
- Summary/Closing Page (see [Summary Page Specifications](#summary-closing-page))

### Step 6: Deployment

Deploy the completed presentation using `deploy_html_presentation`.

---

## Design System

### Core Design Philosophy

**Professional & Serious**: All presentations must be square, formal, and business-appropriate. This is a consulting deck, NOT a creative portfolio.

**Data-Driven**: Every content slide must be backed by verifiable data with proper source citations.

**Information Density**: Content pages should maximize information density with at least 4 distinct content zones per slide.

**Style**: Sharp & Compact — square corners, high information density, professional severity. `border-radius: 0` on ALL elements.

### Color System

#### Primary Colors

| Element | Color Name | Hex | Usage |
|---------|------------|-----|-------|
| **Main Background** | White | `#FFFFFF` | Primary slide background (MANDATORY DEFAULT) |
| **Title Bar/Header** | Deep Navy Blue | `#0B1F3A` | Top header bar (0.6" height) |
| **Primary Accent** | Cobalt Blue | `#1B5AB5` | Primary chart series, emphasis elements, insight text |
| **Body Text/Labels** | Dark Gray | `#2D2D2D` | Primary body text, data labels |
| **Secondary Text/Footnotes** | Medium Gray | `#8C8C8C` | Secondary text, footnotes, sources |
| **Grid Lines/Dividers** | Light Gray | `#E0E0E0` | Chart grid lines, separators |

#### Cover Page & Section Divider Background Colors (Choose ONE)

| Option | Hex Code | Effect | Text Color |
|--------|----------|--------|------------|
| **White** | `#FFFFFF` | Clean, minimal, modern | Navy `#0B1F3A` |
| **Navy Blue** | `#0B1F3A` | Professional, authoritative | White `#FFFFFF` |
| **Cobalt Blue** | `#1B5AB5` | Bold, confident | White `#FFFFFF` |
| **Cyan** | `#2E8BC0` | Fresh, innovative | White `#FFFFFF` |
| **Emerald Green** | `#3AAF6C` | Growth, sustainability | White `#FFFFFF` |
| **Gray** | `#4A4A4A` | Neutral, sophisticated | White `#FFFFFF` |

#### Gradient Options (Cover/Divider pages ONLY, subtle only)

| Gradient | CSS Example |
|----------|-------------|
| Navy to Dark | `background: linear-gradient(180deg, #0B1F3A 0%, #1B3A5C 100%);` |
| Blue to Navy | `background: linear-gradient(180deg, #1B5AB5 0%, #0B1F3A 100%);` |

**Note:** Gradients are ONLY allowed on cover pages and section dividers. Content pages MUST NOT use gradients.

#### Chart Data Series Colors (use in order)

| Series | Color Name | Hex |
|--------|------------|-----|
| 1 | Cobalt Blue | `#1B5AB5` |
| 2 | Cyan Blue | `#2E8BC0` |
| 3 | Amber Gold | `#D4A843` |
| 4 | Coral Red | `#E05252` |
| 5 | Emerald Green | `#3AAF6C` |
| 6 | Purple Gray | `#7B6D9E` |

#### Semantic Colors

| Purpose | Color | Hex |
|---------|-------|-----|
| Positive Data | Green | `#3AAF6C` |
| Negative Data | Red | `#E05252` |

#### ⚠️ Accent Color Limit (STRICTLY ENFORCED — MAX 2 PER PAGE)

**RULE: Maximum 2 accent colors per page. This is NON-NEGOTIABLE.**

| Type | Colors | Can Use Freely |
|------|--------|----------------|
| **Base Colors** | Navy #0B1F3A, White #FFFFFF, Grays (#2D2D2D, #8C8C8C, #E0E0E0) | ✅ Yes |
| **Primary Accent** | Cobalt Blue #1B5AB5 | ✅ Always allowed |
| **Secondary Accent** | #2E8BC0, #D4A843, #E05252, #3AAF6C, #7B6D9E | ⚠️ Pick ONLY ONE |

**Enforcement:**
1. **Before writing HTML**: Decide which 2 accent colors you will use
2. **During HTML writing**: Only use those 2 colors for accents
3. **During verification**: Count accent colors — if >2, FIX by replacing extras with #1B5AB5 or #E0E0E0

**ONLY EXCEPTION**: Multi-series charts with 3+ distinct data categories may use additional colors within that single chart.

#### Alternative Color Schemes

Use ONLY when the McKinsey White Theme is not appropriate:

| # | Name | Colors | Style | Use Cases |
|---|------|--------|-------|-----------|
| 2 | Modern Health | `#006d77` `#83c5be` `#edf6f9` `#ffddd2` `#e29578` | Fresh, healing | Healthcare, wellness |
| 3 | Business Authority | `#2b2d42` `#8d99ae` `#edf2f4` `#ef233c` `#d90429` | Serious, classic | Annual reports, government |
| 4 | Nature Outdoor | `#606c38` `#283618` `#fefae0` `#dda15e` `#bc6c25` | Earthy, grounded | Environmental, agriculture |
| 5 | Dynamic Tech | `#8ecae6` `#219ebc` `#023047` `#ffb703` `#fb8500` | High energy | Startup pitches |
| 6 | Pure Tech Blue | `#03045e` `#0077b6` `#00b4d8` `#90e0ef` `#caf0f8` | Futuristic | Cloud/AI, clean energy |
| 7 | Platinum White Gold | `#0a0a0a` `#0070F3` `#D4AF37` `#f5f5f5` `#ffffff` | Premium | Fintech, luxury brands |

### Typography

#### Font Family

| Language | Font | Notes |
|----------|------|-------|
| **Chinese** | Microsoft YaHei | Use for all titles and body text |
| **English** | Arial / Arial Black | Arial Black for titles, Arial for body |

CSS `font-family` declaration: `"Microsoft YaHei", Arial, sans-serif`

#### Typography Hierarchy

| Element | Font | Size | Color | Notes |
|---------|------|------|-------|-------|
| **Page Title (Header Bar)** | Arial Black | 24px | `#FFFFFF` | White text on dark navy header |
| **Insight/Subtitle** | Arial Bold | 16px | `#1B5AB5` | Blue text, one-line key insight |
| **Chart Title** | Arial Bold | 12px | `#2D2D2D` | Above each chart |
| **Body/Data Labels** | Arial | 10–12px | `#2D2D2D` | Chart labels and body |
| **Chart Legend** | Arial | 9px | `#2D2D2D` | Below or right of chart |
| **Footnotes/Sources** | Arial | 8px | `#8C8C8C` | Bottom of slide |

#### Font Size Limits (STRICT)

| Element | Max Size | Notes |
|---------|----------|-------|
| Page Title | 24px | In header bar |
| Insight Text | 16px | Below header |
| Stat Callout | 48px | Large numbers only |
| Chart Title | 12px | Above charts |
| Body Text | 10–12px | Compact for density |
| Labels | 9–10px | Chart labels |
| Footnotes | 8px | Source citations |

**NO element should exceed 48px except in rare stat callout situations.**

### Forbidden Elements (DO NOT USE)

| ❌ Forbidden | Reason | ✅ Use Instead |
|-------------|--------|----------------|
| **Rounded corners** (`border-radius`) | Looks casual/playful | Square corners (`border-radius: 0`) |
| **Generated images** | Decorative, unprofessional | SVG charts, data visualizations |
| **Oversized fonts** (>48px for body) | Looks like a billboard | Compact, data-dense typography |
| **Drop shadows** | Looks dated/gimmicky | Clean flat design |
| **Gradients on content elements** | Distracting | Solid colors |
| **Animations/transitions** | Unprofessional for consulting | Static content |
| **Decorative icons** | Cluttered | Minimal functional icons only |
| **Bright/saturated colors** | Looks unprofessional | Muted, business colors |

### Required Style Attributes

```css
/* ALL elements must have square corners */
border-radius: 0;

/* Bars and charts - NO rounded corners */
rect { rx: 0; ry: 0; }

/* Progress bars - square ends */
.progress-bar { border-radius: 0; }

/* Cards and boxes - sharp edges */
.card, .box, .zone { border-radius: 0; }
```

---

## Source Citation Format (MANDATORY)

Every slide containing data MUST include a footer citation:

```
Source: [Organization Name(s)] | [Data Period] | [Optional: Disclaimer]
```

**Examples:**

| Type | Example |
|------|---------|
| Financial | `Source: Wind, CSRC, PBoC | Full Year 2025` |
| Research | `Source: Goldman Sachs, Morgan Stanley, JP Morgan, IMF | Forecasts as of early 2026 | Not investment advice` |
| Company | `Source: Company Annual Report 2025 | Data as of December 2025` |
| Industry | `Source: Statista, IDC, Gartner | Q4 2025 | Market estimates` |
| Government | `Source: National Bureau of Statistics | 2025 Annual Data` |

---

## Image Generation Rules (STRICT)

**Maximum 3 images per entire presentation**, only for:
- Market Positioning Map (based on actual research data)
- Timeline/Milestone Diagram (actual company data)
- Process Flow Diagram (actual workflow)
- Geographic Map (when location is central)

**FORBIDDEN:**
- ❌ Generic decorative images
- ❌ Stock photo style images
- ❌ Concept illustrations without data
- ❌ Background images for aesthetics
- ❌ Icons (use SVG instead)

**All other visuals must be SVG charts created in HTML/CSS.**

---

## Slide Types

### Cover Page

**Design: Elegant & Minimal — centered typography only.**

#### ALLOWED Elements
- Solid color backgrounds (from the color palette)
- Subtle CSS gradients (linear, very subtle transitions)
- Typography as the PRIMARY visual element

#### FORBIDDEN Elements
- ❌ Generated images
- ❌ SVG geometric shapes (circles, rectangles, polygons)
- ❌ Decorative icons or illustrations
- ❌ Color blocks or split layouts
- ❌ Any graphical ornamentation

#### Layout

```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│           PRESENTATION TITLE            │
│           ─────────────────             │
│              Subtitle Here              │
│                                         │
│         Presenter | Date | Company      │
│                                         │
└─────────────────────────────────────────┘
```

#### Font Size Hierarchy (Cover)

| Element | Recommended Size | Ratio to Base |
|---------|-----------------|---------------|
| Main Title | 72–120px | 3x–5x |
| Subtitle | 28–40px | 1.5x–2x |
| Supporting Text | 18–24px | 1x (base) |
| Meta Info (date, name) | 14–18px | 0.7x–1x |

#### Cover HTML Example

```html
<!-- Solid color background with centered typography -->
<div style="background: #0B1F3A; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
  <h1 style="color: #FFFFFF; font-size: 72px; font-weight: bold;">Presentation Title</h1>
  <p style="color: #8C8C8C; font-size: 24px; margin-top: 20px;">Subtitle or Tagline</p>
</div>
```

#### Cover Verification Checklist
- [ ] Typography is perfectly centered (horizontal and vertical)
- [ ] Text contrast is correct (white text on dark, navy text on light)
- [ ] No decorative shapes or graphics present
- [ ] Title is NOT truncated — all text fits within the slide
- [ ] Clean, elegant, professional appearance

---

### Content Page

Every content slide MUST follow this vertical structure:

```
┌─────────────────────────────────────────────────────────┐
│  HEADER BAR (Deep Navy #0B1F3A, 0.6" / 32px height)    │
│  [Page Title - White, left-aligned] [Page# - right]    │
├─────────────────────────────────────────────────────────┤
│  INSIGHT ZONE (0.1" below header)                       │
│  One-line blue bold text summarizing the key finding   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CONTENT AREA (4+ zones)                               │
│  Charts, data, bullet points, comparisons              │
│  Left/Right margins: 0.5" (26px)                       │
│  Inter-chart spacing: 0.2" (10px)                      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  FOOTER ZONE (0.4" / 21px height)                      │
│  [Data source + Date + Disclaimer - Gray #8C8C8C, 8px] │
└─────────────────────────────────────────────────────────┘
```

#### 1. Header Bar
- **Height**: 0.6" (32px)
- **Background**: Deep Navy `#0B1F3A`
- **Page Title**: Arial Black, 24px, White `#FFFFFF`, left-aligned with 0.5" padding
- **Page Number**: Right-aligned, White, 14px

```html
<div style="background: #0B1F3A; height: 32px; padding: 0 26px; display: flex; align-items: center; justify-content: space-between;">
  <h1 style="color: #FFFFFF; font-family: Arial Black, sans-serif; font-size: 24px; margin: 0;">Page Title</h1>
  <span style="color: #FFFFFF; font-size: 14px;">3</span>
</div>
```

#### 2. Insight Zone
- **Position**: 0.1" (5px) below header bar
- **Font**: Arial Bold, 16px, Cobalt Blue `#1B5AB5`
- **Content**: One-line summary of the page's key finding/insight

```html
<div style="padding: 5px 26px 10px; color: #1B5AB5; font-weight: bold; font-size: 16px;">
  Key Insight: Market grew 25% YoY driven by digital transformation initiatives
</div>
```

#### 3. Content Area
- **Left/Right Margins**: 0.5" (26px)
- **Inter-zone Spacing**: 0.2" (10px)
- **Must contain 4+ distinct zones**

#### 4. Footer Zone (MANDATORY SOURCE CITATION)
- **Height**: 0.4" (21px)
- **Font**: Arial, 8px, Medium Gray `#8C8C8C`

```html
<div style="position: absolute; bottom: 0; left: 0; right: 0; height: 21px; padding: 0 26px; font-size: 8px; color: #8C8C8C; display: flex; align-items: center;">
  Source: Goldman Sachs, Morgan Stanley | Forecasts as of early 2026 | Not investment advice
</div>
```

#### ⚠️ 4-Zone Minimum Layout (MANDATORY)

**Every content page MUST have at least 4 distinct content zones.**

##### 2x2 Grid
```
┌─────────────────┬─────────────────┐
│  Zone 1         │  Zone 2         │
│  [Chart/Stats]  │  [Bullet List]  │
├─────────────────┼─────────────────┤
│  Zone 3         │  Zone 4         │
│  [Key Finding]  │  [Comparison]   │
└─────────────────┴─────────────────┘
```

##### 1+3 Layout
```
┌─────────────────────────────────────┐
│  Zone 1: Hero Chart                 │
├───────────┬───────────┬─────────────┤
│  Zone 2   │  Zone 3   │  Zone 4     │
│  Detail 1 │  Detail 2 │  Detail 3   │
└───────────┴───────────┴─────────────┘
```

#### Content Variety (NOT JUST BULLETS)

| Format | When to Use |
|--------|-------------|
| **Prose paragraphs** | Context, analysis, explanations (2–4 sentences) |
| **Data tables** | Comparisons, specifications, metrics |
| **Bullet lists** | Action items, key takeaways, features |
| **Charts/Graphs** | Trends, distributions, relationships |
| **Callout stats** | Highlight 1–3 key numbers |
| **Process flows** | Sequential steps, workflows |

**Example of good zone variety on one page:**
- Zone 1: SVG bar chart with trend data
- Zone 2: Prose paragraph explaining context
- Zone 3: Data table with competitor comparison
- Zone 4: 3 bullet points summarizing key takeaways

#### Content Subtypes

- **Text**: bullets/quotes/short paragraphs (still add icons/shapes)
- **Mixed media**: two-column / half-bleed image + text overlay
- **Data visualization**: chart + 1–3 key takeaways + source
- **Comparison**: side-by-side columns/cards (A vs B, pros/cons)
- **Timeline / process**: steps with arrows, journey, phases
- **Image showcase**: hero image, gallery, or visual-first layout

#### Content Page Verification Checklist
- [ ] Header bar with navy background
- [ ] Insight zone with blue text
- [ ] 4+ content zones
- [ ] Footer with source citation
- [ ] Page number badge present
- [ ] **Text Overflow Check**: No text cut off at edges, no truncation with "..."
- [ ] **Whitespace Check**: No large empty gaps (>52px), 70%+ of content area filled, check right side and bottom
- [ ] **Accent Color Count**: ≤2 accent colors (excluding base colors)
- [ ] **Content Variety**: Not all bullet points — mix prose, tables, charts

---

### Table of Contents

#### Layout Options

**1. Numbered Vertical List** (best for 3–5 sections)
```
|  TABLE OF CONTENTS            |
|  01  Section Title One         |
|  02  Section Title Two         |
|  03  Section Title Three       |
```

**2. Two-Column Grid** (best for 4–6 sections)

**3. Sidebar Navigation** (modern/corporate)

**4. Card-Based Layout** (3–4 sections, creative/modern)

#### Font Size Hierarchy (TOC)

| Element | Recommended Size |
|---------|-----------------|
| Page Title ("Table of Contents" / "Agenda") | 36–44px |
| Section Number | 28–36px |
| Section Title | 20–28px |
| Section Description | 14–16px |

#### Content Elements
1. **Page Title** — Always required
2. **Section Numbers** — Consistent format (01, 02... or I, II...)
3. **Section Titles** — Clear and concise
4. **Section Descriptions** — Optional one-line summaries
5. **Page Number Badge** — MANDATORY (see Appendix G)

---

### Section Divider

**Design: Elegant & Minimal — same style as cover pages.**

#### ALLOWED Elements
- Solid color backgrounds (from the color palette)
- Subtle CSS gradients
- Typography as the PRIMARY visual element
- Centered layout only

#### FORBIDDEN Elements
- ❌ SVG geometric shapes (circles, rectangles, bars, polygons)
- ❌ Color blocks or split layouts
- ❌ Accent bars or stripes
- ❌ Decorative icons or illustrations

#### Layout
```
┌─────────────────────────────────────────┐
│                                         │
│                  02                     │
│           SECTION TITLE                 │
│         Optional intro line             │
│                                         │
└─────────────────────────────────────────┘
```

#### Font Size Hierarchy (Section Divider)

| Element | Recommended Size | Notes |
|---------|-----------------|-------|
| Section Number | 72–120px | Bold, accent color or semi-transparent |
| Section Title | 36–48px | Bold, clear, primary text color |
| Intro Text | 16–20px | Light weight, muted color, optional |

**Page Number Badge is MANDATORY** (see Appendix G).

---

### Summary / Closing Page

#### Layout Options

**1. Key Takeaways** — 3–5 key points with icons or numbered markers

**2. CTA / Next Steps** — Clear call-to-action prominently displayed

**3. Thank You / Contact** — Closing message with contact info

**4. Split Recap** — Left: key takeaways; Right: CTA/contact

#### Font Size Hierarchy (Summary)

| Element | Recommended Size |
|---------|-----------------|
| Closing Title ("Thank You" / "Summary") | 48–72px |
| Takeaway / Action Item | 18–24px |
| Supporting Text | 14–16px |
| Contact Info | 14–16px |

**Page Number Badge is MANDATORY** (see Appendix G).

---

## Chart & Data Visualization Rules (MANDATORY)

### General Chart Rules

1. **No outer borders** on any chart
2. **Light gray grid lines** (`#E0E0E0`)
3. **Y-axis starts from zero** (unless specifically noted)
4. **Data labels directly on charts** to reduce legend lookup cost
5. **Legend position**: Below chart or right side, 9px font
6. **Square corners on ALL bars** — NO `rx`/`ry` attributes

### Bar/Column Chart

- **Corner radius**: 0 (SQUARE corners — NO rounded edges)
- **Bar width ratio**: 70% of available space
- **Use chart series colors in order**
- **NO rx/ry attributes on rect elements**

```html
<svg width="300" height="150" viewBox="0 0 300 150">
  <!-- Grid lines -->
  <line x1="40" y1="20" x2="280" y2="20" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="50" x2="280" y2="50" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="80" x2="280" y2="80" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="110" x2="280" y2="110" stroke="#E0E0E0" stroke-width="1"/>

  <!-- Bars (no rounded corners, 70% width) -->
  <rect x="50" y="30" width="40" height="80" fill="#1B5AB5"/>
  <rect x="110" y="50" width="40" height="60" fill="#2E8BC0"/>
  <rect x="170" y="20" width="40" height="90" fill="#D4A843"/>
  <rect x="230" y="40" width="40" height="70" fill="#E05252"/>

  <!-- Data labels directly on bars -->
  <text x="70" y="25" text-anchor="middle" fill="#2D2D2D" font-size="9">85%</text>
  <text x="130" y="45" text-anchor="middle" fill="#2D2D2D" font-size="9">62%</text>
  <text x="190" y="15" text-anchor="middle" fill="#2D2D2D" font-size="9">92%</text>
  <text x="250" y="35" text-anchor="middle" fill="#2D2D2D" font-size="9">71%</text>

  <!-- X-axis labels -->
  <text x="70" y="125" text-anchor="middle" fill="#2D2D2D" font-size="9">Q1</text>
  <text x="130" y="125" text-anchor="middle" fill="#2D2D2D" font-size="9">Q2</text>
  <text x="190" y="125" text-anchor="middle" fill="#2D2D2D" font-size="9">Q3</text>
  <text x="250" y="125" text-anchor="middle" fill="#2D2D2D" font-size="9">Q4</text>
</svg>
```

### Line Chart

- **Line width**: 2px
- **Data points**: Small circles (r=3)
- **Use chart series colors in order**

```html
<svg width="300" height="150" viewBox="0 0 300 150">
  <line x1="40" y1="20" x2="280" y2="20" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="50" x2="280" y2="50" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="80" x2="280" y2="80" stroke="#E0E0E0" stroke-width="1"/>
  <line x1="40" y1="110" x2="280" y2="110" stroke="#E0E0E0" stroke-width="1"/>

  <polyline points="50,90 110,70 170,40 230,55" fill="none" stroke="#1B5AB5" stroke-width="2"/>

  <circle cx="50" cy="90" r="3" fill="#1B5AB5"/>
  <circle cx="110" cy="70" r="3" fill="#1B5AB5"/>
  <circle cx="170" cy="40" r="3" fill="#1B5AB5"/>
  <circle cx="230" cy="55" r="3" fill="#1B5AB5"/>

  <text x="50" y="85" text-anchor="middle" fill="#2D2D2D" font-size="9">$2.1M</text>
  <text x="110" y="65" text-anchor="middle" fill="#2D2D2D" font-size="9">$2.8M</text>
  <text x="170" y="35" text-anchor="middle" fill="#2D2D2D" font-size="9">$4.2M</text>
  <text x="230" y="50" text-anchor="middle" fill="#2D2D2D" font-size="9">$3.5M</text>
</svg>
```

### Progress Bar (NO ROUNDED CORNERS)

```html
<div style="margin-bottom: 8px;">
  <div style="display: flex; justify-content: space-between; font-size: 10px; color: #2D2D2D; margin-bottom: 3px;">
    <span>Market Share</span>
    <span>75%</span>
  </div>
  <!-- NO border-radius - square corners only -->
  <div style="background: #E0E0E0; height: 8px; width: 100%; border-radius: 0;">
    <div style="background: #1B5AB5; height: 100%; width: 75%; border-radius: 0;"></div>
  </div>
</div>
```

### Pie Charts — Image Generation Tool is MANDATORY

**Pie charts MUST be created using the image generation tool.** SVG pie charts require arc commands (`A`) which are forbidden for PPTX conversion. ALL workarounds (layered circles, stroke-dasharray, clip-paths, conic-gradient, rotated segments) WILL FAIL during PPTX conversion.

---

## HTML Implementation Specification

### Appendix A — Responsive Scaling Snippet (REQUIRED)

Every slide HTML file MUST include this snippet:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
}
.slide-content {
  width: 960px;
  height: 540px;
  position: relative;
  transform-origin: center center;
}
</style>
<script>
function scaleSlide() {
  const slide = document.querySelector('.slide-content');
  if (!slide) return;
  const slideWidth = 960;
  const slideHeight = 540;
  const scaleX = window.innerWidth / slideWidth;
  const scaleY = window.innerHeight / slideHeight;
  const scale = Math.min(scaleX, scaleY);
  slide.style.width = slideWidth + 'px';
  slide.style.height = slideHeight + 'px';
  slide.style.transform = `scale(${scale})`;
  slide.style.transformOrigin = 'center center';
  slide.style.flexShrink = '0';
}
window.addEventListener('load', scaleSlide);
window.addEventListener('resize', scaleSlide);
</script>
```

### Appendix B — CSS Rules (REQUIRED)

#### ⚠️ Inline-Only CSS

**All CSS styles MUST be inline (except the snippet in Appendix A).**

- Do NOT use `<style>` blocks outside Appendix A
- Do NOT use external stylesheets
- Do NOT use CSS classes or class-based styling

```html
<!-- ✅ Correct: Inline styles -->
<div style="position:absolute; left:60px; top:120px; width:840px; height:240px; background:#023047;"></div>

<!-- ❌ Wrong: Style blocks or classes -->
<style>.card { background:#023047; }</style>
<div class="card"></div>
```

#### ⚠️ Background on .slide-content Directly

**Do NOT create a full-size background DIV inside `.slide-content`.** Set background directly on `.slide-content` itself.

```html
<!-- ✅ Correct -->
<div class="slide-content" style="background:#FFFFFF;">
  <p style="position:absolute; left:60px; top:140px; ...">Title</p>
</div>

<!-- ❌ Wrong: Nested background DIV -->
<div class="slide-content">
  <div style="position:absolute; left:0; top:0; width:960px; height:540px; background:#FFFFFF;"></div>
</div>
```

#### ⚠️ No Bold for Body Text and Captions

Reserve bold (`font-weight: 600+`) for titles, headings, and key emphasis only. Body text, captions, legends, and footnotes must use normal weight (400–500).

### Appendix C — Color Palette Rules (REQUIRED)

- **Strictly use the provided color palette.** Do NOT create or modify color values.
- **Only exception**: You may add opacity to palette colors for overlays (e.g., `rgba(r,g,b,0.1)`)
- **No gradients on content pages** — No CSS `linear-gradient()`, `radial-gradient()`, `conic-gradient()` on content slides
- **No animations** — No CSS `animation`, `@keyframes`, `transition`, hover effects, or SVG `<animate>`

### Appendix D — SVG Conversion Constraints (CRITICAL)

#### Supported SVG Elements (WHITELIST)
- ✅ `<rect>` — rectangles (with `rx`/`ry` for rounded corners)
- ✅ `<circle>` — circles
- ✅ `<ellipse>` — ellipses
- ✅ `<line>` — straight lines
- ✅ `<polyline>` — connected line segments (stroke only, NO fill)
- ✅ `<polygon>` — closed polyline (stroke only, NO fill)
- ✅ `<path>` — **ONLY with M/L/H/V/Z commands**
- ✅ `<pattern>` — repeating patterns

#### `<path>` Command Restrictions (CRITICAL)

**ONLY these commands are supported:**
- ✅ `M/m` — moveTo
- ✅ `L/l` — lineTo
- ✅ `H/h` — horizontal line
- ✅ `V/v` — vertical line
- ✅ `Z/z` — close path

**FORBIDDEN commands (will cause SVG to be SKIPPED in PPTX):**
- ❌ `Q/q` — quadratic Bézier curve
- ❌ `C/c` — cubic Bézier curve
- ❌ `S/s` — smooth cubic Bézier
- ❌ `T/t` — smooth quadratic Bézier
- ❌ `A/a` — elliptical arc

#### Additional SVG Constraints
- ❌ **NO rotated shapes** — `transform="rotate()"` on shapes causes fallback failure
- ❌ **NO `<text>` in complex SVGs** — SVG text becomes rasterized, not editable in PPTX
- ❌ **Filled `<path>` must be rectangles** — if a path has fill, it must form a closed rectangle with only M/L/H/V/Z
- ⚠️ **Gradients in SVG are DISCOURAGED** — technically supported but can break

#### Workaround: Approximate Curves with Line Segments

```html
<!-- ⚠️ WORKAROUND: Approximate curves with line segments -->
<svg width="200" height="20">
  <path d="M0 10 L12 6 L25 4 L37 6 L50 10" stroke="#dda15e" stroke-width="2"/>
</svg>
```

### Appendix E — Advanced SVG Techniques

- **SVG is for decorative elements ONLY** — it does NOT satisfy "real image" requirements
- Prefer SVG for all decorative shapes (lines/dividers, corner accents, badges, frames, arrows)
- Use SVG when pixel-crisp geometry is needed under `transform: scale()`
- **Background shapes MUST use SVG** `<rect>` or `<path>`, NOT CSS `background`/`border`
- **Dividers MUST use SVG**, NOT CSS `background`, `border`, or `<hr>`

#### SVG Badge Example (Text INSIDE SVG)

```html
<!-- ✅ Correct: Text inside SVG -->
<svg width="180" height="52" viewBox="0 0 180 52">
  <rect width="180" height="52" rx="26" fill="#fb8500"/>
  <text x="90" y="26" text-anchor="middle" dominant-baseline="central"
        font-size="16" font-weight="700" fill="#ffffff">LABEL</text>
</svg>

<!-- ❌ Wrong: Text overlaid on SVG (WILL BE LOST in PPTX) -->
<div class="badge">
  <svg><rect .../></svg>
  <span style="position:absolute;">LABEL</span>
</div>
```

#### SVG Background Patterns

```html
<!-- Dot grid pattern -->
<svg width="100%" height="100%" style="position:absolute;top:0;left:0;opacity:0.08;pointer-events:none;">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="2" fill="currentColor"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#dots)"/>
</svg>
```

#### SVG Icons (Supported Patterns)

```html
<!-- Checkmark icon (polyline - SUPPORTED) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
  <polyline points="20 6 9 17 4 12"/>
</svg>

<!-- Simple arrow icon (M/L path - SUPPORTED) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M5 12 L19 12 M12 5 L19 12 L12 19"/>
</svg>
```

#### SVG Implementation Tips
- Add `vector-effect="non-scaling-stroke"` to keep stroke widths stable under scaling
- For thin lines, prefer filled rectangles over stroked lines
- Use `overflow="visible"` when SVG extends beyond its box
- Use `aria-hidden="true"` for decorative SVGs
- Use `currentColor` for easy theming
- Use `pointer-events: none` for overlay SVGs

### Appendix F — HTML2PPTX Validation Rules (REQUIRED)

#### Layout and Dimensions
- Slide content must not overflow the body (no scroll)
- Text elements larger than 12pt must be at least 0.5" above the bottom edge
- HTML body dimensions must match presentation layout size

#### Backgrounds and Images
- Do NOT use CSS gradients
- Do NOT use `background-image` on `div` elements
- For slide backgrounds, use a real `<img>` element as background
- Solid background colors on a dedicated shape/div element

#### Text Elements
- `p`, `h1`–`h6`, `ul`, `ol`, `li` must NOT have background, border, or shadow
- Inline elements (`span`, `b`, `i`, `u`, `strong`, `em`) must NOT have margins
- Do NOT use manual bullet symbols — use `<ul>` or `<ol>` lists
- Do NOT leave raw text directly inside `div` — wrap in text tags

#### SVG and Text
- Do NOT place text (`<span>`, `<p>`) as overlay on SVG — it will be lost in PPTX
- Text on SVG shapes must use `<text>` element inside the SVG
- SVG `<text>` must use `text-anchor="middle"` and `dominant-baseline="central"`

#### Placeholders
- Elements with class `placeholder` must have non-zero width and height

### Appendix G — Page Number Badge (REQUIRED)

All slides **except Cover Page** MUST include a page number badge. Shows current slide number in bottom-right corner.

- **Position**: `position:absolute; right:32px; bottom:24px;`
- **Must use SVG** (text inside `<text>`, not overlaid `<span>`)
- Colors from palette only; keep it subtle; same style across all slides
- Show current number only (e.g. `3` or `03`), **not** "3/12"

```html
<!-- ✅ Circle badge (default) -->
<svg style="position:absolute; right:32px; bottom:24px;" width="36" height="36" viewBox="0 0 36 36">
  <circle cx="18" cy="18" r="18" fill="#1B5AB5"/>
  <text x="18" y="18" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-weight="600" fill="#ffffff">3</text>
</svg>

<!-- ✅ Pill badge -->
<svg style="position:absolute; right:32px; bottom:24px;" width="48" height="28" viewBox="0 0 48 28">
  <rect width="48" height="28" rx="14" fill="#1B5AB5"/>
  <text x="24" y="14" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-weight="600" fill="#ffffff">03</text>
</svg>

<!-- ✅ Minimal (number only) -->
<p style="position:absolute; right:36px; bottom:24px; margin:0; font-size:13px; font-weight:500; color:#1B5AB5;">03</p>
```

---

## No Excessive Whitespace (MANDATORY CHECK)

**Every page must be information-dense.** Avoid large empty areas.

| Check | Requirement |
|-------|-------------|
| **Content Coverage** | At least 70% of the content area must contain meaningful content |
| **Gap Size** | No single empty gap larger than 1" (52px) in any direction |
| **Zone Balance** | All 4+ zones should have substantial content, not filler |

**During page verification, check for:**
- Large empty margins between zones
- Sparse content zones (single bullet point only)
- Unbalanced layouts (one zone full, others empty)
- Content that could be expanded to fill space

---

## Slide Page Type Classification

Classify **every slide** as **exactly one** of these 5 page types:

1. **Cover Page** — Opening + tone setting
2. **Table of Contents** — Navigation + expectation setting (3–5 sections)
3. **Section Divider** — Clear transitions between major parts
4. **Content Page** — Data-rich slides (pick a subtype)
5. **Summary / Closing Page** — Wrap-up + action

---

## Common Mistakes to Avoid

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need clear differentiation from body text
- **Don't use colors outside the palette** — strictly use provided color values
- **Don't mix spacing randomly** — choose consistent gaps
- **Don't create text-only slides** — add charts, data tables, or visual elements
- **Don't forget text box padding** — account for padding when aligning shapes with text
- **Don't use low-contrast elements** — icons AND text need strong contrast against background
- **NEVER use accent lines under titles** — hallmark of AI-generated slides; use whitespace instead
- **NEVER use rounded corners** — all elements must have `border-radius: 0`
- **NEVER skip source citations** — every data slide needs a footer citation
- **NEVER exceed 2 accent colors per page** (except multi-series charts)
- **NEVER use generated images for decoration** — SVG charts only

---

## Verification Workflow (MANDATORY for Every Slide)

After generating each slide's HTML, verify using screenshots:

1. **Layout Structure**: Correct header/insight/content/footer zones
2. **Text Overflow/Truncation**: No text cut off, no "..." truncation
3. **Whitespace**: No large empty gaps, 70%+ fill rate, check right side and bottom
4. **Accent Colors**: Count ≤2 (excluding base colors)
5. **Content Variety**: Not all bullet points
6. **Square Corners**: No border-radius anywhere
7. **Source Citation**: Footer citation present on data slides
8. **Page Number Badge**: Present on all non-cover slides

**If ANY issue is found, FIX immediately before proceeding to the next slide.**
