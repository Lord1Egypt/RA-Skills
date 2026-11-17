---
name: "logo-svg-generator"
slug: "logo-svg-generator"
displayName: "Logo SVG Generator"
description: "Generate multi-size SVG logos from natural-language product briefs, following Simple Icons design rules; runs an iterative generate → visual-check → optimize loop with a vision-capable LLM. Invoke when the user asks to design a logo, brand mark, app icon or product icon from a description."
summary: "Design production-ready monochrome / brand-color SVG logos in multiple sizes with an iterative vision-LLM review loop, following Simple Icons rules."
version: "0.3.1"
license: "MIT"
homepage: "https://github.com/samonysh/logo-svg-generator-skill"
tags: ["design", "svg", "logo", "brand", "vector", "icon"]
---

# Logo SVG Generator

Turn a natural-language product brief (name, purpose, audience, mood, colors) into a **production-ready set of monochrome / brand-color SVG logos** in multiple sizes (16, 24, 32, 64, 128, 256, 512 px + 24×24 Simple-Icons-compatible master), by following the design regulations mined from the [Simple Icons](https://simpleicons.org/) project.

The skill uses an **iterative visual-review loop**: generate → rasterize → visually inspect (vision LLM) → critique → optimize → re-inspect → finalize.

> **Portable / agent-agnostic.** This skill is a plain Markdown + Python bundle. It runs anywhere a coding agent or LLM tool can load a `SKILL.md` and call local scripts — including but not limited to **TRAE, Opencode, Claude Code, Hermes, openclaw**, Cursor, Continue, or a custom harness. Any reference to "the agent" / "the host" below applies uniformly to all of them.

---

## When to invoke

Trigger this skill whenever the user says any of:

- "Design / make / create a logo for …"
- "I need an SVG icon / brand mark / product logo for …"
- "Generate a logo for my product …"
- "帮我设计 / 生成一个 logo / 图标"
- "给我做一个 SVG 的品牌标识"

Do **NOT** invoke for: free-form illustration, complex marketing artwork, photo editing, or non-vector deliverables.

---

## Inputs the skill collects (or infers)

Before generation, gather (asking the user only when critical, otherwise infer sensibly):

| Field | Example |
|---|---|
| `product_name` | "NovaSync" |
| `product_purpose` | "cross-device file sync tool" |
| `audience / vibe` | "developers, minimal, techy" |
| `preferred_color` (hex) | `#4F46E5` (if omitted → pick from mood) |
| `mono_or_color` | monochrome + branded variant (default: both) |
| `sizes` | `[16, 24, 32, 64, 128, 256, 512]` (default) |
| `metaphor_hints` | "letter N + sync arrows" (optional) |

---

## Core workflow (MUST follow in order)

### Step 1 — Read the design regulations
Load **[references/design-rules.md](references/design-rules.md)** — the condensed Simple Icons style guide (viewBox 0 0 24 24, single `<path>`, no stroke, no fill attribute in master, touches ≥ 2 sides of viewBox, centered, single-color-with-0.5px-gap technique, slug rules).

Also skim **[references/motif-patterns.md](references/motif-patterns.md)** for common shape recipes (roundel, letterform, monogram, arrow, waveform, chevron, gear, chat-bubble, spark, etc.) with real path-fragment examples.

### Step 2 — Brainstorm 2–3 concept directions
Given the brief, write a short internal design brief covering:
1. **Metaphor** (what visual idea encapsulates the product?)
2. **Shape family** (geometric / letterform / abstract / pictogram)
3. **Color** (primary hex + when mono is required)
4. **Composition** (single symbol vs. mark + wordmark — this skill outputs **symbol only**, no wordmark)

Pick the strongest concept unless the user explicitly wants alternatives.

### Step 3 — Generate the 24×24 master SVG
Follow these hard rules (from Simple Icons CONTRIBUTING.md):

- Root: `<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">`
- One `<title>` with the product name
- **Exactly one** `<path d="…"/>`
- **No** `<rect> <circle> <ellipse> <polygon> <g> <line> <defs> <style> <use> <mask> <clipPath>`
- **No** `fill` / `stroke` / `class` / `id` on the path (color is added later per variant)
- Path must **touch at least 2 sides** of the viewBox (no padding)
- Visual center around (12, 12); keep coordinates to ≤ 3 decimals
- Where color layers would exist, use a **0.5-unit gap** trick to imply separation while staying single-path

Write the master to `output/<slug>/master-24.svg`.

### Step 4 — Rasterize + visual check (VISION-CAPABLE LLM REQUIRED BY DEFAULT)

**Hard requirement:** the logo check step MUST be performed by an LLM that has image-input (vision) capability, and that vision capability MUST actually be exercised on the rendered PNG. This is the default and non-optional path — text-only critique is not acceptable as a substitute. If the current host / model does **not** expose vision input, the skill MUST NOT silently fall back; instead the agent MUST:

1. Explicitly inform the user that a vision-capable LLM is required for the review loop.
2. Ask the user to switch to a vision-capable model (or provide an explicit `--no-review` / `structural-only` override) before continuing.
3. Only proceed to the structural-only degradation (Step 5, last bullet) after the user has knowingly opted in.

Run `scripts/render_previews.py` to rasterize the master at **32, 64, 128, 256, 512** and produce a review sheet PNG (`output/<slug>/_review.png`) with:

- The icon on white, on black, and inside a rounded-square app-icon frame
- The 5 sizes side-by-side (to catch scale-dependent issues)
- Coordinate grid overlay at 64px

Then, hand `_review.png` **plus** the source SVG to the **vision-capable LLM** with the prompt in **[assets/templates/visual-review-prompt.md](assets/templates/visual-review-prompt.md)**. The image MUST be attached as a real image input (not described in text) so the model exercises its vision pathway. The reviewer must return a JSON critique:

```json
{
  "score": 0-10,
  "readable_at_16px": true,
  "issues": [
    {"severity": "high|med|low", "area": "balance|proportion|weight|negative-space|readability|brand-fit|geometry", "note": "…"}
  ],
  "concrete_fixes": ["Nudge the top-left arc 0.3u down", "Increase counter of letter N by 8% ..."],
  "verdict": "accept|revise"
}
```

### Step 5 — Optimize
If `verdict == "revise"`, apply the `concrete_fixes` to the SVG path (edit coordinates directly; keep single-path rule). Save as `master-24.v{N}.svg`, then **loop back to Step 4**.

- Max loop count: **3 iterations** (config in `scripts/config.json`; can be raised to 5 with `--max-iterations` when the caller explicitly asks for more polish).
- Stop early when `score ≥ 8.5` AND `readable_at_16px == true` AND no `high` severity issue remains.
- If loops exhaust without acceptance, keep the highest-scoring version as the final master, save every iteration under `output/<slug>/history/` for debugging, and produce a **user-facing summary** (`output/<slug>/_review-summary.md`) that translates each residual `issue.note` into a plain-language sentence plus a suggested next action (e.g. "the letter N is slightly off-center — you can nudge it 0.3u right, or ask me to run 2 more iterations").
- **Graceful degradation when no vision-capable LLM is available:** this path is **opt-in only** and requires either the user's explicit consent (see Step 4 hard requirement) or a `--no-review` / `require_vision_llm=false` override in `scripts/config.json`. When permitted, skip Step 4/5's vision critique and instead run the deterministic checklist in `scripts/validate_svg.py` **plus** the geometric checks documented in `references/design-rules.md` §2 (touches-two-sides, bbox center window, ink coverage). Mark `brand.json.review_mode = "structural-only"` so downstream users know a human should eyeball the result. Never engage this path silently.

### Step 6 — Generate multi-size + color variants
Once the master is accepted, run `scripts/export_variants.py` to produce:

```
output/<slug>/
├─ master-24.svg              (canonical Simple-Icons-compatible)
├─ mono/
│  ├─ logo-16.svg  logo-24.svg  logo-32.svg  logo-64.svg
│  ├─ logo-128.svg logo-256.svg logo-512.svg
├─ color/
│  └─ (same set, path filled with brand hex)
├─ png/
│  └─ logo-16.png … logo-512.png  (PNG previews)
├─ favicon/
│  └─ favicon.ico  apple-touch-icon-180.png
├─ _review.png
└─ brand.json                 ({ slug, title, hex, source_brief, iterations })
```

Multi-size SVGs are the **same path** with adjusted `width`/`height` attributes and (for small sizes 16 & 24) optional **path-simplification** (see `scripts/simplify_for_small.py`) — remove sub-details that vanish below 20px.

### Step 7 — Deliver
Give the user computer:// links to the top-level output folder, the master SVG, and the review sheet. Summarize the concept in ≤ 3 sentences.

---

## Non-negotiable design rules (quick check before finalizing)

Every SVG file the skill emits must pass **all** of:

- [ ] `role="img"`, `viewBox="0 0 24 24"`, `xmlns` — in that order
- [ ] Exactly one `<title>`
- [ ] Exactly one `<path>`, no other tags
- [ ] Master has no `fill`, no `stroke`, no `class`, no `id`
- [ ] Path touches ≥ 2 sides of the 24×24 canvas
- [ ] Visually centered (bounding box center within (11, 13) × (11, 13))
- [ ] Aspect ratio of original concept preserved (never stretched)
- [ ] Slug follows `slugify` rules (lowercase alphanumeric; `.`→`dot`, `+`→`plus`, `&`→`and`, remove spaces / punctuation)
- [ ] At 16 px it is still recognisable (validated by vision LLM)

---

## File layout of this skill project

```
logo-svg-generator-skill/
├─ SKILL.md                    ← this file (SkillHub entry point)
├─ references/
│  ├─ design-rules.md          ← condensed Simple Icons rules
│  ├─ motif-patterns.md        ← common shape recipes + path snippets
│  └─ sample-icons.md          ← 15 curated real SVG references
├─ assets/
│  ├─ logo.svg / logo-*.svg    ← this project's own brand marks
│  └─ templates/
│     ├─ visual-review-prompt.md  ← prompt for vision LLM critique
│     └─ concept-brief-template.md
├─ scripts/
│  ├─ fetch_samples.py         ← pull N icons from simple-icons CDN
│  ├─ render_previews.py       ← SVG → review PNG sheet
│  ├─ export_variants.py       ← multi-size + color variants
│  ├─ simplify_for_small.py    ← small-size path simplification
│  ├─ validate_svg.py          ← rule compliance checker
│  ├─ deploy_skill.py          ← copy skill files → target agent's skill dir
│  └─ config.json
├─ samples/                    ← downloaded reference SVGs (git-ignored)
└─ output/                     ← per-run deliverables (git-ignored)
```

---

## Related references

- [references/design-rules.md](references/design-rules.md)
- [references/motif-patterns.md](references/motif-patterns.md)
- [references/sample-icons.md](references/sample-icons.md)
- [assets/templates/visual-review-prompt.md](assets/templates/visual-review-prompt.md)
- [assets/templates/concept-brief-template.md](assets/templates/concept-brief-template.md)

Source of truth for design regulations:
- https://simpleicons.org
- https://github.com/simple-icons/simple-icons/blob/develop/CONTRIBUTING.md
- https://github.com/simple-icons/simple-icons/blob/develop/slugs.md

---

## Edge cases & how to handle them

| Situation | What the skill does |
|---|---|
| **Very long product name** (`>16` chars, e.g. "HyperContinuousDeliveryPlatform") | Do NOT try to fit the whole name inside the 24×24 canvas. Use only the first initial as a monogram, or ask the user to pick a 1–2-letter abbreviation. Full name still goes into `<title>` and `brand.json.title`. |
| **Multi-word name** ("Nova Sync", "Pulse Mail") | Compose either an initials monogram (`NS`, `PM`) or a symbol derived from the dominant word. Never render the full wordmark inside the icon. |
| **Non-ASCII product name** ("音见 AI", "Café") | Slugify to ASCII per §5 of `design-rules.md` before saving files; keep the original characters only inside `<title>`. |
| **User requests a wordmark or lockup** | Explain that this skill emits symbol marks only, then either (a) generate the strongest single-letter monogram, or (b) hand off to a general design step outside the skill. |
| **User requests a photorealistic / gradient / 3-D logo** | Refuse politely and explain that Simple-Icons style is monochrome flat vector. Offer a flat interpretation as an alternative. |
| **Brand color has poor contrast on white** (e.g. `#F7F7F7`) | Warn the user, still emit the color variant, and always ship a black monochrome fallback. |
| **Vision LLM unavailable / rate-limited** | Stop and inform the user — a vision-capable LLM is the default, non-optional reviewer. Only fall back to `review_mode = "structural-only"` (see Step 5) after the user explicitly opts in (or `--no-review` is passed). Do NOT block the export once the user has opted in. |
| **Rasterizer unavailable** (no `cairosvg`, `resvg`, or `inkscape`) | Emit the SVG variants + `brand.json`, skip `png/` + `_review.png`, and tell the user which one-liner install would restore raster output. |
| **CDN blocked / offline** | `fetch_samples.py` retries with the fallback mirrors in `scripts/config.json`. If all fail, skip sample fetching — the skill can still design from `references/motif-patterns.md` alone. |
| **User in mainland China** | The default primary CDN is jsDelivr; alternate mirrors (`fastly`, `unpkg`, `bytedance jsdelivr mirror`) are tried in order. See `scripts/config.json.cdn_url_templates`. |

---

## FAQ / anti-patterns

**Q: The reviewer keeps returning `score = 6-7` — what should I do?**
The most common cause is **too many motifs**. Cut back to one dominant idea (§Combining motifs · Rule 1 in `motif-patterns.md`) and re-run. If the score still stalls, ask the user for a fresh metaphor hint rather than looping indefinitely.

**Q: `validate_svg.py` fails with `element: <g> is forbidden` — why?**
An LLM sometimes wraps the path in `<g>` for grouping. Delete the `<g>` tags; keep only `<svg><title/><path/></svg>`. The skill MUST emit exactly two child elements of `<svg>`.

**Q: The path uses `fill="currentColor"` on the master.**
That is still a `fill` attribute and fails compliance. The master carries NO fill; color is added by `export_variants.py` only for the `color/` variants.

**Q: My icon looks great at 512 px but is unreadable at 16 px.**
Run `scripts/simplify_for_small.py` and, more importantly, drop sub-details below ~1u wide before Step 3. The reviewer's `readable_at_16px` field is a hard gate; if it comes back `false`, do NOT accept.

**Q: Can I skip the vision-review loop for speed?**
Yes — set `max_review_iterations: 0` in `scripts/config.json` or pass `--no-review`. You will get a rule-compliant but visually un-audited SVG. Recommended only when the caller is doing their own review.

**Q: The generated logo looks generic (a circle with a letter).**
Feed the concept brief more specific `metaphor_hints`. "Two orbiting nodes with a break", "envelope with an EKG waveform" produces markedly stronger results than "modern and clean".

### Anti-patterns to avoid
1. **Silently swallowing rule violations.** Every emitted SVG must pass `validate_svg.py`. If it fails, fix the SVG or report the violation to the user — never emit anyway.
2. **Adding a wordmark inside the 24×24 canvas.** Even a 2-letter wordmark rarely survives at 16 px.
3. **Using `<circle>` "because the geometry is easier".** Convert to a `<path>` arc; multiple SVG elements are a hard-fail.
4. **Skipping the concept brief.** Without a brief, the reviewer has no `brand_fit` reference and the iteration loop cannot converge.
5. **Looping past `max_review_iterations`.** If the score has not converged in 3 rounds, further iterations rarely help — ask the user for a new metaphor instead.

---

## End-to-end walk-through

```text
User: 帮我给 NovaSync 设计一个 logo，跨设备文件同步工具，靛蓝色，开发者向。

Step 1  → skill loads references/design-rules.md and references/motif-patterns.md
Step 2  → concept brief (auto-derived):
          product_name: "NovaSync", slug: "novasync",
          preferred_color: "#4F46E5",
          metaphor_hints: "letter N + sync orbit arrows",
          shape_family: "letterform"
Step 3  → generates master-24.svg with a single <path> that renders an 'N'
          whose diagonal is a partial orbit arc; touches top + bottom edges.
Step 4  → python scripts/render_previews.py output/novasync/master-24.svg
          → output/novasync/_review.png
          vision LLM returns:
            { "score": 7.4, "readable_at_16px": true,
              "issues": [ {"severity":"high","area":"balance",
                           "note":"orbit arc is 0.4u too low"} ],
              "concrete_fixes": ["shift arc anchor from (7,15) to (7,14.6)"],
              "verdict": "revise" }
Step 5  → path is edited; saved as master-24.v1.svg; loop back.
          v1 scores 8.7 → verdict "accept".
Step 6  → python scripts/export_variants.py output/novasync/master-24.v1.svg \
              --slug novasync --title NovaSync --hex "#4F46E5"
Step 7  → user receives:
            output/novasync/
              master-24.svg
              mono/logo-{16,24,32,64,128,256,512}.svg
              color/logo-{...}.svg      (fill="#4F46E5")
              png/logo-{...}.png
              _review.png
              brand.json                { "review_mode": "vision", ... }
```

For a copy-pasteable input brief see [`examples/01-novasync/brief.md`](examples/01-novasync/brief.md); expected outputs are described in [`examples/01-novasync/README.md`](examples/01-novasync/README.md).
