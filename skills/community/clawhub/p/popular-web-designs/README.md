<picture align="right">
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/54-Design_Systems-0075de?style=flat-square">
  <img alt="54 Design Systems" src="https://img.shields.io/badge/54-Design_Systems-0075de?style=flat-square">
</picture>

# popular-web-designs

> 54 production-quality design systems extracted from real websites — every color, font, shadow, border radius, and component spec you need to build pixel-perfect clones.

[![Stars](https://img.shields.io/github/stars/minirr890112-byte/popular-web-designs?style=flat-square&color=f6c242)](https://github.com/minirr890112-byte/popular-web-designs/stargazers)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Templates](https://img.shields.io/badge/templates-54-0075de?style=flat-square)](#design-catalog)
[![ClawHub](https://img.shields.io/badge/ClawHub-downloads-1910-ff6b6b?style=flat-square)](https://clawhub.ai/skills/k97322wf)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

---

## What's Inside

Each of the **54 templates** is a complete design system markdown file containing:

- Color palette & roles (every hex value, semantic roles, interaction states)
- Typography hierarchy (font family, sizes, weights, line-heights, letter-spacing)
- Component stylings (buttons, cards, navs, inputs, badges, modals — with exact CSS)
- Layout principles (spacing scale, grid system, whitespace philosophy)
- Depth & elevation (shadow stacks with layer-by-layer values)
- Responsive behavior (breakpoints, collapsing strategy, touch targets)
- Accessibility specs (focus rings, color contrast ratios, interactive states)
- **Agent prompt guide** — copy-paste prompts to instantly generate pixel-perfect HTML

No guessing. No eyeballing. The exact values used by Stripe, Linear, Notion, Vercel, and 50 more.

## Why This Exists

When an AI generates HTML, it defaults to generic design. Blue links, system fonts, `box-shadow: 0 2px 8px rgba(0,0,0,0.1)`. These templates replace guesswork with precision.

**Without this skill:** you get a generic admin dashboard that looks like 100 other AI-generated demos.

**With this skill:** you get a pixel-accurate Notion page with warm-undertone grays, 4-layer whisper shadows, and compressed-letter-spacing Inter at 64px. You get a Stripe page with blue-purple gradients and weight-300 Source Sans elegance. You get a Linear dark mode UI with Geist Mono code blocks and purple accent glow.

<div align="center">

| Generic AI Output | With This Skill |
|---|---|
| `box-shadow: 0 2px 8px rgba(0,0,0,0.1)` | `rgba(0,0,0,0.04) 0px 4px 18px, rgba(0,0,0,0.027) 0px 2.025px 7.84688px, rgba(0,0,0,0.02) 0px 0.8px 2.925px, rgba(0,0,0,0.01) 0px 0.175px 1.04062px` |
| `border: 1px solid #e5e7eb` | `border: 1px solid rgba(0,0,0,0.1)` |
| `font-family: system-ui` | `font-family: 'Inter', -apple-system, system-ui, sans-serif` at exactly 64px/700/-2.125px |
| `background: #f9fafb` | `background: #f6f5f4` (warm white with yellow-brown undertone) |

</div>

## Install

```bash
# As a pip package
pip install git+https://github.com/minirr890112-byte/popular-web-designs.git

# As a ClawHub skill
clawhub install k97322wf3ap6xdkmwkwvej4kbd86h4yv
```

## Quick Start

```python
# Load any design template
from popular_web_designs import load_template

# Get the full Notion design system
notion = load_template('notion')
print(notion.colors.primary)  # {'text': 'rgba(0,0,0,0.95)', 'accent': '#0075de', ...}
print(notion.shadows.card)    # Multi-layer shadow stack
print(notion.typography.h1)   # {size: '64px', weight: 700, letter_spacing: '-2.125px', ...}
```

Or use it as a skill with any Hermes-compatible agent:

```
skill_view(name="popular-web-designs", file_path="templates/stripe.md")
```

Then ask the agent: "Build a landing page that looks like Stripe" — it will use the exact design tokens.

---

## Design Catalog

### AI & Machine Learning (12)

| Template | Site | Key Visual Identity |
|---|---|---|
| `claude.md` | Anthropic Claude | Warm terracotta accent, clean editorial layout |
| `cohere.md` | Cohere | Vibrant gradients, data-rich dashboard aesthetic |
| `elevenlabs.md` | ElevenLabs | Dark cinematic UI, audio-waveform aesthetics |
| `minimax.md` | Minimax | Bold dark interface with neon accents |
| `mistral.ai.md` | Mistral AI | French-engineered minimalism, purple-toned |
| `ollama.md` | Ollama | Terminal-first, monochrome simplicity |
| `opencode.ai.md` | OpenCode AI | Developer-centric dark theme, full monospace |
| `replicate.md` | Replicate | Clean white canvas, code-forward |
| `runwayml.md` | RunwayML | Cinematic dark UI, media-rich layout |
| `together.ai.md` | Together AI | Technical, blueprint-style design |
| `voltagent.md` | VoltAgent | Void-black canvas, emerald accent |
| `x.ai.md` | xAI | Stark monochrome, futuristic minimalism |

### Developer Tools & Platforms (14)

| Template | Site | Key Visual Identity |
|---|---|---|
| `cursor.md` | Cursor | Sleek dark interface, gradient accents |
| `expo.md` | Expo | Dark theme, tight letter-spacing, code-centric |
| `linear.app.md` | Linear | Ultra-minimal dark-mode, precise, purple accent |
| `lovable.md` | Lovable | Playful gradients, friendly dev aesthetic |
| `mintlify.md` | Mintlify | Clean, green-accented, reading-optimized |
| `posthog.md` | PostHog | Playful branding, developer-friendly dark UI |
| `raycast.md` | Raycast | Sleek dark chrome, vibrant gradient accents |
| `resend.md` | Resend | Minimal dark theme, monospace accents |
| `sentry.md` | Sentry | Dark dashboard, data-dense, pink-purple accent |
| `supabase.md` | Supabase | Dark emerald theme, code-first developer tool |
| `superhuman.md` | Superhuman | Premium dark UI, keyboard-first, purple glow |
| `vercel.md` | Vercel | Black and white precision, Geist font system |
| `warp.md` | Warp | Dark IDE-like interface, block-based command UI |
| `zapier.md` | Zapier | Warm orange, friendly illustration-driven |

### Infrastructure & Cloud (6)

| Template | Site | Key Visual Identity |
|---|---|---|
| `clickhouse.md` | ClickHouse | Yellow-accented, technical documentation style |
| `composio.md` | Composio | Modern dark with colorful integration icons |
| `hashicorp.md` | HashiCorp | Enterprise-clean, black and white |
| `mongodb.md` | MongoDB | Green leaf branding, developer documentation focus |
| `sanity.md` | Sanity | Red accent, content-first editorial layout |
| `stripe.md` | Stripe | Signature purple gradients, weight-300 elegance |

### Design & Productivity (10)

| Template | Site | Key Visual Identity |
|---|---|---|
| `airtable.md` | Airtable | Colorful, friendly, structured data aesthetic |
| `cal.md` | Cal.com | Clean neutral UI, developer-oriented simplicity |
| `clay.md` | Clay | Organic shapes, soft gradients, art-directed layout |
| `figma.md` | Figma | Vibrant multi-color, playful yet professional |
| `framer.md` | Framer | Bold black and blue, motion-first, design-forward |
| `intercom.md` | Intercom | Friendly blue palette, conversational UI patterns |
| `miro.md` | Miro | Bright yellow accent, infinite canvas aesthetic |
| `notion.md` | Notion | Warm minimalism, serif headings, soft surfaces |
| `pinterest.md` | Pinterest | Red accent, masonry grid, image-first layout |
| `webflow.md` | Webflow | Blue-accented, polished marketing site aesthetic |

### Fintech & Crypto (4)

| Template | Site | Key Visual Identity |
|---|---|---|
| `coinbase.md` | Coinbase | Clean blue identity, trust-focused, institutional feel |
| `kraken.md` | Kraken | Purple-accented dark UI, data-dense dashboards |
| `revolut.md` | Revolut | Sleek dark interface, gradient cards, fintech precision |
| `wise.md` | Wise | Bright green accent, friendly and clear |

### Enterprise & Consumer (8)

| Template | Site | Key Visual Identity |
|---|---|---|
| `airbnb.md` | Airbnb | Warm coral accent, photography-driven, rounded UI |
| `apple.md` | Apple | Premium white space, SF Pro, cinematic imagery |
| `bmw.md` | BMW | Dark premium surfaces, precise engineering aesthetic |
| `ibm.md` | IBM | Carbon design system, structured blue palette |
| `nvidia.md` | NVIDIA | Green-black energy, technical power aesthetic |
| `spacex.md` | SpaceX | Stark black and white, full-bleed imagery, futuristic |
| `spotify.md` | Spotify | Vibrant green on dark, bold type, album-art-driven |
| `uber.md` | Uber | Bold black and white, tight type, urban energy |

---

## Featured Previews

### Stripe — Signature purple gradients, weight-300 elegance
```
Primary:    #635bff (purple CTA), #0a2540 (navy text)
Background: #ffffff → #f6f9fc (gradient sections)
Typography: Source Sans 3, weight 300-600, -0.3px letter-spacing
Shadow:     subtle 0 2px 5px rgba(0,0,0,0.05) card lift
```

### Linear — Ultra-minimal dark-mode, precise, purple accent
```
Primary:    #5e6ad2 (purple accent)
Background: #1a1a1a (dark canvas), #222222 (cards)
Typography: Geist / Inter, weight 400-600, -0.01em tracking
Border:     rgba(255,255,255,0.06) whisper lines
```

### Notion — Warm minimalism, serif headings, soft surfaces
```
Primary:    #0075de (Notion Blue)
Background: #ffffff / #f6f5f4 (warm white alternation)
Typography: Inter weight 300-700, -2.125px at 64px display
Shadow:     4-layer whisper stack (max opacity 0.04)
```

### Vercel — Black and white precision, Geist font system
```
Primary:    #000000 (text), #ffffff (bg)
Accent:     #0070f3 (blue), #7928ca (purple gradient partner)
Typography: Geist / Geist Mono, geometric compressed
Border:     rgba(0,0,0,0.08) hairline
```

### Apple — Premium white space, SF Pro, cinematic imagery
```
Primary:    #1d1d1f (text), #f5f5f7 (section bg)
Accent:     #0071e3 (Apple Blue), #2997ff (lighter blue)
Typography: SF Pro Display (Inter substitute), -0.022em tracking
Shadow:     complex multi-layer, subtle depth
```

---

## How Each Template Is Structured

Every `.md` template follows 9 standard sections:

1. **Visual Theme & Atmosphere** — The philosophy behind the design
2. **Color Palette & Roles** — Every hex value with semantic meaning
3. **Typography Rules** — Complete hierarchy table with sizes, weights, letter-spacing
4. **Component Stylings** — Buttons, cards, inputs, navs with exact CSS
5. **Layout Principles** — Spacing scale, grid, whitespace, border radius scale
6. **Depth & Elevation** — Shadow stacks with layer-by-layer values
7. **Responsive Behavior** — Breakpoints, collapsing strategy, touch targets
8. **Accessibility & States** — Focus rings, contrast ratios, interactive states
9. **Agent Prompt Guide** — Copy-paste prompts for instant generation

---

## Choosing a Design

| Use Case | Recommended Templates |
|---|---|
| Developer tools / dashboards | Linear, Vercel, Supabase, Raycast, Sentry, PostHog |
| Documentation / content sites | Mintlify, Notion, Sanity, MongoDB, ClickHouse |
| Marketing / landing pages | Stripe, Framer, Apple, SpaceX, Webflow |
| Dark mode UIs | Linear, Cursor, ElevenLabs, Warp, Superhuman |
| Light / clean UIs | Vercel, Stripe, Notion, Cal.com, Replicate |
| Playful / friendly | PostHog, Figma, Lovable, Zapier, Miro, Airtable |
| Premium / luxury | Apple, BMW, Stripe, Superhuman, Revolut |
| Data-dense / dashboards | Sentry, Kraken, Cohere, ClickHouse |
| Monospace / terminal aesthetic | Ollama, OpenCode, x.ai, VoltAgent |
| Fintech / trust-focused | Coinbase, Revolut, Wise, Kraken |

---

## Ecosystem

Part of the **HermesMade** toolkit:

| Tool | Description |
|---|---|
| [task-cost-estimator](https://github.com/minirr890112-byte/task-cost-estimator) | Estimate dev task costs with AI |
| [api-cost-compare](https://github.com/minirr890112-byte/api-cost-compare) | Compare LLM API pricing |
| [model-watch](https://github.com/minirr890112-byte/model-watch) | Monitor new model releases |
| [prompt-inspector](https://github.com/minirr890112-byte/prompt-inspector) | Analyze and optimize prompts |
| [code-inspector](https://github.com/minirr890112-byte/code-inspector) | Code quality analysis |
| [llm-deploy-helper](https://github.com/minirr890112-byte/llm-deploy-helper) | Deploy LLM inference servers |

---

## ⭐ Why Star?

**1,910 developers downloaded this from ClawHub** — making it the most-downloaded HermesMade skill. This represents thousands of hours of CSS pain avoided.

If these design tokens saved you time building a landing page, a star helps other developers discover it too. It's the only currency open source has.

---

## License

MIT © [HermesMade](https://github.com/minirr890112-byte)

Design systems sourced from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — all design tokens are factual descriptions of publicly accessible websites.
