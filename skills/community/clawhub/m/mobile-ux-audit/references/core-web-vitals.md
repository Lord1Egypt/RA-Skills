# Core Web Vitals — Practical Guide

Core Web Vitals are three metrics Google uses to score user experience. They correlate strongly with conversion on ecommerce sites.

## The three metrics

### LCP — Largest Contentful Paint

Time from navigation start to the render of the largest visible content element (usually the hero image or H1).

- **Good**: ≤2.0s
- **Needs improvement**: 2.0–2.5s
- **Poor**: >2.5s

Common causes of poor LCP:

- Hero image too large or served at desktop resolution on mobile.
- Slow server response (TTFB >600ms).
- Render-blocking CSS or JS.
- Font loading delay for the text that is the LCP element.

### INP — Interaction to Next Paint

Time from user interaction (tap, click, key press) to the next frame that reflects the result. Replaced FID in 2024.

- **Good**: ≤150ms
- **Needs improvement**: 150–300ms
- **Poor**: >300ms

Common causes of poor INP:

- Heavy JavaScript on interaction (tracking calls, re-renders).
- Long tasks blocking the main thread.
- Synchronous handlers that should be async.
- Third-party scripts doing work on every interaction.

### CLS — Cumulative Layout Shift

Sum of unexpected layout shifts during the page's lifetime. A tap moving because an ad loaded is a bad CLS event.

- **Good**: ≤0.05
- **Needs improvement**: ≤0.1
- **Poor**: >0.1

Common causes of poor CLS:

- Images without width/height attributes.
- Ads or embeds inserted without reserved space.
- Fonts that reflow text (use `font-display: optional` or preload).
- Dynamically injected content above existing content.

## Field data vs. lab data

**Field data** (CrUX, RUM): real users, varied devices and networks. This is what Google uses for ranking and what reflects real conversion.

**Lab data** (Lighthouse, WebPageTest): consistent hardware and network. Good for catching regressions in CI; do not use as your only signal.

Always lead with field data. Lab data is a proxy.

## How to get field data

### For a public site

- **PageSpeed Insights**: enter your URL, see CrUX data if your site has enough traffic.
- **Google Search Console**: Core Web Vitals report with URL groups.
- **CrUX API / CrUX Dashboard**: historical trends by country.

### For your own users

- **web-vitals library** (by Google): tiny JS, reports to your analytics.
- **Datadog RUM**, **New Relic Browser**, **Sentry Performance**: paid RUM services.
- **Shopify Web Performance** dashboard for Shopify stores.
- **Vercel Analytics** for Vercel-hosted Next.js apps.

## How to improve LCP

1. Identify the LCP element in DevTools Performance tab.
2. If it's an image: serve a properly sized WebP/AVIF with `fetchpriority="high"` and preload.
3. If it's text: preload the font, use `font-display: optional`.
4. Reduce server response time (TTFB target <600ms).
5. Minimize render-blocking CSS; inline critical CSS for above-fold content.
6. Defer non-critical JavaScript.

## How to improve INP

1. Identify slow interactions with the INP dev tool or `event-timing` API.
2. Break long tasks with `setTimeout(fn, 0)`, `scheduler.yield()`, or `requestIdleCallback`.
3. Move heavy work to a web worker.
4. Audit third-party scripts — defer, async, or remove.
5. Reduce React re-renders (memoization, virtualization for long lists).
6. Show feedback (loading state) immediately on tap; do real work asynchronously.

## How to improve CLS

1. Add `width` and `height` attributes to every image.
2. Reserve space for ads, embeds, and dynamically inserted components.
3. Preload critical fonts to prevent FOUT reflow.
4. Use CSS transforms for animations (not layout-triggering properties).
5. Avoid inserting content above existing content unless user-initiated.

## Setting realistic targets

- For a greenfield headless build: green on all three is achievable within the first quarter of launch.
- For an older Shopify or Magento store: LCP and CLS are usually fixable in weeks; INP takes months because JavaScript debt accumulated over years.
- The biggest conversion wins come from moving from "Poor" to "Needs improvement" on any metric — not from "Needs improvement" to "Good."
