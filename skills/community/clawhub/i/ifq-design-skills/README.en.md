<sub>🌐 <a href="README.md">中文</a> · <b>English</b> · <code>ifq.ai / &lt;authored year&gt;</code></sub>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/ifq-brand/logo-white.svg">
  <img src="assets/ifq-brand/logo.svg" alt="ifq.ai" height="64">
</picture>

# IFQ Design Skills

> ClawHub-safe edition: this bundle keeps templates, references, and front-end assets only.
> For local Playwright verification and MP4/GIF/PDF/PPTX automation, use the full repo: https://github.com/peixl/ifq-design-skills
<sub><i>Intelligence, framed quietly.</i></sub>

<br>

<code>&nbsp;One prompt in.&nbsp;&nbsp;One shippable page out.&nbsp;&nbsp;Handcraft that reads as ifq.ai.&nbsp;</code>

<br><br>

[![License](https://img.shields.io/badge/license-MIT-D4532B?style=flat-square&labelColor=111111)](LICENSE.md)
[![ifq.ai native](https://img.shields.io/badge/ifq.ai-native-111111?style=flat-square)](assets/ifq-brand/BRAND-DNA.md)
[![ambient brand](https://img.shields.io/badge/ambient_brand-embedded-A83518?style=flat-square&labelColor=111111)](references/ifq-brand-spec.md)
[![proof first](https://img.shields.io/badge/proof--first-on-111111?style=flat-square)](references/verification.md)
[![modes](https://img.shields.io/badge/modes-12-D4532B?style=flat-square&labelColor=111111)](references/modes.md)
[![templates](https://img.shields.io/badge/templates-12-A83518?style=flat-square&labelColor=111111)](assets/templates/GALLERY.html)
[![anti-slop](https://img.shields.io/badge/anti--slop-preflight-D4532B?style=flat-square&labelColor=111111)](references/anti-ai-slop.md)

<br>

<sub>Thesis &nbsp;·&nbsp; Install &nbsp;·&nbsp; What it hears &nbsp;·&nbsp; Anatomy &nbsp;·&nbsp; Five marks &nbsp;·&nbsp; 12 modes &nbsp;·&nbsp; 12 templates &nbsp;·&nbsp; Six layers &nbsp;·&nbsp; Verification &nbsp;·&nbsp; License</sub>

</div>

---

## Thesis

Ask most agents to design something, and they will hand you one of two things: a **Figma Community template trying too hard**, or a **Notion page reformatted by an AI**. Neither ships.

This skill is what gets in the way of that. It is not a palette file. It is not a logo sticker.

It is **a way of making things**. Treat a web page like an editorial spread. An animation like a teaser cut. A slide deck like a launch-night master. A business card like a print job with real bleed.

The ifq.ai signature lives inside that craft. First you see the content. **Only on the second look do you notice — this is ifq.ai's hand.**

## Human + Agent Promise

| Audience | What they get |
|----------|---------------|
| **Human user** | Speak in goals instead of full PRDs; the skill reports assumptions, gaps, output files, and verification evidence. |
| **AI agent** | No blank-page guessing: classify the mode, read `modeRoutes`, fork a template, fill context, run anti-slop checks, verify. |
| **Maintainer** | The ClawHub bundle stays zero-dependency, hook-free, and auditable; heavy MP4/GIF/PDF/PPTX automation stays in the full GitHub repo. |

The operating idea is simple: **make AI higher leverage**. Humans judge direction and facts; agents run the craft loop and collect proof.

---

## Install

```bash
# Install from ClawHub (recommended)
openclaw skills install ifq-design-skills
```

> ClawHub is the recommended install channel. For local development, clone the full repo: <https://github.com/peixl/ifq-design-skills>. The ClawHub packaging repo is <https://github.com/peixl/ifq-design-clawhub>.

Then just talk to the agent. The skill routes, picks templates, and verifies itself.

### What first run should produce

Do not let the first run turn into setup. Say one concrete design goal, for example:

```text
Make a command center dashboard for our internal AI operations. Dense, calm, not a BI skin.
```

A good first run returns six pieces of evidence: the output HTML file path, the mode route, the template id, assumptions written into the work, the verification performed (`verify:lite` or browser preview), and caveats that affect use. It should not require account login, global export dependencies, or broad environment changes.

### Why it can compete for ClawHub Top 10

Skills that keep getting installed are rarely "do everything" bundles. They make one job obvious, produce a useful first result, and keep the trust boundary easy to inspect. IFQ Design Skills bakes that growth loop into the package:

| Conversion signal | How this skill handles it |
|---|---|
| Clear job | HTML-first visual artifacts only; no production frontend, backend, or SEO scope creep |
| First-run artifact | natural-language prompt → mode route → forked template → local HTML → evidence packet |
| Agent discipline | `modeRoutes`, evals, `verify:lite`, and `validate` constrain the execution path |
| Marketplace trust | zero dependencies, zero install hooks, no required credentials, no persistent background tasks, ClawHub-clean packing |
| Human shareability | output feels like ifq.ai craft without taking over the user's brand |

### 🦞 OpenClaw · preferred channel (one-line install)

```bash
# Install from ClawHub (recommended)
openclaw skills install ifq-design-skills

# Inspect capabilities and verify readiness
openclaw skills info ifq-design-skills
openclaw skills check ifq-design-skills
```

**Why OpenClaw is the fastest fit**: the frontmatter declares a full `metadata.openclaw` block — triggers, permissions, `tool_map`, and `quick_commands`. OpenClaw learns *when to invoke*, *which plugins it needs*, and *how to translate every neutral verb in `SKILL.md`* the moment it loads. Details and troubleshooting: [references/agent-compatibility.md](references/agent-compatibility.md#3--openclaw--clawhub).

Minimum permissions OpenClaw will request:

- `filesystem` — read + write inside the active workspace only
- `shell` — run bundled Node scripts only (`npm run validate` / `npm run pack`); Playwright / Python export helpers are opt-in in the full GitHub repo
- `browser` — outbound HTTPS for Google Fonts + image CDNs (read-only, **degrades gracefully**)

> **🌐 CN / offline friendly**: every generated HTML follows the Tier B non-blocking protocol in [references/font-loading.md](references/font-loading.md). When Google Fonts is blocked (mainland China, corporate intranet, offline preview), pages render immediately on the bundled `Noto Serif SC / Songti SC / PingFang SC` system stack — no blank screens, no tofu blocks. Tier A (system-only) and Tier C (self-hosted woff2 subset) are documented for full-offline and pixel-perfect needs.

**One-liners for every other agent**:

```bash
# Hermes (Nous Research)
hermes skills install github:peixl/ifq-design-skills

# Claude Code (personal)
git clone https://github.com/peixl/ifq-design-skills ~/.claude/skills/ifq-design-skills

# Codex CLI (OpenAI) — honors AGENTS.md at the repo root
git clone https://github.com/peixl/ifq-design-skills ~/.codex/skills/ifq-design-skills

# CodeBuddy (Tencent)
git clone https://github.com/peixl/ifq-design-skills ~/.codebuddy/skills/ifq-design-skills

# Share across every agent (recommended)
git clone https://github.com/peixl/ifq-design-skills ~/.agents/skills/ifq-design-skills
```

### For maintainers — pack for ClawHub

```bash
npm run validate   # one-minute smoke test: templates · brand toolkit · ClawHub cleanliness
npm run pack       # builds ../ifq-design-clawhub-YYYY-MM-DD.tar.gz (excludes .git/ and junk)
```

---

## What it hears

Real prompts. Left: what you say. Right: what the skill actually does.

<table>
<thead>
<tr><th width="50%">You say</th><th>It does</th></tr>
</thead>
<tbody>

<tr>
<td>

> "Tomorrow I'm giving a 20-min salon on AI agents. Give me a deck that doesn't look like a SaaS keynote — something with a bookish voice."

</td>
<td>

<sub>M-08 Keynote · editorial dark · Newsreader display · chapter breaks as rust ledger verticals · mono slide index <code>01 / 20</code> · closing colophon · ClawHub delivers the HTML deck + export plan; the full repo produces PPTX/PDF</sub>

</td>
</tr>

<tr>
<td>

> "Four updates shipped this week. Make a vertical changelog that feels like a loose-leaf notebook, not a company bulletin board."

</td>
<td>

<sub>M-07 Changelog · warm paper · single rust left-axis · each entry with mono timestamp · header <code>release ledger / vol.12</code> · hand-drawn icons in place of emoji</sub>

</td>
</tr>

<tr>
<td>

> "A friend's indie café. Two-sided card. Black-and-white. No flourish. Needs to feel handmade."

</td>
<td>

<sub>M-10 Card · 85×55mm + 3mm bleed · front: one-line offer + spark dot · back: mono info bar · third-party piece — explicit wordmark off · IFQ kept only as layout rhythm · SVG/HTML bleed source; full repo produces PDF</sub>

</td>
</tr>

<tr>
<td>

> "A 24-second hardware launch opener. Cool, like Teenage Engineering. Not a pre-announcement hype reel."

</td>
<td>

<sub>M-01 Launch Film · three directions first (matter-of-fact / editorial / kinetic-type) · Stage+Sprite timeline · key shot + mono spec overlay + 2s quiet-URL close · ClawHub delivers HTML motion source + keyposter; full repo produces MP4/GIF</sub>

</td>
</tr>

<tr>
<td>

> "One-page personal site. But I don't want it to look like I'm job-hunting."

</td>
<td>

<sub>M-02 Portfolio · five directions first (archive / studio / essay / atlas / ledger) · one chosen, two saved as variant canvases · first screen: no headshot, just <em>currently / writing / building</em> · mono colophon at base</sub>

</td>
</tr>

<tr>
<td>

> "Internal AI command center. Bloomberg-terminal density. Not a BI skin."

</td>
<td>

<sub>M-04 Dashboard · graphite ground · 12-col ledger grid · mono figures + hairline rust underline for trend direction · top row: session / latency / build · no gradient buttons, no cartoon pie colors</sub>

</td>
</tr>

<tr>
<td>

> "A vs B for the roadshow. Us against three competitors. Make it obvious why us. No bragging."

</td>
<td>

<sub>M-05 Compare · matrix over radar · four equal columns · each capability ✓ / ● / — with a small source citation · footer <code>compiled from public docs · ifq.ai</code> · facts WebSearched before any pixel moves</sub>

</td>
</tr>

<tr>
<td>

> "A 2026 AI-agent whitepaper. Under 50 pages. Has to be printable."

</td>
<td>

<sub>M-03 Whitepaper · A4 print-ready HTML · cover / abstract / TOC / chapters / references / colophon · each chapter opens with a mono number and half a page of air · footer <code>ifq.ai / &lt;authored year&gt;</code> · ClawHub delivers print-ready HTML; full repo produces PDF + bookmarks</sub>

</td>
</tr>

<tr>
<td>

> "Visuals feel messy. Don't fix it yet — just tell me what's wrong."

</td>
<td>

<sub>M-11 Brand Diagnosis · hands off · one-page report · color / type / rhythm / motif / finish scored 1–5 · before / suggested-after thumbnail per axis · three upgrade directions, no single verdict</sub>

</td>
</tr>

<tr>
<td>

> "Six social covers for a new column called 'one image a week.' Restrained, but instantly recognizable in-feed."

</td>
<td>

<sub>M-09 Social Kit · 1242×1660 · unified top-left column stamp <code>weekly / 01</code> → <code>06</code> · editorial-typography hero, no giant emoji · quiet URL bottom-right · six covers + one OG landscape, same scene system</sub>

</td>
</tr>

</tbody>
</table>

> No mode numbers to remember. Plain language is enough.

---

## Anatomy

A single hero landing. It looks calm. It is doing seven things at once.

```text
 ┌────────────────────────────────────────────────────────────────────┐
 │  ◇ ifq.ai / live system                            [01 / 12]       │ ← mono field note + column index
 │                                                                    │
 │                                                                    │
 │     Intelligence, framed                                           │ ← Newsreader display
 │     quietly.                                                       │   italic pivot word
 │                                                                    │
 │     A design engine that understands the difference                │ ← body serif
 │     between a slide deck and a launch film.                        │
 │                                                                    │
 │   ┃  ·  ledger                                                     │ ← rust ledger vertical
 │   ┃                                                                │   carries the layout
 │   ┃   01    mode-aware pipeline                                    │ ← mono numbered rows
 │   ┃   02    ambient brand, not loud branding                       │
 │   ┃   03    proof-first export loop                                │
 │                                                                    │
 │                                                                    │
 │                                      ✦                             │ ← signal spark
 │                                                                    │   a single lit point
 │                                                                    │
 │  compiled by ifq.ai              ·           ifq.ai / 2026         │ ← quiet URL + colophon
 └────────────────────────────────────────────────────────────────────┘
```

Unpacked:

1. **Editorial contrast** — Newsreader serif with JetBrains Mono. Not a random pairing.
2. **Rust ledger** — That vertical rule is ifq.ai's spine. More IFQ than any wordmark.
3. **Mono field note** — The `ifq.ai / live system` and `ifq.ai / 2026` microlines.
4. **Quiet URL** — No CTA shouting. The domain appears once, bottom-right.
5. **Signal spark** — One small lit point. The only graphic accent on the page.
6. **Warm paper** — Background is `#FAF7F2`, not `#FFFFFF`. Cold white has no temperature.
7. **Ledger rhythm** — Every spacing value sits on `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64`. Nothing by feel.

Viewers won't count the seven. They'll only say "this one looks a cut above."

**A cut above = one hand = the ifq.ai Ambient Brand.**

---

## Five marks

The Ambient Brand is five environmental markers. Every deliverable weaves in at least three.

| Mark | What it is | Where it lives |
|------|------------|----------------|
| **Signal Spark** | 8-point spark. Intelligence, lit | hero · motion cue · stamp center |
| **Rust Ledger** | Terracotta verticals, dividers, numbering, axes | hero · slides · infographic · dashboard |
| **Mono Field Note** | `ifq.ai / <authored year>` in JetBrains Mono | footer · closing · corner |
| **Quiet URL** | The domain, once, quietly | footer · meta · end card |
| **Editorial Contrast** | Newsreader italic + JetBrains Mono + warm paper | global typographic frame |

Not decoration. Layout grammar.

---

## Co-brand

| Context | Where IFQ sits |
|---------|----------------|
| **IFQ-owned work** (ifq.ai and its products) | Everyone on stage: wordmark · spark · field note · quiet URL |
| **Third-party / client work** | Client brand first. IFQ retreats to authored layer: rhythm, temperature, colophon, hand-drawn icons, export finish |
| **White-label required** | Drop the explicit wordmark and field note. Keep editorial contrast, ledger rhythm, proof-first craft |

**IFQ can go invisible. It never goes missing.** The craft itself is the signature.

---

## 12 modes

| # | Mode | Triggered by | Delivers |
|---|------|-------------|----------|
| M-01 | Launch Film | launch video · product film | 25–40s motion + keyposter + social kit |
| M-02 | Portfolio | personal site · about | one-pager + 5 direction variants |
| M-03 | Whitepaper | whitepaper · annual report · research PDF | A4 print-ready HTML; PDF is a full-repo enhancement |
| M-04 | Dashboard | command center · KPI · monitor | dense dashboard |
| M-05 | Compare | A vs B · benchmark | matrix + cited sources |
| M-06 | Onboarding | new-user flow · demo | 3–5 interactive screens |
| M-07 | Changelog | release notes · dev log | vertical timeline |
| M-08 | Keynote | talk deck · master template | HTML deck; PPTX/PDF are full-repo enhancements |
| M-09 | Social Kit | IG / Xiaohongshu / OG card | multi-size statics |
| M-10 | Card / Invite | business card · invite · VIP | SVG/HTML bleed source; PDF is a full-repo enhancement |
| M-11 | Brand Diagnosis | audit · upgrade | report + three directions |
| M-12 | Full Brand | brand from scratch | logo + palette + type + six applications |

Routing: **mode trigger → direction advisor fallback → Junior Designer main branch**.

Full protocol: [references/modes.md](references/modes.md).

---

## Six layers

It reads as IFQ not because of color, but because six layers move together.

| Layer | Role | Key file |
|-------|------|----------|
| **01 · Context Engine** | Grow the design from existing context. Never from blank | [design-context.md](references/design-context.md) |
| **02 · Asset Protocol** | Capture facts, logo, product shots, UI before pixels move | [asset-protocol.md](references/asset-protocol.md) · [workflow.md](references/workflow.md) |
| **03 · House Marks** | Weave the five ambient marks into the layout | [ifq-brand-spec.md](references/ifq-brand-spec.md) · [assets/ifq-brand/](assets/ifq-brand/) |
| **04 · Style Recipes** | Style as recipes + scene templates. Not mystique | [design-styles.md](references/design-styles.md) · [ifq-native-recipes.md](references/ifq-native-recipes.md) |
| **05 · Output Compiler** | ClawHub edition keeps the HTML-first core; MP4 / GIF / PPTX / PDF helpers are opt-in in the full GitHub repo | [scripts/](scripts/) |
| **06 · Proof Loop** | validate + pack + host-browser screenshots; deep export checks live in the full GitHub repo | [verification.md](references/verification.md) · [smoke-test.mjs](scripts/smoke-test.mjs) |

```text
ifq-design-skills/
├── SKILL.md                 # short router: trigger boundaries · safety contract · reference map
├── assets/
│   ├── ifq-brand/           # logo · sparkle · tokens · BRAND-DNA
│   └── templates/           # forkable templates with ambient marks pre-woven
├── references/              # methodology · mode manuals · verification · recipes
├── scripts/                 # ClawHub-safe smoke / pack; deep export helpers live in the full GitHub repo
└── demos/                   # sample outputs
```

---

## 12 Templates

v3.0 expands templates from 8 to 12 — every mode now has a dedicated template:

| Template | Mode | Purpose |
|----------|------|---------|
| T-hero-landing | M-01, M-02, M-06, M-12 | Editorial hero landing |
| T-slide-title | M-08 | Keynote title slide |
| T-dashboard | M-04 | Bloomberg-density command center |
| T-infographic-vertical | M-03, M-07 | Long-form infographic / whitepaper |
| T-social-x | M-09 | X/Twitter share card |
| T-compare-vs | M-05, M-11 | A vs B comparison matrix |
| T-changelog | M-07 | Vertical timeline |
| T-business-card | M-10 | Print card (90x54mm + 3mm bleed) |
| **T-portfolio** | M-02 | Essay-style portfolio with 5 switchable variants |
| **T-onboarding** | M-06 | 5-screen flow prototype with device frames |
| **T-diagnosis** | M-11 | Brand diagnosis with 6-dim radar chart |
| **T-social-multi** | M-09 | Multi-platform social kit (X / RedNote / IG / WeChat) |

Full preview: [assets/templates/GALLERY.html](assets/templates/GALLERY.html).

## Verification

```bash
npm run validate
npm run evals:validate
npm run anti-slop -- path/to/artifact.html
npm run verify:lite -- path/to/artifact.html
npm run pack
```

A one-minute health check: template index · IFQ brand toolkit · references router · 12-mode evals · ClawHub manifest · package safety · script safety · secret hygiene · font loading · default-template remote runtime · anti-slop preflight.

Per-deliverable verification starts with host-browser screenshots and click tests; full-repo environments add Playwright and export parity. See [references/verification.md](references/verification.md).

---

## License

MIT open-source license — see [LICENSE.md](LICENSE.md). IFQ names, logos, and project identity boundaries are in [NOTICE.md](NOTICE.md).

---

<div align="center">

<sub><code>compiled by ifq.ai&nbsp;&nbsp;·&nbsp;&nbsp;field note&nbsp;&nbsp;·&nbsp;&nbsp;2026</code></sub>


</div>
