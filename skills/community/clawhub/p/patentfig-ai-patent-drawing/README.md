# PatentFig AI — Agent Skill

An [Agent Skill](https://agentskills.io) that teaches AI agents (Claude Code, Claude.ai, and other SKILL.md-compatible agents) how to call the [PatentFig AI](https://patentfig.ai) API:

- **Generate patent figures from text** — USPTO/EPO-style line art as PNG or SVG, with optional reference numerals and reference images
- **Vectorize** raster drawings to SVG / DXF / vector PDF (line-art redraw or faithful trace)
- **AI-upscale** images 2×/4× with 300/600 DPI metadata
- **Convert** to filing-ready TIFF / PDF / PNG

## Install

**Claude Code** — copy into your skills directory:

```bash
git clone https://github.com/TopLocalAI/patentfig-skill.git ~/.claude/skills/patentfig
```

Or with the [skills CLI](https://skills.sh):

```bash
npx skills add TopLocalAI/patentfig-skill
```

## Setup

1. Create an API key at [patentfig.ai/settings/api-keys](https://patentfig.ai/settings/api-keys)
2. Export it:

```bash
export PATENTFIG_API_KEY="pfig_..."
```

Then ask your agent things like:

> "Generate an exploded-view patent figure of a coffee grinder with numbered parts, as SVG."

> "Vectorize drawing.png to DXF so I can edit it in AutoCAD."

## Pricing

API calls draw from your PatentFig AI credit balance — generation 10 credits, conversion endpoints 20 credits, balance lookup free. Credits are only charged on success. See [patentfig.ai/pricing](https://patentfig.ai/pricing).

## Links

- Docs: https://patentfig.ai/docs
- OpenAPI spec: https://patentfig.ai/api/openapi.yaml
- Developers: https://patentfig.ai/developers
- Support: contact@patentfig.ai

## License

MIT © TopLocalAI, LLC. The skill instructions are open source; API usage is governed by the [PatentFig AI terms](https://patentfig.ai/terms-of-service).
