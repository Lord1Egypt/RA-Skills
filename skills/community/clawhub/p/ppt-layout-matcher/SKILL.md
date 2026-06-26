---
name: PPT Layout Matcher
description: |
  Intelligent PPT layout matching system based on a 45-page design layout library (16:9).
  Analyzes input content and automatically recommends the best slide layout from 10 categories.
  Trigger when user says: "做PPT", "创建PPT", "生成PPT", "版式匹配", "选版式", "PPT排版",
  or provides content that needs to be turned into presentation slides.
  Core capability: analyze content → match layout → create slides with python-pptx.
agent_created: true
tags:
  - ppt
  - presentation
  - layout
  - design
  - template
  - slide
  - 16:9
version: 1.0.0
---

# PPT Layout Matcher

Intelligent layout matching for PowerPoint presentations based on a 45-page professional design layout library.

## When to Use

- User wants to create a PPT from content
- User asks "which layout should I use for this content?"
- User provides bullet points / data / flow descriptions and wants them turned into slides
- User mentions "PPT", "presentation", "slides", "版式", "排版"

## Workflow

### Step 1: Analyze Content Structure

Extract key features from user input:
- Number of items (3 key metrics? 4 steps? 2 comparisons?)
- Content nature (data/metrics, process/steps, comparison, gallery, list)
- Presence of numbers/charts/images
- Timeline/step indicators

### Step 2: Run Matching Algorithm

Execute the bundled script to get layout recommendations:

```bash
python3 ppt_layout_matcher.py
```

Or use the Python API:

```python
from ppt_layout_matcher import recommend_layout
results = recommend_layout("user content here", top_k=3)
for template, score, analysis in results:
    print(f"{template.name} (Slide {template.slide_ref}) - Score: {score}")
```

### Step 3: Present Top 3 to User

Show:
- Layout name and reference slide number
- Match score
- Structure description
- Why this layout was recommended

Let the user confirm before creating.

### Step 4: Create PPT with python-pptx

Once confirmed, create the slide:
- 16:9 dimensions (13.33" × 7.50")
- Dark theme (deep blue/gray background)
- White text, accent colors for data highlights
- Follow the reference layout structure from `references/layout_templates.md`

### Step 5: QA

Verify with markitdown:
```bash
python -m markitdown output.pptx | head -100
```

## Layout Categories (Quick Reference)

| Category | Count | Use Case |
|----------|:-----:|----------|
| A-Cover | 2 | Report cover, proposal front page |
| B-Divider | 2 | Section transitions |
| C-Data Display | 9 | Metrics, charts, data highlights |
| D-Process/Steps | 6 | STEP flows, development stages |
| E-Comparison | 5 | A/B comparison, multi-solution, SWOT |
| F-Grid/Cards | 8 | 2×2, 3×2, 4×N card grids |
| G-Gallery | 1 | Image gallery, timeline |
| H-List/Points | 4 | Numbered lists, text+image lists |
| I-Infographic | 1 | One Pager overview |
| J-Special | 7 | Radial, wraparound, mixed layouts |

## Design Conventions

- Title bar: top 0.3-1.0" area
- Content area: 1.2"-7.0"
- Footer: 6.5"-7.2"
- Margins: ≥0.5" on all sides
- Heading: 20-30pt Bold, Body: 10-14pt, Big Numbers: 36-60pt Bold
- Dark background, white text, accent colors for highlights

## References

Full layout library documentation: `references/layout_templates.md`
