# Photo Edit Analysis

[![ClawHub](https://img.shields.io/badge/ClawHub-photo--edit--analysis-blue)](https://clawhub.com/pfrederiksen/photo-edit-analysis)
[![Version](https://img.shields.io/badge/version-1.2.0-green)]()

An [OpenClaw](https://openclaw.ai) skill that critiques the post-processing and editing of a photograph. Runs automatically alongside the `photo-captions` skill, or triggers when you ask about a photo's exposure, tone, color grade, or edit.

## Features

- 🖼️ **Composition critique** — framing, subject placement, depth/layering, leading lines, horizon, point of entry
- 🎨 **Tonal analysis** — contrast, shadow/highlight handling, midtone separation
- 🌡️ **Color critique** — white balance, color cast, saturation, color grade consistency
- 📐 **Grain & texture** — evaluates whether grain is natural and appropriate for the stock/ISO
- 🔍 **Zone-specific feedback** — names the actual areas of the frame that need work
- 📊 **Letter grade** — honest A–D rating with one clear note on what would improve it
- 🎞️ **Film-aware** — understands stock characteristics (e.g. Portra overexposed intentionally vs. a mistake)

## Installation

```bash
clawhub install photo-edit-analysis
```

## Usage

Triggers automatically when used with `photo-captions`. Also responds to direct questions like:

- "Is this edited well?"
- "Is it underexposed?"
- "What would you fix in this edit?"

## Output

150–250 words of editorial feedback structured as: what's working, what isn't, and a letter grade with one actionable note.

## Requirements

- OpenClaw agent
- Works best paired with `photo-captions`

## License

MIT

## Links

- [ClawHub](https://clawhub.com/pfrederiksen/photo-edit-analysis)
- [OpenClaw](https://openclaw.ai)
