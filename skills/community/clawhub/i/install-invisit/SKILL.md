---
name: install-invisit
description: "Add invisit cookieless web analytics to a website or web app with the script tag or the @invisitdev/web npm package, then check that visits arrive. Use when asked to add invisit, privacy-friendly analytics, or a cookie-free Google Analytics alternative to a project."
---

# Install invisit

invisit is cookieless web analytics: no cookies, no consent banner, realtime visitors, AI assistant referrals, revenue and web vitals. Full docs as Markdown: https://invisit.dev/llms.txt

## 1. Get the site id

The person signs up at https://app.invisit.dev/auth, adds a site with its domain, and copies the **site id** from **Settings → Installation**. Ask them for it; never invent one. The id is public: it is safe in client code and in `PUBLIC_` or `NEXT_PUBLIC_` environment variables.

## 2. Add the tracker

Prefer the installer, once you have the id from the person: run `npx invisit init --site <site id>` in the project's directory. It detects the framework, installs the package and edits the right file; `--dry-run` shows the diff first. It exits 0 when done or already set up, and when it could not place an edit safely it changes nothing and prints the snippet and file to paste it into: follow those steps. It exits 1 when it needs input (a site id, or `--dir <app>` at a monorepo root). Otherwise, add it by hand.

Pick one, never both.

**No build step** (static HTML, WordPress, Webflow, Shopify themes): put this in the `<head>` of every page.

```html
<script
  async
  src="https://api.invisit.dev/invisit.js"
  data-site="<site id>"
  data-collector="https://api.invisit.dev"
></script>
```

Keep `data-collector`: without it the script sends events to the page's own origin.

**Bundled app** (Next.js, React Router, TanStack Start, Nuxt, SvelteKit, Astro, Angular, SolidStart, Vite):

```sh
npm install @invisitdev/web
```

```ts
import { init } from '@invisitdev/web'

init({ site: '<site id>' })
```

Call `init()` once, in the browser, as early as the app allows. It follows client-side navigation by itself, and it is a no-op on the server, so importing it from shared code is safe. Where the line goes in each framework: https://invisit.dev/docs/web/frameworks.md

## 3. Custom events (optional)

```ts
import { track } from '@invisitdev/web'

track('signup', { plan: 'pro' })
```

Events from a backend go through `@invisitdev/server`: https://invisit.dev/docs/server/sdk.md. Event naming and properties: https://invisit.dev/docs/guides/events.md

## 4. Check that it works

Deploy, open the site, then open **Realtime** in the dashboard: the visit shows up within seconds. If nothing arrives, **Settings → Blocked traffic** lists what the collector refused and why; the usual cause is the site's domain missing from **Settings → Collection**. **Settings → Debug** opens the site in a sandbox, localhost included, and shows each event with the collector's verdict without counting it.

## Reference

- Options for `init()` and the script's `data-*` attributes: https://invisit.dev/docs/web/installation.md
- Full API of `@invisitdev/web`: https://invisit.dev/docs/reference/web.md
- Privacy, consent and excluding traffic: https://invisit.dev/docs/guides/privacy.md
