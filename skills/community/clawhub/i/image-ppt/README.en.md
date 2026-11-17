# Image PPT Skill · Turn Text into Editable PPTs

![GitHub stars](https://img.shields.io/github/stars/helloo1568/image-ppt?style=flat-square)
![License](https://img.shields.io/github/license/helloo1568/image-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Recommended-222222?style=flat-square)
![GPT-Image 2.0](https://img.shields.io/badge/GPT--Image%202.0-Recommended-0A7CFF?style=flat-square)

> 🌏 **中文版: [README.md](./README.md)**

An agent skill for **Codex / Claude Code and other agent environments** that turns books, PDFs, or any text material into **beautiful, editable PPTX decks** — not a pile of static images you cannot touch.

**Recommended environment: Codex + GPT-Image 2.0.** Codex reads the document, orchestrates the pipeline, and assembles files; GPT-Image 2.0 renders PPT pages with consistent style and pixel-accurate text.

## Why Codex + GPT-Image 2.0

| Stage | Recommended | Why |
|-------|-------------|-----|
| Document understanding & orchestration | **Codex** | Shell access to read long docs, loop image generation, and auto-assemble/restore PPTX in one run |
| Page rendering | **GPT-Image 2.0** | Pixel-accurate text, cross-page style consistency, commercial-grade layout |
| PPTX assembly | Codex + python-pptx | Embeds image pages in 16:9 order and outputs a downloadable .pptx |

> Works in any AI assistant with document reading, image generation, and file output capabilities (GPT, Claude, Kimi, Doubao, WorkBuddy, etc.) — follow the adaptation notes in the prompts.

## Three-Step Workflow

```
Source material (PDF / book / text)
    │
    ▼
① Extract content + design styles   Read the material, build an outline, generate 4 style previews
    │
    ▼
② Generate image-based PPT          Render pages in the chosen style, merge into a downloadable .pptx
    │
    ▼
③ Restore an editable PPTX          Rebuild page by page ("visual fidelity + editable text")
```

## 30-Second Start

Send this to an agent with shell access (Codex recommended):

```text
Install the image-ppt skill for me. Clone https://github.com/helloo1568/image-ppt into the local
skills directory, then verify SKILL.md and references/ exist. After that, "turn this book into a PPT"
will trigger it.
```

Then just say:

```text
Turn this PDF into a class-presentation PPT. Generate 4 style previews first; I'll pick one before you continue.
```

More example requests:

```text
Turn this book into a book-sharing deck; generate images with GPT-Image 2.0.
Make a lab-meeting PPT from this report, following the template style I uploaded.
Image PPT: convert this Markdown into an editable 16:9 PPTX.
```

## Highlights

- 🧠 **Reads the material**: extracts author background, structure, key ideas, examples, quotes, and takeaways
- 🎨 **Four style previews**: 4 previews with different colors/layouts/visual styles — pick one before rendering
- 🖼 **Page-by-page rendering**: one core idea per page, with structure diagrams, timelines, and relationship maps
- 📦 **Editable PPTX**: complex visuals kept as hi-res images, main text rebuilt as native PPT text boxes
- 🔁 **Iterative restore**: 1-3 pages per pass; confirm one page's quality before batch-processing the rest

## Good Fit / Not a Fit

**✅ Good fit**: classroom group presentations / book sharing / lab paper reviews / project reports / pitch events / coursework

**❌ Not a fit**: real-time multi-user collaborative editing (use Office online instead), dense data-table reports (image-based pages have limited information density)

## Common Use Cases

| Task | Recommended Approach |
|------|----------------------|
| Book → book-sharing deck | Full three-step flow, emphasize key ideas and quotes |
| Paper / literature → lab meeting | Prompt 1 to structure, add flow/relationship diagrams |
| Coursework / classroom demo | Reference template + 4 style previews for a quick final |
| Pitch / project report | Highlight conclusions and key-result pages, keep it tight |
| Existing image deck needs text edits | Prompt 3 to restore pages into an editable PPTX |

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Codex** | Recommended | Full pipeline: read docs, GPT-Image 2.0 rendering, python-pptx assembly/restore |
| Claude Code | Works | Strong text/orchestration; image gen needs an external tool |
| GPT / ChatGPT | Works | Native image capability; just paste the three prompts |
| WorkBuddy | Works | Document reading + local toolchain per adaptation notes |
| Kimi / Doubao / Tongyi | Partial | Confirm their image-generation and file-output capabilities |

## Installation

### One-liner (recommended)

```bash
npx skills add https://github.com/helloo1568/image-ppt --skill image-ppt
```

### Let the agent install it

> Install the `image-ppt` skill for me:
>
> 1. Make sure the local skills directory exists (`~/.claude/skills/` or `~/.codex/skills/`)
> 2. Run `git clone https://github.com/helloo1568/image-ppt.git <skills-dir>/image-ppt`
> 3. Verify `SKILL.md` and `references/prompts.md` exist
> 4. Tell me when done; "make a PPT" will trigger it afterwards

### Manual clone

```bash
git clone https://github.com/helloo1568/image-ppt.git ~/.claude/skills/image-ppt
# or into the Codex skills directory
git clone https://github.com/helloo1568/image-ppt.git ~/.codex/skills/image-ppt
```

### Trigger phrases

- "Turn this book into a PPT"
- "Make a class-presentation PPT from this PDF"
- "Image PPT, generate a book-sharing deck"
- "Make an editable PPTX from this material"
- "image-ppt"

## Workflow

The skill is a structured workflow the agent walks through:

1. **Read the material** — extract author background, structure, key ideas, examples, quotes, takeaways
2. **Design styles** — ask about a reference template, generate 4 style previews with GPT-Image 2.0
3. **User picks** — show previews, wait for a style choice
4. **Render pages** — cover → agenda → content → summary → thanks, in the chosen style
5. **Merge PPTX** — embed image pages in 16:9 order, output a downloadable .pptx
6. **Restore editability** — rebuild 1-3 pages per pass: complex visuals as images, main text as native text boxes
7. **Compare & iterate** — render a preview against the original; keep iterating on obvious gaps
8. **Delivery notes** — report what is editable text vs. image, and any font substitutions

Details in [`SKILL.md`](./SKILL.md); the three core prompts live in [`references/prompts.md`](./references/prompts.md).

## Repo Layout

```
image-ppt/
├── SKILL.md              ← Main skill file: three-step workflow & adaptation notes
├── README.md             ← Chinese README
├── README.en.md          ← This file (English)
├── manifest.yaml         ← Skill manifest (version, triggers, security notes)
└── references/
    └── prompts.md        ← Three copy-paste-ready core prompts
```

## Core Prompts

- **Prompt 1** — Content extraction & style design: read the material, generate 4 style previews
- **Prompt 2** — Image-based PPT generation: render pages in the chosen style and merge
- **Prompt 3** — Editable PPTX restore: "visual fidelity + editable text" hybrid strategy

## FAQ

**Do I have to use Codex?**
No. Codex is the recommended environment (document reading + GPT-Image 2.0 + python-pptx in one flow), but the three prompts work in any AI that can read documents and generate images.

**Do I have to use GPT-Image 2.0?**
No. It offers the best text rendering and cross-page consistency; swap the model name in the prompts for whatever you use.

**Is the generated PPT directly editable?**
Step 2 produces an image-based PPT (one image per page, not editable). Step 3 restores pages into an editable PPTX with main text as native text boxes.

**How many pages per restore pass?**
1-3 pages at a time. Too many at once degrades the element-splitting quality.

**Does this skill go online or upload data?**
No. It is a pure prompt methodology — everything runs in your own AI environment.

## Roadmap

- More real-world examples and preview images
- Fixed layouts for structure diagrams / timelines / relationship maps
- A ready-to-run python-pptx merge script
- Listing on ClawHub and other skill marketplaces

## License

[MIT](./LICENSE) © 2026 风清云影 (helloo1568)
