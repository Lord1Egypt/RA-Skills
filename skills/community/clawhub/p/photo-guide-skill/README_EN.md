# photo-guide-skill

[![license](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

[简体中文](./README.md)

> Upload a photo, learn how to shoot it, edit it, and master it.

A photography analysis Skill built for beginners. Based on the AgentSkills open standard, compatible with Claude Code, OpenClaw, and other AI Agents that support Skills.

## What Does It Do?

| Feature | Description |
|---------|-------------|
| EXIF Extraction | Automatically reads real shooting parameters (aperture, shutter speed, ISO, focal length, camera model) |
| 5-Dimension Visual Analysis | Infers shooting parameters from depth of field, motion, lighting, color, and composition |
| Style Matching | Categorizes photos into 10 common photography style templates and cross-validates parameters |
| Post-Processing Guidance | Provides tone direction, exposure adjustments, contrast suggestions, and preset keywords |
| Beginner Learning Tips | Offers actionable learning keywords to help you get started quickly |

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install the Skill

Copy or symlink the `photo-guide-skill` directory to your Agent Skills directory:

```bash
# Claude Code example
cp -r photo-guide-skill ~/.claude/skills/

# Or use a symbolic link
ln -s $(pwd)/photo-guide-skill ~/.claude/skills/photo-guide-skill
```

### Usage

Upload a photo in your Agent conversation and ask:

- "How was this photo taken?"
- "Teach me to shoot this effect"
- "What aperture/shutter speed was used here?"
- "How do I get this color tone?"
- "Help me analyze this photo"

## Directory Structure

```
photo-guide-skill/
├── SKILL.md                          # Main skill entry (triggers, workflow, output template)
├── README.md                         # Project documentation (Chinese)
├── README_EN.md                      # Project documentation (English, this file)
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
├── .gitignore
├── references/                       # Knowledge base
│   ├── photography-basics.md         # Photography parameter reference tables
│   ├── style-templates.md            # 10 photography style templates
│   └── post-processing-guide.md      # Post-processing color grading tutorial
├── scripts/                          # Utility scripts
│   └── extract_exif.py               # EXIF metadata extraction script
└── examples/                         # Sample analysis reports
    ├── test1.jpeg / test1.md         # Example 1: Architecture/religious details
    ├── test2.jpg  / test2.md         # Example 2: Landscape architecture
    └── test3.jpg  / test3.md         # Example 3: Seascape (no EXIF, visual inference only)
```

## Workflow

```
User uploads photo + asks question
        │
        ▼
  ① Extract EXIF ─── Has EXIF ──→ Record real parameters as baseline
        │
     No EXIF
        │
        ▼
  ② 5-Dimension Visual Analysis (depth of field / motion / lighting / color / composition)
        │
        ▼
  ③ Match style template, cross-validate parameters
        │
        ▼
  ④ Generate structured analysis report
     ├── Scene overview
     ├── Shooting parameters (inferred vs. actual comparison)
     ├── Shooting technique tips
     ├── Photo optimization suggestions
     ├── Post-processing color grading advice
     └── Recommended learning keywords
```

## Analysis Report Example

```
📷 Photo Analysis Report
━━━━━━━━━━━━━━━

📋 Scene Overview
- Photo type: Seascape
- Main elements: Rock pillars in the sea, waves, sky
- Shooting environment: Outdoors, dusk

⚙️ Shooting Parameters
| Parameter     | Estimated       | Reasoning                      |
| ------------- | --------------- | ------------------------------ |
| Aperture      | f/8 - f/11      | Overall sharp, large depth of field |
| Shutter Speed | 1/2s - 2s       | Silky water surface effect     |
| ISO           | 100 - 200       | Fine quality, no visible noise |
| Focal Length  | 24mm - 35mm     | Wide-angle view covering foreground rocks |
| Shooting Angle| Low angle, eye-level | Rock pillars appear majestic  |

💡 Shooting Technique Tips
- Use a tripod + slow shutter for silky water effect
- Low angle enhances the visual impact of rock pillars

🎨 Post-Processing Suggestions
- Tone direction: Cool with warm shift, sunset atmosphere
- Recommended style preset: Long Exposure Seascape

📚 Recommended Learning Keywords
- Long exposure seascape photography
- ND filter usage
```

## Design Principles

1. **Inference first, EXIF second** — Most online images lack EXIF; visual inference is the core capability
2. **Ranges over fixed values** — e.g., `f/2.0 - f/2.8`, since the same effect can be achieved with multiple parameter combinations
3. **Beginner-friendly** — Acknowledge strengths first, then suggest improvements; explain jargon briefly
4. **Practical focus** — Emphasize "how to shoot" rather than theory

## Dependencies

- Python 3.10+
- Pillow >= 9.0.0 (EXIF extraction)

See [requirements.txt](requirements.txt).

## Compatibility

Follows the [AgentSkills](https://agentskills.io/home) open standard. Compatible with:

- Claude Code
- OpenClaw
- Other AI Agents supporting the AgentSkills standard

## License

[MIT License](LICENSE)

Copyright (c) 2026 dcison
