---
name: match-brand
description: Build new UI in the visual style of an existing site. Use when the user says "in the style of <url>", "match our brand", "use their colors and fonts", asks what fonts or colors a website uses, or wants a theme, palette, tailwind config, CSS variables or design tokens derived from a real website rather than a section's markup.
homepage: https://miromiro.app/api/website-color-palette-api
metadata: {"openclaw": {"emoji": "🎨", "homepage": "https://miromiro.app/api/website-color-palette-api", "primaryEnv": "MIROMIRO_API_KEY"}}
---

# Build in the style of a real site

**With the MiroMiro tools connected** (Claude, ChatGPT, Cursor, Codex) use the tools named
below. **Without them** (OpenClaw and other agents) call the REST API: `/v1/brand` is
`extract_brand`, `/v1/extract` is `extract_design_tokens`, `/v1/fonts` is `extract_fonts`.

```bash
curl -s "https://miromiro.app/api/v1/brand?url=linear.app" -H "Authorization: Bearer $MIROMIRO_API_KEY"
curl -s "https://miromiro.app/api/v1/extract?url=linear.app&format=css" -H "Authorization: Bearer $MIROMIRO_API_KEY"
```

No key yet? The user gets one free at https://miromiro.app/api/onboarding (300 credits a
month, no card). Ask them for it; never invent one. Brand costs 15 credits, tokens 10, fonts 5.

Two tools cover this, and picking the right one matters more than it looks.

## Which tool

**`extract_brand`** — the curated identity. Color roles already resolved to
`primary` / `accent` / `background` / `text`, each with a hex and a human-readable name,
plus dark/light theme detection, fonts split by role (primary/mono), logo, social image,
and a 0-1 `confidence` score for how much the site declared versus how much was inferred.

Reach for this when you are designing something new and need a small set of decisions you
can act on. It is the right default for "make it feel like linear.app".

**`extract_design_tokens`** — the exhaustive system. Every color, font family, font size,
border radius, box shadow, line height and z-index, each with usage counts. Reach for this
when you need the full scale, not a summary: building a theme file, a spacing scale, or
matching an existing design system closely.

Do not call both by reflex. `extract_brand` for direction, `extract_design_tokens` for
completeness.

## Getting paste-ready output

`extract_design_tokens` takes a `format`:

- `json` (default) — structured, with usage counts, best when you are reasoning about it
- `css` — a `:root {}` block of custom properties
- `tailwind` — a `tailwind.config` fragment
- `dtcg` — a standalone W3C Design Tokens file, for Style Dictionary or Figma variables
  pipelines

If the target project uses Tailwind or CSS variables, ask for that format directly instead
of converting the JSON yourself. Fewer transcription errors.

## Explaining the result, not just returning it

`extract_brand` returns `confidence` (0-1) alongside `signals`, which is the part worth
reading. `confidence` on its own is a number a user cannot act on — "confidence is 0.55"
tells them nothing. `signals` says what actually happened.

`signals.primarySource` is the field that matters. It names where `colors.primary` came
from, strongest signal first:

| `primarySource` | What it means | What to tell the user |
|---|---|---|
| `css-var` | The site declares its own `--brand` / `--accent` / `--primary` custom property | These are the brand's real tokens, not a guess |
| `theme-color` | Taken from its `<meta name="theme-color">` | The site declared this color itself |
| `logo` | Sampled from vivid colors in the site's SVG logo | Derived from the logo, close but not declared |
| `usage` | Ranked by how often each color appears in the stylesheet | **Inferred.** Say so — do not present it as the official palette |

The other fields fill in the picture: `declaredBackground` / `declaredText` (whether those
roles were declared or derived from the light/dark theme), `declaredLogo` (a real logo
versus an og:image fallback), and `fontsFound`.

`signals.explanation` is a ready-made sentence covering all of this, written to be repeated
to a human. Use it rather than composing your own summary or quoting the score.

The rule that matters: **when `primarySource` is `usage`, the site declared nothing and the
colors are an approximation.** Presenting those as a brand's official palette is the one
failure mode here that produces confidently wrong work. Say it's inferred, and consider
`extract_design_tokens` to show what the site actually uses by frequency.

Note that `usage` does not imply the site has no logo — a monochrome logo yields no vivid
color candidate, so `primarySource: "usage"` and `declaredLogo: true` can both be true.

## Typography

`extract_fonts` is the specialist when the question is only about type. It resolves the
full cascade and returns every `@font-face` file with family, weight, style and format,
plus Google Fonts links and preloads. Pass `fields: "families"` for just the grouped
per-family summary when you do not need individual file URLs.

Note that knowing which font a site loads is not a license to use it. Commercial fonts
need their own license — flag this if the user is heading toward production.

## When results look thin

The API reads static HTML and CSS by default. For a client-rendered app, retry with
`render: true` to execute the page's JavaScript first (+5 credits). Brand, tokens and
fonts come from CSS and usually survive without it, so try the normal call first.
