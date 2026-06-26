# Powerpoint-Generator

> Professional Full-Process PPT Presentation AI Generation Assistant

**[English](README.md)** | [中文](README_CN.md)

---

**Powerpoint-Generator** mimics the complete workflow of a professional PPT design company (priced at 10,000+ RMB per page), automating everything from requirements research to post-processing SVG+PPTX, outputting professional-grade HTML presentations + editable vector PPTX files.

---

## Recent Updates

`2026-04-10 · v2.0`

- Added 8 new theme styles (Gradient Blue / Warm Sunset / Nordic White / Cyber Punk / Elegant Gold / Ocean Depth / Retro Film / Corporate Blue)
- Added 4 new card types (feature_grid / image_text / data_highlight / stat_block)
- Removed exec bypass code, strengthened degradation strategy
- Separated English and Chinese SKILL.md

---

## Workflow

```
Step 1 Requirements Interview  →  Step 2 Information Gathering  →  Step 3 Outline Planning
     ↓
Step 4 Content Allocation + Planning Draft  →  Step 5 Style + Illustrations + HTML Design
     ↓
Step 6 Post-processing (HTML → SVG → PPTX)
```

---

## Demo Showcase

> Example output for "New Xiaomi SU7 Launch" theme (Xiaomi Orange style):

| Cover | Configuration Comparison |
|:---:|:---:|
| ![Cover](ppt-output/png/slide_01_cover.png) | ![Comparison](ppt-output/png/slide_02_models.png) |

| Power & Range | Smart Driving & Safety |
|:---:|:---:|
| ![Power](ppt-output/png/slide_03_power.png) | ![Smart](ppt-output/png/slide_04_smart.png) |

| End Page |
|:---:|
| ![End](ppt-output/png/slide_05_end.png) |

---

## Key Features

| Feature | Description |
|---------|-------------|
| **6-Step Professional Pipeline** | Requirements → Research → Outline → Planning → Design → Post-processing, simulating professional PPT company workflow |
| **16 Preset Styles** | Dark Tech / Xiaomi Orange / Blue White / Royal Red / Fresh Green / Luxury Purple / Minimal Gray / Vibrant Rainbow / Gradient Blue / Warm Sunset / Nordic White / Cyber Punk / Elegant Gold / Ocean Depth / Retro Film / Corporate Blue |
| **7 Bento Layouts** | Single Focus / 50/50 Symmetric / Asymmetric Two-column / Three-column Equal Width / Primary-Secondary / Hero with Sub-items / Mixed Grid |
| **12 Card Types** | text / data / list / tag_cloud / process / timeline / comparison / quote / stat_block / feature_grid / image_text / data_highlight |
| **Smart Illustrations** | AI generation / Unsplash library + 5 visual fusion techniques (fade blend / tinted overlay / ambient background / crop viewport / circular crop) |
| **Cross-page Narrative** | Density alternation / chapter color progression / cover-ending echo / progressive revelation |
| **Dual PPTX Export** | SVG PPTX (editable vectors) + PNG PPTX (pixel-perfect fidelity) — HTML → SVG/PNG → PPTX pipeline |

---

## Quick Start

Just describe your needs in the conversation to trigger the skill. The Agent will automatically execute the full workflow:

> *"Make a 15-page roadshow deck about 2026 embodied AI trends, dark tech style"*

All outputs are saved to `ppt-output/`, including browser preview and dual-format PPTX.

---

## Requirements

**Required:**
- **Node.js** >= 18
- **Python** >= 3.8
- **python-pptx / lxml / Pillow**

**Quick Install:**
```bash
pip install python-pptx lxml Pillow
npm install puppeteer dom-to-svg
```

**Optional (for illustrations):**
Configure `.env` file with `UNSPLASH_ACCESS_KEY`, or use text/data-driven design without it.

---

## Directory Structure

```
Powerpoint-Generator/
├── SKILL.md              # Main workflow instructions (Agent entry point, English)
├── skill_cn.md          # Main workflow instructions (Chinese)
├── README.md             # English documentation
├── README_CN.md          # Chinese documentation
├── .env.example          # Environment variable template
├── references/
│   ├── prompts.md        # 5 Prompt templates
│   ├── style-system.md   # 16 styles + CSS variables
│   ├── bento-grid.md     # 7 layouts + 12 card types
│   ├── method.md         # Core methodology
│   └── pipeline-compat.md # Pipeline compatibility rules
└── scripts/
    ├── html_packager.py  # HTML merge preview
    ├── html2svg.py       # HTML → SVG
    ├── html2png.py       # HTML → PNG (Puppeteer screenshot)
    ├── svg2pptx.py       # SVG → PPTX (editable)
    ├── png2pptx.py       # PNG → PPTX (pixel-perfect)
    ├── contract_validator.py   # Contract validation
    ├── planning_validator.py   # Planning JSON validation
    ├── milestone_check.py      # Milestone checker
    ├── prompt_harness.py       # Dynamic prompt generator
    ├── resource_loader.py      # Resource router
    ├── visual_qa.py           # Visual QA (screenshot + audit)
    └── subagent_logger.py      # Subagent runtime logger
```

---

## Usage Examples

| Scenario | What to Say |
|----------|-------------|
| Topic only | "Make a PPT about X" / "Create a presentation on Y" |
| With source material | "Turn this document into slides" / "Make a PPT from this report" |
| With requirements | "15-page dark tech style AI safety presentation" |
| Implicit trigger | "I need to present to my boss about Y" / "Make training materials" / "Make a roadshow deck" |

---

## Acknowledgments

This project is based on [ppt-agent-skill](https://github.com/Akxan/ppt-agent-skill). We thank the original project author for their excellent work and open source spirit.

## License

[MIT](LICENSE)
