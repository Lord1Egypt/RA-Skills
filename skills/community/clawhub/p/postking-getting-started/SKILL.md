---
name: postking
description: Router skill for PostKing — confirms the active brand, then hands off to the right specialist skill for posts, blogs, landing pages, SEO, or setup.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking.svg
  category: marketing
---

# PostKing

PostKing is a hosted content platform for social posts, blogs, landing pages, SEO/GEO, marketing campaigns, competitor intelligence, and Reddit community engagement — driven through MCP tool calls (or the `pking` CLI as an optional fast path) across ~140 commands / 200+ tools. This skill is deliberately a thin router: it gets the active brand sorted out, then hands off to whichever specialist skill actually owns the procedure. Don't try to execute social/blog/landing-page flows from here — read the sibling skill instead.

## When to Use

Reach for this skill first on almost any PostKing request — it's the default landing spot before you know which specialist skill applies, and the place to come back to whenever you're unsure which skill owns a task or need to pick/switch the active brand.

## Pick the active brand

Every brand-scoped tool call needs an active brand. Do this before anything else:

1. `list_brands({})` — if there's exactly one brand, it's already active; continue.
2. Multiple brands → ask the user which one, then `set_active_brand({ brandId })`.
3. Zero brands → stop here and use the `postking-getting-started` skill to onboard one before doing anything else.

## Where to go next

| Intent | Use skill |
|---|---|
| Social posts — generate/approve/schedule, content weeks (Smart Week), repurposing to social, post visuals, trend hooks | `postking-social` |
| Blogs — publications, generate/iterate/publish articles (PostKing-hosted or WordPress/Medium/Substack) | `postking-blog` |
| Landing pages — generate, edit/vibe-edit, side pages, custom domains, publish | `postking-landing-pages` |
| SEO / GEO — keyword research through published articles | `postking-seo` |
| Multi-channel marketing campaigns (Storylines: brief → strategy → execute) | `postking-storylines` |
| Competitor discovery, registration & analysis | `postking-competitor-intel` |
| Subreddit pool, content-to-community matching, native Reddit rewrites | `postking-reddit` |
| Applying/listing saved voice profiles, de-slop / AI-detection pass | `postking-brand-voice` |
| First-time auth, credits/billing, brand onboarding from a URL, connecting socials | `postking-getting-started` |

Do not duplicate those skills' procedures here — this skill only routes to them.

Every brand carries a `contentLanguage` (`en`/`es`/`pt-BR`/`de`/`fr`/`cs`; absent means `en`) that generation tools use by default — read it with `get_brand_content_language({ brandId })`, change it with `set_brand_content_language({ brandId, language })`. Most generation tools (`generate_post`, `generate_blog_post`, `generate_landing_page`, `repurpose_content`, and others) also accept a per-call `language` override that beats the brand default for that one call only.

A brand can also publish in more than one language at once — its enabled set (the language roster) is a separate concept from the single `contentLanguage` default above. `get_brand_languages({ brandId })` returns `{ defaultLanguage, languages, maxAllowed }` (plan caps: Trial/Growth 1, Pro 2, Enterprise 5); `add_brand_language({ brandId, language })` enables one (idempotent, settings-only — doesn't generate anything); `remove_brand_language({ brandId, language })` disables one (the default language can't be removed this way, and neither add nor remove touches already-published content). This matters for tools that take an explicit per-resource `languageCode` rather than the per-call `language` override above: `create_publication`'s `languageCode`, for example, is rejected with a 403 if that language isn't already on the roster — call `add_brand_language` first, then retry.

See also: **BrandMind**, PostKing's agentic brand-knowledge assistant in the dashboard, draws on the brand knowledge base reachable via the `knowledge_list` / `knowledge_create` / `knowledge_get` / `knowledge_update` / `knowledge_delete` tools. **Brand Truth** is a separate, more atomic store — durable facts/observations about the brand (hard facts, audience truths, strategy notes, negative space, content insights, topics) that PostKing mines from free-form text and reuses to ground generation: `brand_truth_list` / `brand_truth_get` to browse, `brand_truth_create({ brandId, text })` to submit plain-language prose (an LLM extraction pipeline decides what atomic truths to keep, reports `skipped` with reasons), `brand_truth_update` for a direct field edit (no re-extraction), `brand_truth_delete` to remove one (also records rejection memory so it isn't re-suggested). **Audience / ICP** is the brand's mined audience intelligence: `get_audience({ brandId })` reads the current ICP/persona/positioning; `preview_audience_edit({ brandId, prompt })` is a read-only dry run that discovers which `sections`/`subsections` a change would touch; `edit_audience({ brandId, prompt, sections })` is the async AI edit itself (`sections` required, poll `get_job`). **Social Performance**, the post-performance analytics dashboard, has no MCP tool surface — point the user to the PostKing dashboard for it.

## Verification

After picking a brand, these should always succeed:

- `get_credits({ detail: "short" })` — returns the authenticated user's balance and free-tier status.
- `list_brands({})` — returns at least one brand (active brand marked).

If both succeed, the platform connection is healthy — proceed to the relevant specialist skill above.

## Full command reference

For the complete `pking` CLI surface (every group, every flag), read `references/commands.md` in this skill. The agent should consult it before running an unfamiliar CLI command.
