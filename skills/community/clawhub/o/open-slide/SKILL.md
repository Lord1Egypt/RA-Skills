---
name: open-slide
description: Create, edit, preview, and export web-native slide decks with the open-slide React framework.
metadata: {"openclaw":{"requires":{"bins":["node","python3"],"anyBins":["pnpm","npm"]}}}
---

# open-slide - Slides as React Code

open-slide is a slide framework built for agents. You write React components on a fixed 1920×1080 canvas; the framework handles scaling, navigation, hot reload, present mode, and export. Every slide is a file — versioned, reviewable, yours.

This OpenClaw skill is an independent companion for the upstream open-slide framework at https://github.com/1weiho/open-slide. It does not vendor or replace open-slide; it guides agents to use the upstream framework and CLI.

## When to Use This Skill

- User wants to **create a new presentation/deck** (web-native output)
- User mentions "open-slide" or "slides as code"
- User wants to **edit or iterate** on an existing open-slide deck
- User wants to **preview** slides or **export** to HTML/PDF
- User wants to **scaffold** a new open-slide workspace
- User wants to **apply inspector comments** to slides
- User asks for "slides as code", "React slides", or a web-native presentation

If the user explicitly needs a `.pptx` file for PowerPoint compatibility, use a PowerPoint/PPTX workflow instead of open-slide.

## Prerequisites

- **Node.js** 18+ must be available.
- **pnpm** or **npm** must be available.
- **Python 3** must be available for PDF export.
- **Python dependencies:** install from `{baseDir}/requirements.txt` when exporting.
- **Browser binaries:** Playwright requires Chromium to be installed once.

Check availability before exporting:
```bash
python3 -m pip install -r {baseDir}/requirements.txt
python3 -m playwright install chromium
```

Check Node.js availability before starting:
```bash
node --version
pnpm --version  # or: npm --version
```

If Node.js, Python 3, and at least one package manager are not available, tell the user what is missing before continuing.

---

## Workflow 1: Init — Scaffold a Deck (First Time)

```bash
# Prefer pnpm when available; otherwise use npm/npx.
pnpm dlx @open-slide/cli init <deck-name>
# or:
npx @open-slide/cli init <deck-name>

cd <deck-name>
pnpm install  # or npm install
```

This creates:
```
<deck-name>/
├── slides/
│   └── getting-started/
│       └── index.tsx       # starter slide
├── themes/                  # optional shared themes
├── open-slide.config.ts     # framework config
├── AGENTS.md                # agent rules
└── package.json
```

Keep track of the deck path — all subsequent commands run from there.

---

## Workflow 2: Create — Author a New Deck

Before writing any code, **read the authoring reference** at `{baseDir}/references/authoring.md` for the file contract, canvas rules, vertical budget math, type scale, design system, and anti-patterns.

### Step 1 — Pick a theme (if available)

List files under `themes/` in the deck root. If theme markdown files exist, ask the user which theme to use (or "no theme — design from scratch"). Read the chosen theme file end-to-end — its palette, typography, and layout are now authoritative.

### Step 2 — Clarify requirements

Before writing any code, lock in these decisions if not already provided. Ask users:

1. **Aesthetic direction** — propose 3 visual directions tailored to the topic. Each should combine a vibe word + concrete visual cue (palette, typography, motif). Mark the best fit as "(Recommended)".
2. **Page count** — 3–5 (short), 6–10 (standard), 11–20 (deep dive), or custom.
3. **Text density** — minimal (one line / big number), light (heading + 2–3 bullets), standard (heading + 4–5 bullets), dense (multi-column).
4. **Motion** — static (no motion), subtle (fades/entrance only), rich (keyframes, staggered reveals).

Only skip a question when the user's original request already gave an unambiguous answer — and restate your assumption so they can correct it.

### Step 3 — Pick a slide id

Kebab-case, short, descriptive. Examples: `rust-intro`, `q2-roadmap`, `team-offsite-2026`. Check `slides/` to avoid collisions.

### Step 4 — Plan the structure

Sketch the slide as a list of page roles:

| Role | Purpose |
|------|---------|
| Cover | Title + subtitle, strong visual |
| Agenda | What's coming (3–5 items) |
| Section divider | Big label between chapters |
| Content | Heading + 2–5 bullets OR heading + one visual |
| Big number | One statistic the size of the canvas |
| Quote | Pull-quote with attribution |
| Comparison | Two-column before/after or A vs B |
| Closing | CTA, thanks, contact |

**One idea per page.** If you're tempted to put two, split them.

Share the outline with the user for quick confirmation before writing code.

### Step 5 — Write `slides/<id>/index.tsx`

Follow the authoring reference in `{baseDir}/references/authoring.md`. Key points:

- **Declare `export const design: DesignSystem = { … }`** at the top — this makes the slide tweakable from the Design panel.
- **Use `var(--osd-X)` CSS variables** for visual properties (bg, text, accent, fonts, sizes).
- **Do the vertical budget math** for every page before writing — sum element heights + gaps + 2×padding ≤ 1080px.
- **One concept per page**, max ~40 words of body text.
- **Use `<ImagePlaceholder>`** from `@open-slide/core` only when a real image the user must supply is genuinely needed (product screenshots, team photos, data charts) — not for decoration.
- **Only use `react` and standard web APIs.** No extra npm packages.

### Step 6 — Self-review

Run the checklist in `{baseDir}/references/authoring.md` before finishing.

### Step 7 — Hand off

When the environment can run a browser, automatically create a visual artifact:
1. Run the PDF export script at `{baseDir}/scripts/export_pdf.py`.
2. Report the final `.pdf` absolute path to the user.
3. Ask whether they want the source code or the static HTML build (`dist/`) zipped for hosting.
---

## Workflow 3: Edit — Iterate on Slides

### Direct Code Edits

Open `slides/<id>/index.tsx` and modify the React code. This is the most common workflow — you're just editing code. Always re-verify the vertical budget after changes.

### Apply Inspector Comments

When the user has used the inspector in the browser and has `@slide-comment` markers in the source:

1. Scan all files under `slides/` for `@slide-comment` markers
2. For each marker, read the surrounding code and the comment text
3. Edit the code to satisfy the comment
4. Remove the `@slide-comment` marker after applying
5. If a comment is ambiguous, leave the marker in place and explain why

---

## Workflow 4: Dev — Preview with Hot Reload

```bash
cd <deck-path>
pnpm dev  # starts on http://localhost:5173
```

The dev server gives you:
- **Live preview** — changes hot-reload instantly
- **Inspector** — press `i` to toggle; click any element to see/edit properties
- **Assets panel** — drag-drop images, search svgl logos
- **Present mode** — fullscreen with keyboard navigation
- **Design panel** — tweak palette, fonts, type scale, radius live

To visually verify a slide, use an appropriate browser tool to open `http://localhost:5173` and take a screenshot.

---

## Workflow 5: Export — Build & Share

```bash
cd <deck-path>
pnpm build       # static build to dist/
```

### PDF Export (headless)

open-slide currently has no built-in CLI PDF command. Use the bundled export script, which enters **Present mode** before capturing to get clean slides without editor chrome:

```bash
# Start dev server first
cd <deck-path>
pnpm dev

# In another shell, export to PDF
python3 {baseDir}/scripts/export_pdf.py \
  --url http://localhost:5173/s/<slide-id> \
  --pages <page-count> \
  --out /tmp/deck.pdf
```

**⚠️ Critical: always use Present mode.** The editor view (`/s/<id>`) includes navbars and sidebars. The export script presses `F` to enter Present mode and hides remaining controls via CSS before screenshotting. Never screenshot the editor view directly for PDF output.

### Share with the user

- Once the PDF or ZIP file is generated, send a message to the user and attach the file using the appropriate tool or attachment mechanism for your current communication channel. Ensure you provide the absolute file path so the system can locate and upload it.
- For **Static HTML:** The `dist/` folder can be zipped and sent, or deployed to any static host (Vercel, Cloudflare Pages, Netlify, etc.)

---

## Workflow 6: Theme — Create Reusable Themes

If the user plans multiple decks with a consistent look:

1. Create `themes/<id>.md` with palette, typography, voice, and layout vocabulary
2. Reference the theme name when creating future decks
3. See the Themes section in `{baseDir}/references/authoring.md` for the template

---

## Quick Reference: Page Patterns

### Cover Slide
```tsx
const Cover: Page = () => (
  <div style={{
    ...fill, background: 'var(--osd-bg)', color: 'var(--osd-text)',
    display: 'flex', flexDirection: 'column',
    justifyContent: 'center', padding: '0 160px',
  }}>
    <h1 style={{
      fontFamily: 'var(--osd-font-display)',
      fontSize: 'var(--osd-size-hero)',
      fontWeight: 900, lineHeight: 1.05,
    }}>
      Title
    </h1>
    <p style={{ fontSize: 'var(--osd-size-body)', color: muted }}>
      Subtitle
    </p>
  </div>
);
```

### Content Slide
```tsx
const Content: Page = () => (
  <div style={{
    ...fill, background: 'var(--osd-bg)', color: 'var(--osd-text)', padding: 120,
  }}>
    <h2 style={{
      fontFamily: 'var(--osd-font-display)', fontSize: 80, fontWeight: 800, margin: 0,
    }}>
      Section Title
    </h2>
    <ul style={{
      fontSize: 'var(--osd-size-body)', lineHeight: 1.6, marginTop: 64, paddingLeft: 48,
    }}>
      <li>One clear point per line</li>
      <li>Keep to 3–5 bullets</li>
      <li>Let the space breathe</li>
    </ul>
  </div>
);
```

## Error Recovery

- **Build errors:** Read the error output — it usually points to the exact line. Fix the TSX and the dev server hot-reloads.
- **Missing `@open-slide/core` types:** Make sure `pnpm install` ran successfully.
- **Port 5173 in use:** The dev server auto-increments to the next free port. Always check the actual port printed in the dev server output.
- **Blank slide:** Verify the component fills `width: '100%'` and `height: '100%'` on its root div.
- **Git identity error on init:** Set `git config --global user.email` and `git config --global user.name`, then init the git repo manually.
- **Blank PDFs from Playwright:** `page.pdf()` does not render CSS backgrounds by default, so dark-themed slides appear blank. Use the screenshot-based export script (`scripts/export_pdf.py`) instead — it takes PNG screenshots and converts them to PDF via Pillow, which preserves backgrounds correctly.
- **PDFs include editor navbars:** Never screenshot the editor view (`/s/<id>`) directly for PDF output — it includes sidebars, thumbnail rails, and toolbar. Always enter **Present mode** first (press `F`), then hide remaining controls with CSS injection before capturing.
