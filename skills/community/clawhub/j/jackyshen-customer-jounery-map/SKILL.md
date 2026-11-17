---
name: customer-journey-map
description: "Use this skill whenever you want to visualize customer journeys, employee experiences, or service blueprints with stages, touchpoints, behaviors, emotions, pain points, and opportunities. Perfect for e-commerce promotions, B2B sales funnels, or any multi-stage experience mapping. Generates clean SVG/PNG/PDF exports with stage-based rows layout, consulting-style."
compatibility: Python, Pydantic, Jinja2, Playwright
---

# Customer Journey Map Skill

## What This Skill Does

Converts structured customer journey, employee journey, experience map, service blueprint, or similar flow data into high-quality SVG visualizations with multi-format export (SVG/PNG/PDF).

The core principle: **data drives rendering, not Markdown拼接 or Mermaid.**

---

## Input Format

### Primary: YAML (Stage-Based)

```yaml
journey_name: 电商促销活动用户旅程
stages:
  - id: awareness
    name: 触发
    touchpoints:
      - 短信
      - 邮件
      - 消息
    behaviors:
      - 打开消息
      - 删除消息
    emotions:
      - 优惠券快到期了
      - 推销短信太烦人了
    pain_points:
      - 触达渠道不对
      - 触达内容不相关
    opportunities:
      - 根据历史消费行为精准营销
      - 个人定制消息推送
  - id: explore
    name: 探索
    ...
```

### Secondary: Touchpoint List (Score-Based Legacy)

```yaml
title: 宜家客户旅程图
touchpoints:
  - name: 商场位置与外观
    score: 3
    stage: 到达
    action: 驾车前往/查找位置
    thought: 好不好找停车位？
    emotion: neutral
    opportunity: 优化交通指引和停车指引
```

---

## Data Model

### Stage-Based Input (Primary)

```python
class StageInfo(BaseModel):
    id: str
    name: str
    touchpoints: list[str]
    behaviors: list[str]
    emotions: list[str]
    pain_points: list[str]
    opportunities: list[str]

class EcommerceJourneyInput(BaseModel):
    journey_name: str
    stages: list[StageInfo]
    flow: list[str]
```

### Touchpoint-Based Input (Legacy)

```python
class TouchPoint(BaseModel):
    name: str
    score: float = Field(ge=1.0, le=5.5)
    stage: str | None = None
    action: str | None = None
    thought: str | None = None
    emotion: str | None = None
    opportunity: str | None = None
    tags: list[str] = []

class JourneyMap(BaseModel):
    title: str
    type: str = "customer"
    touchpoints: list[TouchPoint]
```

---

## Rendering Pipeline

```
User Input (YAML)
    ↓
Schema Parser (parser.py)
    ↓
Render Model (svg_renderer.py / Jinja2)
    ↓
SVG (authoritative format)
    ↓
Export: PNG (Playwright) / PDF (Playwright)
```

**Rule: SVG is the single source of truth.** PNG and PDF MUST be generated from SVG.

---

## Canvas & Layout

| Parameter | Default |
|-----------|---------|
| Canvas | 2400 × 900 (min) |
| Top margin | 120 |
| Left margin | 180 |
| Right margin | 80 |
| Bottom margin | 120 |

### Row Structure (Y-Axis)

Unlike a line chart, the Y-axis represents **horizontal rows** for each touchpoint:

| Row | Content |
|-----|---------|
| 阶段 (Stage) | Stage name + stage marker |
| 服务触点 (Touchpoint) | Touchpoint name |
| 想法和疑虑 (Thoughts) | User thoughts and doubts |
| 感受和情绪 (Emotions) | Emotional response (positive/negative/neutral) |

### Stage Grouping

Each stage's touchpoints are grouped together with visual separators. The journey flows left-to-right across stages.

### Satisfaction Bands (Optional, Legacy)

For touchpoint-based input with score field:

| Score | Zone |
|-------|------|
| 5.5 | 非常满意 |
| 5 | 满意 |
| 3 | 一般满意 |
| 2 | 不满意 |
| 1 | 非常不满意 |

---

## Line & Node Specs

**Journey line:**
- Color: #333333
- Style: smooth (Bezier curves), or straight-line mode
- Stroke width: 3px

**Touchpoint nodes:**
- Circle, radius 8px
- Fill: #333333
- Stroke: #333333

**Stage markers:**
- Vertical dotted lines to separate stages
- Stage name labels at top or bottom

---

## Typography

- Primary font: Noto Sans CJK (Chinese/English/Japanese)
- Fallback: system CJK → sans-serif
- Font strategy: embed in SVG or rely on system fonts with graceful degradation

---

## Export Specs

Use MCP provided playwright by default.

### PNG (via Playwright)

```
SVG → HTML wrapper → Chromium → PNG
```

### PDF (via Playwright)

```
SVG → HTML wrapper → Chromium → PDF
```

Requirements:
- Chinese font rendering preserved
- Background colors preserved
- Vector quality maintained

---

## Default Theme: Consulting

McKinsey / Bain / BCG style:
- Clean, minimal, professional
- Printable, no decorative elements
- Muted color palette

---

## Required Project Structure

```
journey_map_schema.py       # Pydantic models
journey_map_parser.py       # YAML + Markdown table parser
journey_map_svg_renderer.py # Jinja2 + SVG generation
journey_map_v3.svg.j2      # Template
journey_map_png_exporter.py # Playwright PNG export
journey_map_pdf_exporter.py # Playwright PDF export
```

---

## Output Files

Always produce:
1. `journey_map.svg` — the authoritative rendering
2. `journey_map.png` — preview image
3. `journey_map.pdf` — deliverable document

---

## Layout Principles

1. **Stage-based rows** — Y-axis displays: Stage name, Touchpoint name, Thoughts, Emotions (not satisfaction score)

2. **Horizontal flow** — Journey flows left-to-right, grouped by stages

3. **Abstraction over hardcoding** — Framework supports: Customer Journey Map, Employee Journey, Experience Map, Service Blueprint, Stakeholder Journey, Change Journey

4. **Extensibility** — Future support for: PPTX, HTML, Notion embed