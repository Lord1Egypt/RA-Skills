# Phase 1 — Build the Static Site

Deep details for the build half. SKILL.md gives the high-level flow; this file is what to consult while writing the actual Astro project.

## Locked-in stack — do not deviate

| Layer | Choice | Why |
|---|---|---|
| Framework | **Astro 6** with `trailingSlash: 'always'`, `build.format: 'directory'`, static output | Marketing sites want HTML on disk. Astro emits clean per-route directories and zero JS by default. |
| Islands | **React 19** via `@astrojs/react ^5`, ONLY for the mobile menu | Marketing site = mostly static. Pulling React in for a single interactive island is the right boundary. Don't make the whole site an SPA. |
| Styling | **Tailwind CSS 4** via `@tailwindcss/vite` (NOT `@astrojs/tailwind`) | The Vite plugin is the supported path in Tailwind 4. The old `@astrojs/tailwind` integration relies on Tailwind 3's PostCSS pipeline. |
| Tailwind config | `@import "tailwindcss";` + `@theme` directive inside `src/styles/global.css` | Tailwind 4's CSS-first config. No `tailwind.config.mjs` needed. |
| Package manager | **pnpm** with `"packageManager": "pnpm@10.x"` in `package.json` | Repeatable installs, matches the rest of the Tenshow stack. |
| Runtime | **Node 22+** | We use `--env-file-if-exists=.env` natively, no `dotenv` dep. |
| Language | **TypeScript strict** | |
| Images | **Zero external image files.** Logo, icons, hero visuals = inline SVG + CSS gradients | Faster, simpler, no broken-image risk, no CDN egress cost on a marketing page. |
| UI / animation libs | **None.** Tailwind utilities + handwritten `@keyframes` | Marketing pages don't need a UI kit. Bundle size and visual differentiation both win. |
| Fonts | System stack — `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif` | Bilingual zh/en. System fonts render correctly on both. No FOIT, no third-party request. |
| Brand accent color | Extract from the brand logo's actual hex values (read the SVG) | Visual coherence between logo and accents on the page. |

**`pnpm deploy` is a pnpm built-in workspace command** — calling it outside a workspace errors with `ERR_PNPM_CANNOT_DEPLOY`. Always invoke custom scripts via `pnpm run <name>` (or just `pnpm <name>` for non-conflicting names). Document this in the project's README so future contributors don't trip on it.

## Astro config

Copy [`../assets/templates/astro.config.mjs`](../assets/templates/astro.config.mjs) and adjust `site` to the deployment domain. Don't change the other options — they're load-bearing for the deploy workflow (e.g. `trailingSlash: 'always'` matches how CDN/TOS serve `index.html` from a directory key).

## Content management — single source of truth

Every user-visible string lives in **`src/content/site.ts`**, exported as a type-safe `SITE: Record<Locale, SiteContent>` map. Top-level sections:

```text
SITE.zh.seo          SITE.zh.nav     SITE.zh.hero    SITE.zh.about
SITE.zh.products     SITE.zh.focus   SITE.zh.news    SITE.zh.contact
SITE.zh.footer
SITE.en.<same structure>
```

Plus two companion constants:

```ts
export const COMPANY = {
  nameZh, nameEn, domain, email,
  icp,                // ICP record number from MIIT filing
  publicSecurity,     // 公安备案号 — PLACEHOLDER until the user provides it
  icpUrl,             // typically beian.miit.gov.cn
  year,               // copyright year
};

export const PRODUCTS: Product[] = [/* … */];
```

Each `Product` has bilingual `name: {zh, en}`, `desc: {zh, en}`, a `url`, an `accent` hex color, and an `icon` enum keyed to a path map in `ProductCard.astro`. This pattern lets non-developers edit copy by touching exactly one file.

**Placeholder discipline**: `publicSecurity` is almost always a placeholder when scaffolding. Flag it loudly in the README so the user replaces it before launch. Same for any `CHANGE-ME` values in `deploy.config.mjs`.

## Brand mark extraction

The user's brand kit typically has an icon-only or short-horizontal SVG (e.g. `Tenshow_short1.svg`). The mark itself is the **last 3 paths** of that file — read the SVG and extract them verbatim.

Use [`../assets/templates/BrandMark.astro`](../assets/templates/BrandMark.astro) as a starting point. It takes:

- `size` (default 32)
- `inverted` (boolean) — when true, the mark renders as a white silhouette against dark backgrounds (for the footer)
- `class` (passthrough)

And renders the three paths with theme-aware fills (dark color, light color, cutout color). For the favicon, reuse the same paths centered in a 256×256 viewBox with `<rect rx=56 fill=white>` behind them.

The reference project has a complete working `BrandMark.astro` — when the brand is different, swap in the new path strings, update the fills to match the brand palette, and verify by rendering at multiple sizes.

## SEO + accessibility — non-negotiable

- One `<h1>` per page (in the Hero section)
- `<html lang="zh-CN">` for Chinese pages, `<html lang="en">` for English pages
- Hreflang alternates on every page:
  ```html
  <link rel="alternate" hreflang="zh-CN" href="https://<domain>/" />
  <link rel="alternate" hreflang="en"    href="https://<domain>/en/" />
  <link rel="alternate" hreflang="x-default" href="https://<domain>/" />
  ```
- Canonical URL per page
- Open Graph + Twitter Card meta in `BaseLayout.astro`
- `scroll-margin-top: 5rem` on `section[id]` so anchor links don't get hidden under the sticky header
- `@media (prefers-reduced-motion: reduce)` opts out of `scroll-behavior: smooth`

## Hero visual recipe

The hero is the single most important visual decision. Use this exact recipe for consistency across Tenshow marketing sites — the result is distinctive but not flashy, ships zero external assets, and degrades gracefully.

```astro
<section class="relative isolate overflow-hidden">
  <!-- Background grid -->
  <div
    aria-hidden="true"
    class="absolute inset-0 -z-10"
    style="
      background-image:
        linear-gradient(rgba(15,15,15,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,15,15,0.06) 1px, transparent 1px);
      background-size: 48px 48px;
    "
  />

  <!-- Accent radial glow (positioned where it complements the headline) -->
  <div
    aria-hidden="true"
    class="absolute -z-10 ..."
    style="
      background: radial-gradient(circle, rgba({{ACCENT_RGB}}, 0.22), transparent 65%);
      filter: blur(40px);
    "
  />

  <!-- Status pill with pulsing dot -->
  <span class="inline-flex items-center gap-2 rounded-full ...">
    <span class="relative flex h-2 w-2">
      <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
      <span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
    </span>
    Status copy
  </span>

  <!-- Gradient headline -->
  <h1 class="bg-gradient-to-br from-neutral-900 via-neutral-700 to-[{{ACCENT_HEX}}] bg-clip-text text-transparent">
    Headline
  </h1>

  <!-- CTAs -->
  <a class="rounded-full bg-neutral-900 text-white ...">Primary</a>
  <a class="rounded-full border border-neutral-900 ...">Secondary</a>
</section>
```

Replace `{{ACCENT_HEX}}` and `{{ACCENT_RGB}}` with the values extracted from the brand SVG. The reference project's `Hero.astro` is the production version of this recipe — use it for the exact class names and spacing.

## File layout the scripts expect

```text
my-site/
├── astro.config.mjs               # from assets/templates/
├── deploy.config.mjs              # from assets/templates/, with values filled in
├── package.json                   # from assets/templates/, with name + scripts
├── tsconfig.json                  # strict, Astro defaults
├── public/                        # favicon.svg, robots.txt, sitemap.xml (Astro emits)
├── src/
│   ├── content/site.ts            # single source of truth for all copy
│   ├── components/                # Astro components + BrandMark + the single React island
│   ├── layouts/BaseLayout.astro   # html, head, SEO, language switch
│   ├── pages/
│   │   ├── index.astro            # zh root
│   │   ├── 404.astro
│   │   └── en/
│   │       └── index.astro        # en root
│   └── styles/global.css          # @import "tailwindcss"; + @theme tokens
└── scripts/                       # copied verbatim from assets/scripts/
    ├── lib/volc-api.mjs
    ├── setup-bucket.mjs
    ├── deploy.mjs
    ├── cdn-setup.mjs
    ├── cdn-refresh.mjs
    └── cdn-payloads/
        ├── apex.json              # from assets/cdn-payloads/, with placeholders replaced
        └── www.json
```

If the layout differs, the Phase-2 scripts will fail in non-obvious ways — `setup-bucket.mjs` reads `deploy.config.mjs` from project root, `cdn-setup.mjs` reads `scripts/cdn-payloads/*.json`, `deploy.mjs` walks `dist/`. Keep the layout.
