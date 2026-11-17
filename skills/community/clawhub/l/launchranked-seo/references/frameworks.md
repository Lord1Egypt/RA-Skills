# Where SEO fixes live, by framework

Fix the thing that *generates* the tag. Check the repo's existing SEO helpers first (a `seo.ts`, a `<Seo>` component, a head partial) and extend them instead of adding a second system.

## Next.js (App Router, `app/`)

- **Site defaults**: `app/layout.tsx` → `export const metadata: Metadata = { metadataBase: new URL("https://example.com"), title: { default: "Brand", template: "%s | Brand" }, description, openGraph, twitter: { card: "summary_large_image" } }`. Without `metadataBase`, relative OG and canonical URLs break.
- **Per page**: `export const metadata` or `export async function generateMetadata({ params })` in `page.tsx`. Only server components can export metadata. For a `"use client"` page, move the export to the page's server wrapper or its layout.
- **Canonical**: `alternates: { canonical: "/pricing" }` (resolved against `metadataBase`). Next.js adds no canonical by default.
- **noindex**: `robots: { index: false, follow: true }`.
- **Sitemap / robots**: `app/sitemap.ts` (returns `MetadataRoute.Sitemap`) and `app/robots.ts` (returns `MetadataRoute.Robots`, including `sitemap: "https://example.com/sitemap.xml"`).
- **OG image**: `app/opengraph-image.tsx` (or per route segment) using `ImageResponse` from `next/og`.
- **JSON-LD**: in the page component, `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\\u003c") }} />`.
- **llms.txt**: `public/llms.txt`, or `app/llms.txt/route.ts` returning `text/plain` if it should be generated.
- **lang**: `<html lang="en">` in the root layout.

## Next.js (Pages Router, `pages/`)

- Per page tags with `next/head`. Put site defaults in a shared `<Seo>` component used by every page.
- `<Html lang="en">` in `pages/_document.tsx`.
- Sitemap: `next-sitemap` (postbuild) or `pages/sitemap.xml.ts` writing XML in `getServerSideProps`. Robots: `public/robots.txt`.

## Astro

- Tags in the shared layout's `<head>` (`src/layouts/*.astro`), fed by props from each page.
- Set `site: "https://example.com"` in `astro.config.mjs`. Canonical: `new URL(Astro.url.pathname, Astro.site)`.
- Sitemap: `@astrojs/sitemap` integration (needs `site`). Robots: `public/robots.txt` or `src/pages/robots.txt.ts`.
- JSON-LD: `<script type="application/ld+json" set:html={JSON.stringify(data)} />`.

## SvelteKit

- `<svelte:head>` in `+page.svelte` / `+layout.svelte`. `lang` in `src/app.html`.
- Sitemap: `src/routes/sitemap.xml/+server.ts` returning XML. Robots: `static/robots.txt`.
- Static content pages: `export const prerender = true`.

## Nuxt 3

- `useSeoMeta({ title, description, ogTitle, ogDescription, ogImage, twitterCard })` per page. Use `useHead({ link: [{ rel: "canonical", href }], htmlAttrs: { lang: "en" } })` for the rest.
- Sitemap and robots: `@nuxtjs/sitemap` and `@nuxtjs/robots` (or the Nuxt SEO bundle).
- Keep SSR on. `ssr: false` makes pages invisible to crawlers that don't run JavaScript.

## Remix / React Router v7 (framework mode)

- `export const meta: MetaFunction = () => [{ title }, { name: "description", content }, { tagName: "link", rel: "canonical", href }]`.
- Sitemap and robots as resource routes, e.g. `app/routes/sitemap[.]xml.ts` with a `loader` returning a `Response` with `Content-Type: application/xml`.

## Client-only SPA (Vite or CRA React, Vue without SSR)

The HTML every crawler first sees is `index.html`: one title, no content. `react-helmet` / `vue-meta` tags only exist after JavaScript runs, and most AI crawlers never run it.

- Best: prerender the routes at build time (e.g. `vite-react-ssg`, `vite-ssg` for Vue, Vike), or move marketing pages to an SSR/SSG framework.
- Minimum: make `index.html`'s static title, description, OG tags and JSON-LD right for the home page, and serve `public/robots.txt`, `public/sitemap.xml` and `public/llms.txt` as static files.

## Gatsby

- `export const Head = () => (<><title>…</title><meta name="description" content="…" /></>)` per page. Sitemap: `gatsby-plugin-sitemap`.

## Static site generators

- **Hugo**: `layouts/partials/head.html` (or `baseof.html`). Set `baseURL`. Canonical `{{ .Permalink }}`. Built-in `/sitemap.xml`. `enableRobotsTXT = true` plus `layouts/robots.txt`.
- **Jekyll**: `jekyll-seo-tag` (`{% seo %}` in the head) and `jekyll-sitemap`. Set `url` in `_config.yml`.
- **Eleventy**: the base layout's head. Sitemap from a `sitemap.xml.njk` template over `collections.all`.

## CMS and site builders

- **WordPress**: titles, meta, sitemaps and schema usually come from an SEO plugin (Yoast, Rank Math), which is configured, not coded. Custom themes need `add_theme_support('title-tag')` and `wp_head()` in `header.php`.
- **Shopify themes**: `layout/theme.liquid` (`{{ page_title }}`, `{{ page_description }}`, `canonical_url`). Product JSON-LD in the product section.
- **Webflow, Framer, Wix, Squarespace**: per-page SEO settings live in their dashboards. Give the user exact settings to change; there's no code to edit.

## Host-level fixes (any framework)

- **www vs apex, http → https**: one 301 at the host or CDN (Vercel domain settings, Netlify `_redirects`, Cloudflare redirect rules), not in app code.
- **Trailing slashes**: pick one in framework config (`trailingSlash` in Next.js, Astro and Nuxt) and match the sitemap and canonicals to it.
- **Security headers / HSTS**: `headers()` in `next.config`, `vercel.json`, or `_headers` on Netlify / Cloudflare Pages.
- **Slow TTFB**: static generation or caching (ISR, CDN cache headers) before code-level tuning.
