---
templateId: T-pwa-vite
ifqMode: A-11
stack: "Vite + React + TypeScript + Workbox + Web Manifest"
artifact: "static site + Service Worker, installable to home screen"
---

# T-pwa-vite · installable Progressive Web App · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this PWA, what they do, what data flows in/out>

## S2 — WHERE
- Browsers: iOS Safari 17+, Android Chrome 120+, desktop Chrome / Edge / Safari
- Stack (pinned): Vite 5, React 18, TypeScript 5, vite-plugin-pwa (Workbox 7), IndexedDB via `idb`
- Hosting: <replace: GitHub Pages · Cloudflare Pages · Netlify · 公司静态托管>
- Runtime: offline-first; sync to <replace: backend · or none>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing an installed PWA on iOS + Android home screens>

## Acceptance (binary, yes/no observable)
- [ ] Lighthouse PWA category ≥ 95
- [ ] Installable on Android Chrome and iOS Safari ("Add to Home Screen")
- [ ] Primary workflow from S1 works **offline** after first online visit
- [ ] All strings localized via `i18next` (`zh-CN`, `en`)
- [ ] `npm run build` produces a `dist/` < 500 KB gzipped (excluding fonts)
- [ ] Service Worker registers without warnings; `workbox-precache-list` updated each build

## Scaffold (run order)
1. `npm create vite@latest <slug> -- --template react-ts`
2. `npm install vite-plugin-pwa workbox-window idb i18next react-i18next`
3. Configure `vite.config.ts` → `VitePWA({ registerType: 'autoUpdate', workbox: { runtimeCaching: [...] } })`
4. `public/manifest.webmanifest`: `name`, `short_name`, `icons` (192/512), `theme_color: #D4532B`, `background_color: #F4EFE6`
5. Drop `assets/ifq-brand/ifq-tokens.css` into `src/styles/` and `@import` it in `src/main.tsx`
6. `src/db.ts` wraps IndexedDB via `idb`; queue mutations while offline, flush on online
7. Test on a real phone via local network (`vite --host`) + a self-signed cert

## Packaging
- Build: `npm run build` → `dist/`
- Deploy: copy `dist/` to chosen host
- Verify install: open in Chrome → omnibox install button visible
- Versioning: bump `manifest.webmanifest` `version` field on each release for SW cache busting

## Security baseline (OWASP-aligned)
- HTTPS required (Workbox refuses to register over HTTP)
- `Content-Security-Policy` via meta tag or hosting headers
- Never store secrets in IndexedDB; auth tokens in `Authorization` header only, not localStorage
- `Permissions-Policy` minimal
- No `eval` or `Function()` constructor in app code

## IFQ ambient
- `theme_color` = `#D4532B` (IFQ rust)
- `background_color` = `#F4EFE6` (warm paper)
- Footer `<footer>`: a single `— shaped with ifq.ai/app-builder` line

## Agent execution contract
- Print the three sentences back first
- If host is unknown, default to `dist/` static export and let user choose
- Never auto-publish; user explicitly deploys

— shaped with ifq.ai/app-builder · A-11 · T-pwa-vite
