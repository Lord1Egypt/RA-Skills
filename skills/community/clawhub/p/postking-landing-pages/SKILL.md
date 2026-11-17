---
name: postking-landing-pages
description: Generate, edit, vibe-edit, and publish landing pages on PostKing, including comparison/side pages and custom domains, for launches and campaigns.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-landing-pages.svg
  category: marketing
---

# PostKing Landing Pages

Handles the landing-page lifecycle on PostKing: AI generation, targeted or full AI ("vibe") edits, side pages under a parent page, custom domains, and publishing. Requires an active brand — use the `postking` skill's brand-pick flow first if one isn't set.

## When to Use

Use this skill when the user wants to generate a new landing page, edit or AI-rewrite one, add or edit a side page (a comparison, text, or landing-style sub-page under a parent LP), attach a custom domain, or publish/preview a page.

## When NOT to Use

- Social posts or content weeks → `postking-social`.
- Blog articles → `postking-blog`.
- The SEO/GEO roadmap pipeline that decides *what* pages to brief (seeds → keywords → clusters → roadmap items) → `postking-seo`. This skill covers generating and editing the pages themselves, including side pages fed by a roadmap brief.
- Saved voice profile management or a standalone de-slop pass → `postking-brand-voice`.
- No active brand yet → `postking-getting-started`.

## Minimal tool subset

- `list_landing_pages`, `generate_landing_page`, `view_landing_page`, `get_job` — create and inspect (`get_job` is for the async `generate_landing_page`/`regenerate_landing_page` ops only — vibe-edit sessions are polled with `get_vibe_edit_status`, not `get_job`).
- `edit_landing_page`, `set_landing_page_section`, `set_lp_section_layout`, `regenerate_landing_page`, `vibe_edit_landing_page`, `get_vibe_edit_status`, `apply_vibe_edit`, `restore_lp_version`, `delete_lp_version` — editing.
- `list_lp_versions`, `view_lp_version`, `view_lp_draft` — landing-page version-history reads (`restore_lp_version`/`delete_lp_version` above are the writes) — see "Version history".
- `list_side_pages`, `generate_side_page`, `import_side_page_html`, `view_side_page`, `edit_side_page`, `set_side_page_section`, `set_side_page_state` — side pages.
- `list_block_types`, `add_block`, `edit_block`, `delete_block`, `reorder_blocks` — block-model editing for `sidePageType: "custom"` side pages — see "Custom side pages (block model)".
- `list_side_page_versions`, `view_side_page_version`, `restore_side_page_version`, `delete_side_page_version` — side-page version history — see "Version history".
- `get_landing_page_translations`, `create_landing_page_translation` — landing-page language variants — see "Landing page translations".
- `list_asset_slots`, `assign_asset_to_slot` — discover a page's asset slots and assign/reassign/clear the asset in a slot (works for main LPs and side pages — see "Assign or reassign an asset to a slot").
- `add_domain`, `verify_domain`, `list_domains`, `delete_domain` — custom domains (partial support — see Pitfalls).
- `publish_landing_page`, `delete_landing_page` — publish/lifecycle.

## Procedure

### Generate and publish a landing page

1. `generate_landing_page({ brandId, topic, slug?, language? })` — async; creates the LP record and kicks off AI content generation. `language` (`en`/`es`/`pt-BR`/`de`/`fr`/`cs`) overrides the brand's `contentLanguage` for this page only. Returns `{ slug, operationId, pollUrl }`. Poll with `get_job({ pollUrl: operationId, brandId, wait: true })` until `state` is `completed` (or `failed`/`partially_failed`/`cancelled`).
2. `view_landing_page({ slug })` — preview the generated content.
3. `publish_landing_page({ slug })` — free-tier choke point. Surface the returned `webUrl` to the user.

### Edit a landing page

- Targeted metadata/instructions patch: `edit_landing_page({ slug, title?, instructions? })`.
- Direct field/section write (no AI): `set_landing_page_section({ slug, section, field?, value, replaceSection? })` — each call creates a new draft version. For many related changes across a page, prefer the vibe-edit flow below. `section` is one of the 12 built-ins (`hero`, `showcase`, `videos`, `howItWorks`, `features`, `categoryExplorer`, `replacesStack`, `comparisonMatrix`, `cta`, `faq`, `pricing`, `roiCalculator` — the same list `set_lp_section_layout` orders) or a top-level root (`slotMap`, `config`, `navigation`, `siteMetadata`). Freeform HTML sections are a separate address: `section: "customHtml"` with `field: "<id>"` and `value: { name?, html }` (or `replaceSection: true` to replace the whole `id -> {name?, html}` map) — the HTML is sanitized server-side and rejected (not stripped) if it breaks the `blk-*`-class/no-script rules.
- Reorder or toggle visibility of sections: `set_lp_section_layout({ slug, sectionOrder?, sectionVisibility? })` — `sectionOrder` takes the 12 built-in keys above plus any `customHtml:<id>` freeform sections in the page.
- Full AI regeneration pass, optionally scoped to specific sections: `regenerate_landing_page({ slug, voiceProfileId?, instructions?, sections? })`.
- Natural-language AI edit ("vibe edit") — this is a propose → review → apply flow, nothing changes until you apply it:
  1. `vibe_edit_landing_page({ slug, instructions, scope?, sectionId?, language? })` — `scope` is `"full" | "section"` (`sectionId` required when `scope: "section"`; example section keys: `hero`, `features`, `pricing`, `cta`, `faq`, `howItWorks`, `showcase`, `categoryExplorer`, `replacesStack`, `comparisonMatrix`, `roiCalculator`). `scope: "section"` is **hard-enforced**: any patch keys outside `sectionId` are silently dropped, not applied elsewhere. Use `scope: "full"` for any edit that spans more than one section. `language` regenerates the edited content in that language for this edit only, overriding the brand's configured content language. Returns `{ operationId }`.
  2. Poll `get_vibe_edit_status({ slug, operationId })` — **not `get_job`**, which cannot find vibe-edit sessions — until `status` is `completed` (or `failed`). The default `detail: "medium"` is the review view: `{ status, stale, changes: [{ index, path, before, after }] }`. A structurally impossible request (e.g. asking for a 6th pricing plan when the schema caps at 5) fails fast with a clear error on the status response instead of looping/repairing — read the error and adjust the instructions rather than retrying the same payload.
  3. Review the `changes` array, then `apply_vibe_edit({ slug, operationId, all? | indices? | paths? })` to apply the accepted changes to the draft as one new version. A stale session (draft moved on since the edit was proposed) returns a `stale_session` error — re-run `vibe_edit_landing_page` or retry with `force: true`.
  4. `publish_landing_page({ slug })` to make it live. `restore_lp_version({ slug, versionId })` rolls the draft back if needed.

### Pricing section (`pricing.plans`)

- 1–5 plans max, no more. A request for a 6th plan is structurally impossible and fails fast (see step 2 above).
- Plan objects are **strict** — unknown keys are rejected. Required: `id`, `name`, `price` (number ≥0), `period`, `description`, `features` (array of `{ text, included }`), `cta`. Optional: `isHighlighted`, `nofollow`, `contactSales`, `isComingSoon`, `outputs[]`, `meta`, `metaItems[]`, `valueProp`, `annualPrice`, `billingNote`, `ctaUrl`, `url`, `annualUrl`, `urls{monthly,annual}`.
- Put a plan's checkout/signup link in `url` or `ctaUrl` (or `urls.monthly`/`urls.annual` for cadence-specific links) — don't invent a new key for it; it'll be rejected.

### Assign or reassign an asset to a slot

Images and videos on a page are **not** stored inside section text — they live in a `slotMap` keyed by dotted slot keys (e.g. `hero.backgroundVideo`, `cta.image`, `hero.logoCarousel`, `showcase.video.1`, `pricing.illustration`). Each slot holds one asset ID, or an array of IDs for "array" slots. A main LP's slots are namespaced under a `pageKey` (`main` by default); a side page keeps its **own** separate `slotMap`.

1. Make sure the asset is in the brand library first — `list_assets`, `upload_asset`, or `import_asset_from_url`. `assign_asset_to_slot` only references existing assets; it does not upload.
2. Discover slot keys and their current assignments: `list_asset_slots({ slug, sidePageSlug?, pageKey? })` — pass `sidePageSlug` for a side page. Returns each slot with its media type and current asset.
3. Assign, reassign, or clear the slot: `assign_asset_to_slot({ slug, slotKey, assetId? | assetIds?, sidePageSlug?, pageKey?, clear? })`. Synchronous — applies immediately, no polling.

- **Main landing page:** `assign_asset_to_slot({ slug, slotKey: "hero.backgroundVideo", assetId })`.
- **Side page:** `assign_asset_to_slot({ slug, sidePageSlug, slotKey: "cta.image", assetId })`.
- **Clear a slot:** `assign_asset_to_slot({ slug, slotKey: "hero.logoCarousel", clear: true })`.

Rules:
- Array slots require `assetIds` (plural); single slots require `assetId`. Using the wrong one is rejected.
- The asset must belong to the brand **and** match the slot's media type (IMAGE vs VIDEO), or the call is rejected.
- A main-LP assignment creates a new **draft** version — `publish_landing_page({ slug })` to make it live. Side-page `slotMap` writes apply in place with no version of their own — unlike `set_side_page_section`/`edit_side_page`/the block tools, which do create one (see "Version history").
- A side page carrying its own `slotMap` shadows the parent LP's slots for that page.

### Side pages

1. `list_side_pages({ slug })` — see what already exists under a parent landing page. Each entry includes `previewUrl` (browser-openable draft preview, present whenever the server has a preview domain configured) and `liveUrl` (only when a custom domain is connected) — hand these to the user instead of constructing URLs yourself.
2. `generate_side_page({ slug, key, prompt?, brief?, keywords?, sidePageType?, name? })` — `key` is the required URL-slug fragment for the side page. `sidePageType` is `"landing" | "text" | "comparison" | "custom" | "spotlight"` (defaults to `"landing"`) — there is **no `type` param**, and `"comparison"` requires a persisted `briefId`. `"spotlight"` is the **feature / service spotlight** page: a fixed-schema single-topic page (hero, a 3-6 step feature tour, 3-6 benefits, a stat + quote proof band, CTA footer) with no testimonial carousel, pricing table or showcase — use it whenever the page covers ONE feature or service, instead of `"landing"`, which pulls in the full marketing template. Spotlight is freeform-only: pass `key` + `prompt` (+ optional `name` for the display title, `keywords`); `brief` and `selectedSections` are ignored for it. Async for most cases (returns `operationId`); some comparison briefs run synchronously and return `sidePageId` directly with no `operationId`. Poll `get_job` when an `operationId` is returned; the completed result includes `previewUrl`/`liveUrl` as above.
3. `import_side_page_html({ slug, url? | html?, sidePageSlug?, voiceProfileId?, autoAssignAssets? })` — clone an existing web page as a side page under the parent LP `slug`. Pass `url` (PostKing fetches the page server-side — don't download the HTML yourself; an invalid or SSRF-blocked URL 400s) or `html` directly, not both. `sidePageSlug` is optional with `url` (derived from the URL path), **required** with `html`. Behavior follows the *parent* LP's type: raw-HTML parent → synchronous verbatim import, returns `{ sidePage: { id, slug }, mode: "import", previewUrl?, liveUrl? }`; sectioned parent → the source page's text is extracted and seeds an async side-page generation instead, returns `{ mode: "generate", operationId, key }` — poll with `get_job`, same as `generate_side_page`. 409 = a side page with that slug already exists. Contrast with `import_landing_page_html`, which creates a standalone top-level landing page, not one nested under a parent.
4. `view_side_page({ slug, sideKey })` — inspect content and rendered HTML; also returns `previewUrl`/`liveUrl`.
5. `edit_side_page({ slug, sideKey, name?, newKey?, instructions?, updateReferences? })` — `name` sets the display title, which is what shows up in the parent landing page's auto-generated footer/nav "Solutions" links and in breadcrumbs; changing it updates those automatically. `newKey` renames the side page's URL-slug fragment — the old URL 404s afterward (no redirect), and existing internal references (blog backlinks, internal links) are rewritten in the background; poll the returned `slugRewriteOperationId` for that rewrite. `updateReferences` defaults to `true` and can be set `false` to skip that reference-rewrite cascade when renaming via `newKey`. `instructions` still only records a page-level annotation and does not itself trigger an AI edit. Use `set_side_page_section({ slug, sideKey, sectionId, fields?, field?, value?, instructions? })` for a single structured section edit instead.
6. `set_side_page_state({ slug, sideKey, published })` — publish or unpublish it.

### Custom side pages (block model)

A `sidePageType: "custom"` side page (see `generate_side_page` above) stores content as an ordered `blocks[]` array instead of the fixed section list `"landing"`/`"spotlight"` pages use — reach for it when the page needs a shape the fixed sections can't express. Every block tool addresses a specific side page with **both** the parent LP `slug` and the side page's `sideKey` (from `list_side_pages`) — there is no way to add blocks to a top-level landing page directly, only to a `"custom"`-type side page nested under one.

1. `list_block_types({ brandId?, detail? })` — the entire runtime discovery mechanism for what `add_block` accepts: Tier 1 (the 12 built-in Uland sections — `hero`, `showcase`, `videos`, `howItWorks`, `features`, `categoryExplorer`, `replacesStack`, `comparisonMatrix`, `cta`, `faq`, `pricing`, `roiCalculator`) merged with Tier 2 (brand-visible `BlockType` rows seeded in the DB). `detail: "full"` returns each type's complete `jsonSchema` (and `template` for Tier 2) — call it before every `add_block`/`edit_block` to see exactly what shape `props` must have, rather than assuming a fixed catalog; a new Tier 2 type is usable immediately with no server rebuild. Tier 3 (`type: "html"`) is always available and is not listed here.
2. `add_block({ slug, sideKey, type, props, position? })` — `type` is a key from `list_block_types` or the literal `"html"`. `props` must match that type's schema exactly (a mismatch is rejected, not coerced, and the error names the offending field); for `"html"` it's `{ html: "<section class=\"blk-section\">...</section>" }`, sanitized server-side against a `blk-*` class/tag allowlist (no `<script>`/`<style>`/`<img>`/inline standard CSS) and REJECTED with a reason on violation, never silently stripped. `position` is a 0-based insert index into the current array; omit to append. The server generates and returns the new block's id (`blk_xxxxxxxx`).
3. `edit_block({ slug, sideKey, blockId, type?, props? })` — `props` replaces the block's ENTIRE props object, not a shallow merge; fetch current props first via `view_side_page({ slug, sideKey, detail: "full" })` (under `overrides.blocks`) if you're only changing one field, merge locally, then send the full object back. Passing `type` also revalidates `props` against the new type's schema — pass matching `props` in the same call.
4. `delete_block({ slug, sideKey, blockId, confirm: true })` — removes one block; recoverable via `list_side_page_versions`/`restore_side_page_version` even after deletion, since version history is append-only.
5. `reorder_blocks({ slug, sideKey, blockIds })` — `blockIds` must be the full, exact set of the page's current block ids in the new order; it cannot add or remove blocks (use `add_block`/`delete_block` for that), and a set mismatch is rejected.

All four writes create a new draft version (draft-only until `set_side_page_state({ published: true })`) and are fenced by optimistic concurrency: a 409 means another write landed between your last read and this call — call `view_side_page` again to re-fetch current blocks and retry against the fresh state, don't blindly resend the same call.

### Version history

Every content write to a landing page (`set_landing_page_section`, `apply_vibe_edit`, `regenerate_landing_page`, a main-LP `assign_asset_to_slot`) or to a side page (`set_side_page_section`, `edit_side_page`, the block tools above) creates a new **draft** version — publishing is always a separate step (`publish_landing_page` / `set_side_page_state({ published: true })`). The one exception is `assign_asset_to_slot` targeting a side page's `slotMap`, which writes in place with no version of its own.

- Landing page: `list_lp_versions({ slug })` — history, each entry with a `previewUrl`. `view_lp_version({ slug, versionId })` — inspect one version's section content. `view_lp_draft({ slug })` — the current unpublished draft. `restore_lp_version({ slug, versionId })` — roll the draft back to a prior version (does not touch the published version). `delete_lp_version({ slug, versionId, confirm: true })` — permanently remove a historical version; the published version and the last remaining version can't be deleted.
- Side page: `list_side_page_versions({ slug, sideKey })` — history; the response's top-level `currentVersionId` (draft) and `publishedVersionId` (live) tell you draft vs. live without a second call. `view_side_page_version({ slug, sideKey, versionId })` — inspect a snapshot (`{ type, overrides, siteMetadata, slotMap, config }`). `restore_side_page_version({ slug, sideKey, versionId })` — moves the draft forward to a new version copied from the target (forward history is never deleted); the live page is unaffected until you `set_side_page_state({ published: true })` again. `delete_side_page_version({ slug, sideKey, versionId, confirm: true })` — deleting the current draft version is allowed and repoints the draft to the newest remaining version; the published version and the last remaining version can't be deleted.

### Landing page translations

A landing page can have language variants linked into a shared translation group — one page row per language, distinct from the brand's default `contentLanguage`. The target language must already be enabled for the brand (`get_brand_languages`/`add_brand_language`, in the `postking` skill) or `create_landing_page_translation` is rejected with a language-not-enabled error.

1. `get_landing_page_translations({ slug })` — read the translation group `slug` belongs to: `{ slug, languageCode, pathPrefix, translationGroupId, isTranslationSource, variants: [...] }`. `variants` lists the OTHER language variants already in the group (empty if none yet). Call this before `create_landing_page_translation` to check whether a variant in the target language already exists.
2. `create_landing_page_translation({ slug, language })` — `slug` must be the group's actual source page: fails with 400 if `slug` is itself already a translation (chain new variants off the source, never off another variant), and 409 if a variant in that language already exists in the group. Creates a new DRAFT page row (correct slug suffix and `/{languageCode}` path prefix) and kicks off an async job that pulls and translates the source page's current content; the response's `operationId` is pollable with `get_job`, and `pullFromSourceUrl` is a documented manual fallback (an AI-edit pull-from-source call) if you need to re-trigger the pull yourself.

### Custom domain (partial support)

1. `add_domain({ domain, primaryContentType: "landing_page", brandId? })` — registers the domain and returns a DNS TXT record to add at the registrar.
2. `verify_domain({ domainId })` — checks DNS once the record is added; `domainId` comes from the `add_domain` response or `list_domains`.
3. **There is currently no MCP or CLI tool to connect a verified domain to a specific landing page.** `connect_domain_to_publication` only attaches a domain to a *blog* publication (it takes a `publicationId`, not a landing-page slug) — using it for a landing page is a no-op/wrong target, not a substitute. Tell the user to finish the connection from the landing page's own settings in the PostKing dashboard.
4. `delete_domain({ domainId })` — removes a custom domain; connected blogs and landing pages are unlinked but not deleted.

## CLI fast path

| Goal | Command |
|---|---|
| List / generate | `pking lp list` / `pking lp generate --topic "..." [--slug <slug>] [--voice <id>]` |
| View / preview | `pking lp view <slug>` |
| Edit (metadata or AI pass) | `pking lp edit <slug> [--title "..."] [--instructions "..."]` |
| Vibe edit | `pking lp vibe <slug> --instructions "..." [--scope full\|section --section-id <id>] --wait` then `pking lp vibe status <slug> <operationId>` |
| Side pages | `pking lp side list <slug>` / `pking lp side edit <slug> <sideKey> --instructions "..."` — generation is currently MCP-only, see Pitfalls |
| Side page section | `pking lp side section <slug> <sideKey> --id <sectionId> [--content "..." | --file <path>] [--instructions "..."]` |
| Publish / unpublish a side page | `pking lp side state <slug> <sideKey> --publish` (or `--unpublish`) |
| Custom domain (register + verify only) | `pking domains add <domain>` → `pking domains verify <domain>` |
| Publish the landing page | `pking lp publish <slug>` |

For the full command catalog, use the `postking` skill's `references/commands.md`, or run `pking lp --help`.

## Pitfalls

- **`generate_side_page` has no `type` param** — it's `sidePageType`, and the only valid values are `"landing"`, `"text"`, `"comparison"`, `"custom"`, `"spotlight"`. Don't invent other values (e.g. "pricing", "features", "legal") as `sidePageType` — those aren't recognized side-page types by this tool. A feature page is `"spotlight"`, not a made-up `"features"` value.
- **`key` is required on `generate_side_page`** — it's the side page's URL-slug fragment, not optional metadata.
- **`pking lp side generate <slug> --type <type>` is currently broken** — the inner route ignores the `<slug>` path param and requires `name`/`slug`/`landingPageId` in the request body, so it always 400s. Use the MCP tool `generate_side_page({ slug, key, sidePageType })` instead.
- **Custom domains for landing pages stop short of dashboard-only.** Registering (`add_domain`) and verifying (`verify_domain`) work via MCP/CLI, but attaching the verified domain to a specific landing page does not — don't tell the user `connect_domain_to_publication` will do it; that tool is blog-only.
- **`pking domains connect <id> --target lp:<slug>` is not a working command** — the CLI accepts the flag but the endpoint it calls does not exist on the server; don't suggest it.
- **Async operations can take 30s–5min.** Poll `get_job` (or the CLI's built-in `--wait`) rather than assuming failure early.
- **Comparison-type side pages may return synchronously** with `sidePageId` and no `operationId` — don't poll `get_job` with an ID you don't have; check the immediate response first.
- **Side-page content writes DO have version history and a draft/publish split**, the same shape as the main LP: `set_side_page_section`, `edit_side_page`, and the block tools (`add_block`/`edit_block`/`delete_block`/`reorder_blocks`) each create a new draft version, and `set_side_page_state({ published: true })` is the side-page equivalent of `publish_landing_page` — see "Version history". The one exception is `assign_asset_to_slot` targeting a side page's `slotMap`, which still writes in place with no version of its own — double-check slot assignments before writing.
- **Renaming a side page's title or key is MCP-only** (`edit_side_page({ name, newKey })`) — there is no `pking` CLI flag for it yet; `pking lp side edit` only supports `--instructions`.
- **A missing `previewUrl` or `liveUrl` is not an error.** No `liveUrl` just means no custom domain is connected yet; no `previewUrl` means the server has no preview domain configured. Don't retry or report failure — just skip handing that link over.
- **`newKey` changes the live URL with no redirect** — the old URL 404s immediately. Warn the user before renaming a published side page, and mention that internal references are fixed up asynchronously (poll `slugRewriteOperationId`), not instantly.

## Verification

- `get_credits({ detail: "short" })` — confirms auth and balance.
- `list_landing_pages({})` — returns the brand's landing pages (or an empty list if none created yet, which is expected pre-setup).
