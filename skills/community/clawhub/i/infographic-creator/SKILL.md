---
name: infographic
description: >
  Generate modern operator-style social-media infographics (Twitter, LinkedIn, Instagram) using OpenAI gpt-image-2.
  Use this skill whenever the user wants to make an infographic, design a Twitter or LinkedIn visual, draft a cheat sheet, create a comparison graphic, build a branded image post, ship a content carousel, or produce a recurring weekly visual series. The skill owns the full pipeline: idea selection, layout choice, asset enrichment via Google favicons, copywriting refinement through targeted questions, and final rendering via the OpenAI images.edit endpoint with reference logos and avatar.
  Trigger on: "make an infographic", "design a Twitter visual", "draft a cheat sheet", "create a social graphic", "branded image post", "comparison graphic", "before/after visual", "ranked list image", "process flow infographic", "hero chart for tweet", "framework graphic", "carousel post", "weekly social series", "LinkedIn carousel", "Instagram graphic", "twitter image", "social card".
  Also trigger when a user asks to render any kind of designed image with text + structured layout for social distribution, even if they don't say "infographic" specifically — for instance "I want to share these 5 lessons as a visual" or "turn this comparison into a graphic." This skill is designed to avoid the generic AI-image look and produce graphics that read as intentional, branded, and on-trend for product/founder/operator content.
metadata:
  requires:
    env:
      - OPENAI_API_KEY
    bins:
      - python3
      - curl
    pip:
      - openai
      - cairosvg
---

# Infographic generator

A pipeline for producing branded, operator-style infographics for social media. The design system is reverse-engineered from top product creators on LinkedIn — the look is clean grid structure + handwritten annotations + flanking emojis + signed footer. Outputs are ready for Twitter, LinkedIn, or Instagram.

The skill renders via OpenAI `gpt-image-2` using the `images.edit` endpoint so the user's logos, screenshots, and avatar are honored as visual references rather than hallucinated.

---

## What this skill produces

- **Single-image infographics** in 4:5 portrait, 1:1 square, or 16:9 landscape
- **Consistent visual identity** across posts via a saved theme color + avatar
- **12 layout templates** (L1–L12) covering comparisons, before/after, stage flows, ranked lists, hero charts, framework grids, cheat sheets, ladders, myth/truth, process grids, visual metaphors, and annotated screenshots
- **Reusable prompt patterns** so each new piece takes ~5 minutes from idea to PNG

---

## Project layout

When the skill is first used in a project, it creates a working directory:

```
infographics/
├── style.json          # active theme (filled at runtime: accent color, handle, avatar path)
├── assets/             # logos, screenshots, avatar (user-supplied)
├── outputs/            # rendered PNGs
└── prompts/            # one .py file per generated piece, kept for re-rendering
```

If this directory already exists, reuse the existing `style.json` (don't re-ask theme questions every session).

---

## The 5-step workflow — always follow

When the user asks for a new infographic, run these steps in order. Don't shortcut.

### Step 1 — Find the idea

If the user gave a clear topic, skip ahead. Otherwise:
- Surface 3–5 candidate ideas as a short table (idea title, why it'll resonate, suggested layout, suggested format).
- Pull from what you know about the user's work, recent context, or industry. Avoid generic ideas — specificity drives engagement.
- Recommend ONE pick with reasoning. Wait for confirmation.

### Step 2 — Select layout + format

Pick one layout from `references/style-guide.md` (L1–L12). Justify briefly.

Then pick a Twitter/LinkedIn format:

| Format | gpt-image-2 size | When to use |
|---|---|---|
| **4:5 portrait** | `1024x1536` | Default. Dense data — comparison tables, cheat sheets, ranked lists. Highest engagement. |
| **1:1 square** | `1024x1024` | Single hero metaphor, hooks, hero charts. Punchy in-feed. |
| **16:9 landscape** | `1536x1024` | Process flows, timelines, before/after spreads. |

**Rotation rule:** if the user is producing a series, alternate formats across posts to break feed monotony. Don't ship 5 portraits in a row.

### Step 3 — Enrich with logos + images

Identify every brand, tool, or person mentioned in the idea. For each:

1. **Brand favicons via Google's favicon service**:
   ```
   https://www.google.com/s2/favicons?domain=DOMAIN&sz=128
   ```
   This is the most reliable logo source. Download with `curl -sL <url> -o assets/<name>.png`.

2. **SVG-only logos**: convert to PNG with `cairosvg`. Install inside a virtualenv to avoid touching the system Python:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install --quiet "openai>=1.0" "cairosvg>=2.7"
   python3 -c "import cairosvg; cairosvg.svg2png(url='in.svg', write_to='out.png', output_width=512)"
   ```
   If a venv isn't an option, ask the user before falling back to a system-wide install (e.g. `pip install --break-system-packages`) — it can affect their global Python environment.

3. **User avatar**: ask the user once for a photo path; copy into `assets/avatar.png` and reference in `style.json`.

4. **Verify each PNG visually with the Read tool** before proceeding. If a favicon came back as a generic globe (domain has no favicon), warn the user and either skip the logo or ask for an alternate URL.

### Step 4 — Copywriting (ask the user)

The visual quality is bounded by the copy quality. Ask 3–5 targeted questions to fill the prompt. Tailor them to the chosen layout. Examples:

- **Title** (≤6 words, declarative or metaphorical) — what's the punch?
- **Subtitle** (handwritten line, one conversational sentence)
- **Section/row labels** specific to the layout (e.g. for L1: column headers + 5–7 row criteria)
- **The takeaway** (closing one-line rule that goes in the cream callout box)
- **Tone**: declarative / contrarian / playful / operator-honest

Do NOT generate copy yourself. Wait for the user. Their voice is the differentiator — the moment you write the copy, the post sounds AI-generated.

### Step 5 — Generate

1. **Compose the prompt**: open `references/prompt-templates.md`, pick the right layout template, fill in all `{{...}}` placeholders with the user's confirmed copy, accent color, and reference image filenames.
2. **Save the prompt** as a `.py` file in `infographics/prompts/<slug>.py` so it's re-runnable.
3. **Render via gpt-image-2**: call `scripts/generate.py` (see that file for the exact API contract).
4. **Read the output** with the Read tool and show it to the user inline.
5. **Note any rendering issues** + offer one tightening pass (e.g. "Hostinger logo came out fuzzy — want me to swap to a cleaner source?").

---

## Style invariants — never break these

These are what make the output look intentional rather than AI-slop. Skipping any one of them dilutes the whole brand.

1. **Accent color carries the piece.** Frame, accent words in the title, handwritten subtitle, hand-drawn arrows — all use the user's chosen accent. Read `style.json` for the active hex; if not yet set, ask the user.

2. **Two emojis flank the title** (top-left + top-right). One literal, one emotional. Use 3D Apple-style emojis, never flat ones.

3. **Handwritten subtitle** in a darker shade of the accent color (~25% darker), Caveat or Patrick Hand font. One sentence, conversational.

4. **Footer signature pill**: black rounded pill at bottom-center, small circular avatar (from `assets/avatar.png`) on the left, the user's handle on the right. Anchors the brand.

5. **Closing panel is mandatory.** Every piece ends with either a cream callout box ("rule of thumb"), a mint "final insight" panel, or a handwritten one-liner. Never end on raw data.

6. **Use `images.edit`, not `images.generate`.** This is what lets reference logos and the avatar be honored. `generate` will hallucinate them.

7. **Don't say "purple" (or any color word) verbally in the prompt** if it conflicts with the chosen accent hex. Models weight words higher than hex codes. Always describe the accent as the actual color word the user picked, AND include the hex.

---

## Worked example — comparison infographic

User says: *"Make a comparison infographic of Linear vs Jira."*

**Step 1** — Idea is clear. Skip to step 2.

**Step 2** — Layout: **L1 (comparison table)** — head-to-head naturally maps to a table. Format: **4:5 portrait** for density. Confirm with user.

**Step 3** — Fetch logos:
```bash
curl -sL "https://www.google.com/s2/favicons?domain=linear.app&sz=128" -o assets/linear.png
curl -sL "https://www.google.com/s2/favicons?domain=atlassian.com&sz=128" -o assets/jira.png
```
Read both back to confirm they look right.

**Step 4** — Ask:
- Title (≤6 words): your suggestion?
- Subtitle (handwritten, one line): the human take
- 5–7 comparison rows: which dimensions matter (speed, pricing, integrations, learning curve, mobile, ...)
- Takeaway: which side you actually pick + why
- Tone: declarative / contrarian / playful?

**Step 5** — Compose the L1 prompt from `references/prompt-templates.md`, fill in placeholders, save to `infographics/prompts/linear-vs-jira.py`, render at `1024x1536`, show output, note quirks.

---

## Pitfalls to avoid

- **Color word/hex conflict** — if the user picks `#006EFF` (blue), don't leave the word "purple" or "violet" anywhere in the prompt. The model weights words higher than hex codes.
- **Text density above ~12 cells** — gpt-image-2 starts garbling. Shorten cell copy or split into two posts.
- **Brand-name moderation** — celebrity names, "Tesla", "Apple" (and other major brands sometimes) trip the safety system on `images.edit`. If you get a `moderation_blocked` error, swap the brand reference for a generic descriptor and retry.
- **SVG logos** — gpt-image-2 won't accept them. Always convert to PNG first.
- **Outer frame missing** — gpt-image-2 frequently drops the top edge of the outer accent frame. If a clean frame matters, composite it in Figma post-render (5 min job). Don't burn iterations chasing it.
- **Tiny favicon source** — Google's favicon API sometimes returns a 32px image. The model can still use it as a reference but the rendered logo may look fuzzy. Try `&sz=256` first; if still small, source from the brand's press kit.
- **Avatar drift** — gpt-image-2 will sometimes alter the avatar photo. If brand consistency matters, composite the real avatar over the rendered output in Figma.

---

## Security notes

This skill writes images, reads reference files, and uploads them to OpenAI. A few things to be deliberate about:

- **API key scoping**: `OPENAI_API_KEY` should be a project-scoped key with a spending limit. Image-2 calls are billable and can run up if the loop misfires.
- **Reference images stay inside `assets_dir`**: `scripts/generate.py` rejects absolute paths and `..` segments in filenames. Don't try to work around the guard — if you need a logo from elsewhere, copy it into `infographics/assets/` first.
- **Output names must be bare basenames**: `out_name` is validated for the same reason. Use names like `linear-vs-jira`, never paths.
- **Prompt files**: when invoking the CLI with `python3 generate.py path/to/prompt.txt …`, treat the prompt file as user-authored. Don't let an upstream agent point this at unrelated local files (the contents will be sent to OpenAI).
- **Confidential assets**: logos, screenshots, and avatars are uploaded to OpenAI under your account. Don't include private/internal product UI you wouldn't paste into ChatGPT.
- **Persistent style state**: `infographics/style.json` stores the user's accent color, handle, and avatar path. Treat it as branding metadata only — never store secrets there.

---

## Reference files

When you need details, read these:

- **`references/style-guide.md`** — full visual rules: 12 layouts (L1–L12), color tokens, typography, recurring motifs, tone of writing
- **`references/prompt-templates.md`** — fill-in-the-blank prompt scaffolds, one per layout
- **`references/style.json`** — machine-readable design tokens, runtime-edited to record the user's theme

---

## When the user has used this skill before

- Don't re-ask their theme color or handle — read `infographics/style.json` from their project.
- Reuse logos already in `assets/` (don't re-fetch).
- Ask if they want to keep the same format as last post (rotation rule) or switch.

---

## When to recommend Figma post-processing

Image-2 is great for the *layout + composition* but has known weak spots:
- Pixel-perfect outer frames
- Brand logos at small sizes (favicons under 64px)
- Specific typography (forcing a real font like Inter)
- Avatar fidelity

If any of these matter for a high-stakes post (launch announcement, sponsored content), generate the layout in image-2, then do a 5-minute touch-up in Figma to composite real logos + avatar + frame. Tell the user when that's worth doing.
