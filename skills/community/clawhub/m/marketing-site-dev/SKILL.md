---
name: marketing-site-dev
description: Opinionated end-to-end workflow for shipping a bilingual (中文/English) static company marketing site to Volcengine — Astro 6 + React 19 islands + Tailwind 4, deployed to TOS + CDN with HTTPS, force-redirect, HSTS, and HTTP/2, entirely via the `ve` CLI and Node SDKs. Use whenever the user mentions building, scaffolding, deploying, or updating a company / brand / product / 公司官网 / 营销网站 / 品牌站 / marketing site, ESPECIALLY when Volcengine (火山引擎), TOS, CDN, ICP 备案, or Chinese deployment is involved. Also trigger when the user provides a company brief with product list + brand assets and asks for a "single command deploy" or "production-ready landing page", or references files like `astro.config.mjs`, `deploy.config.mjs`, `scripts/cdn-setup.mjs`, `scripts/setup-bucket.mjs`. Prefer this skill over generic web-dev guidance whenever the target deployment is Volcengine + China mainland.
license: MIT
compatibility: Designed for Claude Code and compatible agents. Requires Node.js 22+, pnpm 10+, the Volcengine `ve` CLI (1.0.x+), and network access to npm + Volcengine OpenAPI. Domain must already be ICP-filed and ideally hosted on Volcengine DNS. macOS / Linux recommended.
metadata:
  author: "北京腾秀创智技术有限公司 (Tenshow Innovation)"
  organization: tenshowinnovation.com
  version: "0.1.0"
---

# Marketing Site Dev (Volcengine)

End-to-end skill for building and shipping a bilingual static company marketing site to Volcengine. Two phases:

1. **Build** — Astro 6 + React 19 islands (mobile menu only) + Tailwind 4. Inline SVG everywhere. Single content file (`src/content/site.ts`) is the source of truth.
2. **Deploy** — TOS bucket + CDN + free DV cert + HTTPS hardening, all scripted in idempotent Node scripts via `ve` CLI and Volcengine OpenAPI (SigV4-signed via `volc-api.mjs` for the actions `ve` doesn't ship).

**What success looks like:** the user runs ~6 commands end-to-end and gets `https://<their-domain>/` serving a production-quality bilingual site with HTTPS, force-redirect to HTTPS, HSTS, HTTP/2, edge caching, and automated cache invalidation. Every infrastructure step is in version control as an idempotent script.

---

## Is this skill the right fit?

This is a **deliberately opinionated** workflow optimized for one specific scenario. Before going deep, check that scenario actually matches the user's situation. If it doesn't, surface the better alternative instead of forcing the user through a heavier path.

**Use this skill when:**

- The site is for a **Chinese company or a product targeting users in mainland China** — latency from mainland to non-Chinese CDNs is bad enough (200-400ms, often worse during peak hours) that visitors notice and bounce.
- **ICP 备案 is required or already in hand** — distributing in China legally needs the filing tied to a domain hosted on a Chinese cloud. Volcengine bundles 备案 assistance and offers it for the domain you deploy here.
- The user is already in the Volcengine ecosystem (other Volcengine services, existing TOS buckets, etc.) and consolidation is valuable.
- The bilingual zh/en pattern is desired — the content layer (`site.ts`) is designed around it.

**Use a simpler alternative when:**

| Scenario | Recommended alternative | Why |
|---|---|---|
| **Personal site / portfolio / side project, no Chinese audience requirement** | **GitHub Pages** | Free, auto-HTTPS, deploys on `git push`, no infra to manage. Zero of the Volcengine landmines apply. |
| **International-only audience (US/EU/SEA), no China presence planned** | **Vercel** (or Cloudflare Pages / Netlify) | Free tier, instant deploys from git, preview URLs per PR, automatic HTTPS, global edge network. Skip the whole `ve` CLI + ICP workflow entirely. |
| **Site needs serverless functions (forms, auth, dynamic content)** | **Vercel** or **Cloudflare Pages** with their edge functions | This skill ships purely static — Volcengine has serverless products, but the workflow here doesn't cover them. |
| **You want preview URLs per branch / PR-based review** | **Vercel** | Vercel's preview-URL UX is best-in-class. This skill produces one production deploy per push; no branch previews. |

If the user's situation matches the "use a simpler alternative" column, **tell them so explicitly** before scaffolding anything. A 2-minute Vercel deploy is a better experience than a 30-minute Volcengine bootstrap when the user doesn't need what Volcengine provides. Don't sunk-cost them into the wrong stack because they invoked this skill.

When in doubt, ask: "Will mainland-China users be a meaningful part of your audience, and do you have (or plan to file) ICP 备案 for the domain?" If both answers are no, point at Vercel / GitHub Pages and stop.

---

## Step 1: Capture intent (ALWAYS ASK FIRST)

Don't write any code until you have these six inputs from the user. If they're missing from the prompt, ask via `AskUserQuestion`. Most teams will have everything except possibly the public-security number — that one is OK as a placeholder.

| # | Input | Used for | Notes |
|---|---|---|---|
| 1 | **Company name** (Chinese + English) | `COMPANY.nameZh` / `COMPANY.nameEn` in `site.ts`; footer; SEO | |
| 2 | **Domain** (e.g. `example.com`) | Everywhere — bucket binding, CDN, DNS, cert SAN | MUST already be ICP-filed and ideally hosted on Volcengine DNS. If hosted elsewhere, the user needs to manually add CNAME + TXT records. |
| 3 | **Brand assets directory** (path to SVG logo files) | Inline `BrandMark.astro` extraction (last 3 paths of the short logo SVG) | Usually something like `assets/logo/svg/Tenshow_short1.svg` — short / icon-only variant. |
| 4 | **Product list** | `PRODUCTS[]` in `site.ts` | Each product needs bilingual name + description, URL, accent hex color, icon enum. |
| 5 | **ICP record number** | Footer | The MIIT-issued 备案号. |
| 6 | **Working directory** | Project root | Should be greenfield (empty) or you'll have to coordinate with existing files. |

Optionally:
- **公安备案号** (Public Security Bureau filing number) — usually a placeholder at scaffold time. Flag it loudly in the README so the user replaces it before launch.
- **Brand accent color** — extract from the logo SVG's hex values. If undecidable, default to whatever the dominant non-neutral color is.

---

## Step 2: Build the static site

Full details in [references/phase-1-static-site.md](references/phase-1-static-site.md). The shortlist:

1. **Scaffold** — copy [`assets/templates/package.json`](assets/templates/package.json) and [`assets/templates/astro.config.mjs`](assets/templates/astro.config.mjs) into the project root. Update `name` in package.json and `site` in astro.config.mjs.
2. **Install** — `pnpm install`.
3. **Create the source tree** matching the layout in [phase-1-static-site.md](references/phase-1-static-site.md) (`src/content/site.ts`, `src/components/`, `src/layouts/BaseLayout.astro`, `src/pages/index.astro`, `src/pages/en/index.astro`, `src/styles/global.css`).
4. **Extract the brand mark** from the user's SVG — use [`assets/templates/BrandMark.astro`](assets/templates/BrandMark.astro) as a starting point. The last 3 `<path>` elements of the short-logo SVG are the mark; copy them verbatim and pick fills from the brand palette.
5. **Build the sections** — Hero (with the exact recipe in [phase-1-static-site.md](references/phase-1-static-site.md) — grid background + radial glow + gradient headline + status pill + 2 CTAs), About, Products, Focus, Updates, Contact, Footer. Header sticky, mobile menu = the only React island.
6. **Verify locally** — `pnpm dev` to develop, `pnpm build && pnpm preview` to sanity-check the static output before touching infra.

### Stack lock-in (don't deviate)

Astro 6, React 19 (mobile menu only), Tailwind 4 via `@tailwindcss/vite`, pnpm 10, Node 22+, TypeScript strict, zero external images, zero UI libs, zero font services, system font stack. Rationale and full details in [phase-1-static-site.md](references/phase-1-static-site.md).

---

## Step 3: Set up deploy infrastructure

Full details in [references/phase-2-volcengine-deploy.md](references/phase-2-volcengine-deploy.md). **Read [references/landmines.md](references/landmines.md) FIRST** — half your time in this phase is avoiding the landmines, not running commands.

1. **Copy scripts** — copy the entire [`assets/scripts/`](assets/scripts/) directory and [`assets/cdn-payloads/`](assets/cdn-payloads/) into the user's `scripts/` and `scripts/cdn-payloads/` respectively. Copy [`assets/templates/deploy.config.mjs`](assets/templates/deploy.config.mjs) to the project root and fill in `bucket`, `region`, `endpoint`, `cdnDomains`.
2. **Replace placeholders in payloads** — `{{DOMAIN}}`, `{{BUCKET}}`, `{{REGION}}` in `scripts/cdn-payloads/apex.json` and `www.json`. **`OriginHost` must be the domain itself, not empty** — the templates are correct out of the box; if you edit them, preserve `OriginHost`. See [landmines.md #3](references/landmines.md).
3. **Create `.env`** at project root (gitignored):
   ```env
   VOLC_ACCESS_KEY=AK...
   VOLC_SECRET_KEY=...
   ```
   Volcengine AK/SK needs `TOSFullAccess`, `CDNFullAccess`, `DNSFullAccess`, `CertificateFullAccess` (or least-privilege equivalents).
4. **Verify `ve` is installed**: `ve version` — needs 1.0.x or later. If missing, install via Volcengine's official docs.

---

## Step 4: Execute the first deploy

```bash
pnpm install                        # if not done yet
pnpm build                          # verify local build works
pnpm run setup:bucket               # idempotent: bucket + website routing + custom-domain binding
pnpm run deploy:upload              # sync dist/ → bucket
# at this point: https://<bucket>.tos-<region>.volces.com/index.html should 200
pnpm run setup:cdn                  # verification → CDN add → CNAME → cert → HTTPS hardening
# wait 1-3 minutes for DNS propagation
pnpm run cdn:refresh                # purge edge cache so first-time hits don't return bucket-listing JSON
```

After this initial run, daily iteration becomes **one command**:

```bash
pnpm run deploy && pnpm run cdn:refresh
```

### Always use `pnpm run`, NOT bare `pnpm`

`pnpm deploy` is a pnpm built-in workspace command — it'll error with `ERR_PNPM_CANNOT_DEPLOY` outside a workspace. Use **`pnpm run deploy`** and **`pnpm run cdn:refresh`**. Document this in the project's README. See [landmines.md #6](references/landmines.md).

---

## Step 5: Verify

Run the curl + openssl checklist in [references/verification.md](references/verification.md). Expected: 5× HTTP 200 on key routes, 1× 301 on HTTP → HTTPS, valid cert with SAN covering apex + www, HTTP/2 + HSTS confirmed, cache-control headers matching `deploy.config.mjs` rules.

If any check fails, [verification.md](references/verification.md) maps each failure mode to the root cause and the fix.

---

## Critical landmines you must know before executing

Full enumeration in [landmines.md](references/landmines.md). The ones you'll hit if you skip reading:

1. **`HTTPS_PROXY` pollution** — TOS SDK + a local HTTP proxy = `Protocol "http:" not supported`. Every script in `assets/scripts/` already deletes proxy env vars at the top — preserve that preamble if you copy / adapt them.
2. **TOS SDK quirks** — `headBucket(string)` not `headBucket({bucket})`; `listObjectsType2` signature breaks when `continuationToken: undefined` is in the input; `putObject` defaults to private even on public-read buckets — always set `acl: 'public-read'`.
3. **TOS has no separate website endpoint hostname** — the same `<bucket>.tos-<region>.volces.com` returns either bucket-listing JSON or `index.html` depending on the `Host` header. You MUST (a) call `putBucketCustomDomain` per apex/www domain, AND (b) set `OriginHost` in the CDN `AddCdnDomain` payload to the user's domain (not empty).
4. **CDN ≠ DCDN for verification** — CDN (内容分发网络) wants TXT host `volccdnauth` and `cdn:CheckCdnDomain` (not in `ve` CLI — use `volc-api.mjs`). DCDN (全站加速) uses `_dnsauth` and `ve dcdn VerifyDomainOwnership`. Mixing them up = endless verification loop.
5. **TXT changes take ~10 min to propagate** at Volcengine's verifier. Get the value right on the first write; don't churn.
6. **`pnpm deploy` is a built-in.** Use `pnpm run deploy`.
7. **Free DV cert APPLICATION is console-only.** API issuance is blocked with permanent AK/SK (`OperationDenied.RequestFreeInstance`). But **listing already-issued certs works fine** — and free DV certs are often auto-issued at domain registration. Always `CertificateGetInstanceList` first; look in `Result.Instances[]` (NOT `InstanceList`, NOT `Data`) for one whose `San` covers both apex + www.

---

## Behavior rules

- **Plan first; confirm before destructive ops.** Before `createBucket`, `AddCdnDomain`, `DeleteRecord` on existing TXT, or `BatchDeployCert`, summarize what's about to happen and ask the user for confirmation.
- **Read existing state before writing.** Always `ListRecords` / `ListCdnDomains` / `CertificateGetInstanceList` first — free certs are often pre-issued, CDN domains may already exist, DNS records may already point at the right place. Idempotency is the whole point.
- **When `ve` lacks an action, use `volc-api.mjs`** rather than telling the user to upgrade `ve` or use the console. The only true console-only path is free DV cert issuance ([landmines.md #4](references/landmines.md)).
- **Don't churn DNS records.** Each TXT modification adds ~10 min cache. Get the host/value right the first time — `volccdnauth` for CDN, `_dnsauth` for DCDN, they're not interchangeable.
- **Surface every config decision in `deploy.config.mjs`**, never hardcode in scripts. Bucket, region, endpoint, CDN domains, cache rules — all live in the config so the user can edit one file to change everything.
- **`/usr/bin/curl` is more reliable than bare `curl`** when running checks after long commands in the same shell — bash PATH lookup occasionally goes weird. Same goes for tests in CI scripts.

---

## Bundled assets and references

### `assets/scripts/` (copy verbatim into the user's `scripts/`)

- [`lib/volc-api.mjs`](assets/scripts/lib/volc-api.mjs) — SigV4 signer, zero deps. Use for any action missing from `ve` CLI.
- [`setup-bucket.mjs`](assets/scripts/setup-bucket.mjs) — idempotent bucket + website + custom-domain binding.
- [`deploy.mjs`](assets/scripts/deploy.mjs) — TOS sync uploader with per-prefix `Cache-Control`, orphan deletion.
- [`cdn-setup.mjs`](assets/scripts/cdn-setup.mjs) — CDN orchestration: ownership verification → AddCdnDomain → CNAME → cert → HTTPS hardening.
- [`cdn-refresh.mjs`](assets/scripts/cdn-refresh.mjs) — cache invalidation via `cdn:SubmitRefreshTask` (signed by `volc-api.mjs`, works in CI without `ve`).

### `assets/cdn-payloads/` (copy into `scripts/cdn-payloads/`)

- [`apex.json`](assets/cdn-payloads/apex.json) and [`www.json`](assets/cdn-payloads/www.json) — `AddCdnDomain` payload templates with `{{DOMAIN}}`, `{{BUCKET}}`, `{{REGION}}` placeholders. `OriginHost` is set correctly out of the box — don't strip it.

### `assets/templates/` (copy into project root)

- [`astro.config.mjs`](assets/templates/astro.config.mjs) — locked-in Astro config. Only `site` should change per project.
- [`deploy.config.mjs`](assets/templates/deploy.config.mjs) — fill in `bucket`, `region`, `endpoint`, `cdnDomains`.
- [`package.json`](assets/templates/package.json) — scaffolded with the right dependencies + scripts. Update `name`.
- [`BrandMark.astro`](assets/templates/BrandMark.astro) — starting point for the brand mark component. Replace the three `<path>` elements with the user's logo paths.

### References (deep dives — read as needed)

- [`references/phase-1-static-site.md`](references/phase-1-static-site.md) — full Phase 1 walkthrough: stack rationale, content layout, brand mark extraction, SEO/a11y rules, hero visual recipe, file structure.
- [`references/phase-2-volcengine-deploy.md`](references/phase-2-volcengine-deploy.md) — full Phase 2 walkthrough: what `ve` can/can't do, the 5 scripts step-by-step, environment setup, the 12-step `cdn-setup.mjs` sequence with payload examples.
- [`references/landmines.md`](references/landmines.md) — every known gotcha (proxy pollution, TOS SDK quirks, CDN vs DCDN, TXT propagation, pnpm-deploy collision, cert auto-issuance). Read once before executing Phase 2 for the first time.
- [`references/verification.md`](references/verification.md) — post-deploy curl + openssl checklist with failure-mode mapping.
