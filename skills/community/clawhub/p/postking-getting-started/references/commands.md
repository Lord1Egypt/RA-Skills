# `pking` command reference

Full command tree for `postking-cli` v1.0.3+. Run `pking <group> --help` for canonical flag documentation.

Conventions:
- Items in `<angle>` are required positional arguments.
- Items in `[brackets]` are optional.
- Flags ending in `...` accept multiple values.

### `webUrl` on responses

Most artifact-producing commands print a `View in browser: <url>` line on
success. The underlying API returns a `webUrl` field — the dashboard page
where the user can review the artifact (post detail page, blog edit
page, landing-page review page). Surface this URL to the user verbatim
whenever you confirm an action like "post created", "post scheduled",
"post published", "blog generated", "landing page updated", or "visual
picked". The user is assumed to be already logged in to the dashboard in
their browser.

Commands that include `webUrl`: `pking posts create / approve /
reschedule`, `pking visuals pick`, `pking blogs generate / publish`,
`pking lp generate / update / publish`.

---

## Auth

```
pking login                                Device-code OAuth flow (blocks; polls server).
pking login-start                          Print URL+code, save device_code, exit.
pking login-finish                         Finish a login-start session (exits 2 if pending).
pking logout                               Clear local credentials.
pking register --email <e> --password <p> [--client-name <n>]
                                           Create a new PostKing account.
pking register-start --email <email> [--client-name <n>]
                                           Non-blocking device/magic-link
                                           registration: sends the magic-link
                                           email, saves the device_code
                                           locally, exits immediately. Use
                                           from agent skills instead of a
                                           blocking flow.
pking register-finish                      Finish a pending register-start
                                           session. Calls the token endpoint
                                           ONCE; exits 2 if the user hasn't
                                           clicked the magic link yet — retry
                                           after they confirm.
pking login-password --email <e> --password <p> [--client-name <n>]
                                           Password login (legacy).
pking me                                   Show authenticated user, scope, credits, brands.
pking user credits                         Show plan + remaining credits.
```

## Billing

```
pking billing packs                        List available one-off credit
                                           packs with pricing.
pking billing topup --pack <sku> [--json]
                                           Purchase a credit pack and poll
                                           for payment confirmation.
                                           --pack is required, e.g. agent_4 |
                                           agent_5 | agent_25 | agent_50.
pking billing wallet [--json]              Show current agent credit balance
                                           and recent transactions.
pking billing tiers                        List subscription tiers with
                                           pricing and monthly credit
                                           allowances.
pking billing subscribe --tier <TIER> [--interval month|year] [--json]
                                           Start a subscription checkout and
                                           poll for activation confirmation.
                                           --tier is required: GROWTH | PRO |
                                           ENTERPRISE. --interval defaults to
                                           month.
```

## Brand

```
pking brand list                           List brands; active is starred.
pking brand info                           Show active brand details.
pking brand create <name> [--description <d>] [--website <url>] [--tone <t>] [--audience <a>] [--brand-type <personal|business>] [--skip-finalize] [--json]
                                           Create a brand manually (no website crawl).
                                           Automatically chains POST /api/brands/{brandId}/finalize
                                           after creation, which generates the audience profile
                                           + initial themes for manual brands — mirrors the web
                                           flow. Pass --skip-finalize to create the brand row
                                           only (testing/debug; leaves audience-review empty).
                                           Polling: 'pking jobs list' or 'pking brand info'.
pking brand delete <brandId> --destructive [--confirm <brandName>] [--json]
                                           Delete a brand workspace (owner only; soft-delete).
                                           --destructive is required. After it, you must
                                           type the exact brand name when prompted to proceed.
                                           In non-interactive mode (--json), pass
                                           --confirm <brandName> to skip the prompt; mismatched
                                           or missing --confirm aborts with exit 1.
pking brand set <brandId>                  Switch active brand.
pking onboard <websiteUrl> [--name <n>] [--description <d>] [--tone <t>] [--audience <a>] [--brand-type <personal|business>]
                                           Top-level. Crawl site, analyze audience,
                                           generate 10 themes. Async. All description/tone/
                                           audience/brandType flags are passed through to the
                                           agent onboard route (mirrors the inner /api/brands
                                           POST body) so an agent can seed the brand profile
                                           in a single call.
pking brand generate-themes [--count <n>] [--instructions <t>] [--input <path_or_text>]
                                           Regenerate themes for active brand.

pking brand mix [brandId] [--json] [--set <json>]
                                           Review/confirm the brand's content intent mix
                                           (educate/connect/present/intrigue, sum = 100).
                                           Runs after the audience-review step in the
                                           brand-setup flow. With no flags, prints the
                                           current mix and prompts: accept | edit | reject.
                                             --json   Print the fetched mix as JSON and exit
                                                      (no prompt).
                                             --set    Non-interactive override. Pass a JSON
                                                      object (single line), e.g.
                                                      --set '{"intentMix":{"educate":30,"connect":20,"present":35,"intrigue":15}}'
                                           Wraps GET/PATCH /api/agent/v1/brands/{brandId}/content-mix.
                                           Next step after this: pking brand themes.

pking brand themes list                    List content themes.
pking brand themes edit <themeId> [--title <t>] [--content <t>]
pking brand themes delete <themeId>        Delete a theme.

pking brand mediums [brandId] [--json] [--set <csv>]
                                           Pick the social/content channels (mediums)
                                           the brand wants to grow on. Stored at
                                           brandSettings.selectedMediums; consumed by
                                           the smart-week engine and the weekly
                                           scheduler. With no flags, prints the
                                           current selection and prompts for a
                                           comma-separated list (press Enter to keep
                                           current).
                                             --json   Print the fetched payload as JSON and exit.
                                             --set    Non-interactive override. Comma-separated, e.g.
                                                      --set 'linkedin,x/twitter,instagram,blog'
                                           Supported mediums: instagram, facebook, x/twitter,
                                           linkedin, threads, pinterest, youtube, blog, newsletter,
                                           reddit, landing-pages, seo. Smart-week generation is
                                           limited to instagram/facebook/x/twitter/linkedin/threads/blog.
                                           Wraps GET/PATCH /api/agent/v1/brands/{brandId}/mediums.
                                           Next step after this: pking brand smart-week.

pking brand smart-week [brandId] [--yes] [--json]
                                           Generate a full Mon–Fri week of posts across
                                           the brand's selected mediums. Asks for explicit
                                           consent first ("Generate now? [y/N]") and prints
                                           an estimate of post count + runtime before
                                           kickoff. The CLI/agent flow never auto-triggers
                                           smart-week — the web onboarding flow does, but
                                           agent v1 onboarding does not.
                                             --yes    Skip the consent prompt (required for
                                                      non-interactive runs like Hermes/OpenClaw).
                                             --json   Emit the raw kickoff payload
                                                      ({ sessionId, totalPosts, operationId, ... }).
                                           Wraps POST /api/agent/v1/brands/{brandId}/posts/smart-week.
                                           Generation runs in the background; track with
                                           'pking jobs list' or 'pking posts list'.

pking brand visual set [brandId] [--logo <assetId>] [--symbol-light <assetId>] [--symbol-dark <assetId>] [--primary-color <hex>] [--secondary-color <hex>] [--accent-color <hex>] [--primary-font <n>] [--secondary-font <n>] [--json]
                                           Configure visual identity (logo, colors, fonts).
                                           Mirrors the web Visual Identity onboarding step
                                           in components/dashboard/onboarding/VisualIdentitySetup.tsx.
                                           Every value is a flag — headless, no prompts.
                                           --logo, --symbol-light, --symbol-dark accept
                                           asset IDs returned by 'pking brand visual
                                           import-assets' (or listed by 'pking visuals list').
                                           Raw URLs are NOT accepted — import them first.
                                           Writes brandSettings.logo.{fullLogoLight,
                                           symbolLogoLight, symbolLogoDark}.
                                           --primary-color etc. accept 3- or 6-char hex
                                           (e.g. #FF6B35). At least one flag is required.
                                           Wraps PATCH /api/agent/v1/brands/{brandId} with
                                           a deep-merged brandSettings payload.

pking brand visual import-assets [brandId] [--urls <csv> | --from-file <path>] [--json]
                                           Batch-import up to 50 image URLs into the brand
                                           asset library. Mirrors the importCrawledAssets
                                           call the web onboarding makes when finishing
                                           Visual Identity. Pass URLs inline via --urls
                                           (comma-separated) or from a file containing one
                                           URL per line (or a JSON array). Headless.
                                           Wraps POST /api/agent/v1/brands/{brandId}/assets/import-urls.

pking brand finalize [brandId] [--json]
                                           Mark the brand fully onboarded by setting
                                           brandSettings.isOnboarded = true. Mirrors the
                                           final settings PATCH the web flow issues at the
                                           end of Visual Identity. Triggers the one-time
                                           "onboarding complete" notification. Run this
                                           last in the chain:
                                             onboard -> mediums -> mix -> themes -> voice
                                             -> visual -> smart-week -> finalize
                                           Wraps POST /api/agent/v1/brands/{brandId}/finalize
                                           (thin wrapper over PATCH /api/brands/{brandId}/settings).

pking brand crawl-profile [brandId] --platform <x|linkedin|threads> --handle <id> [--profile-type <personal|brand|mix>] [--tone-consent] [--json]
                                           Queue the "best profile" crawl for a brand.
                                           Mirrors the web onboarding BestProfileStep —
                                           captures a public handle/URL on x/linkedin/threads,
                                           normalises it server-side, and runs a §2.2-compliant
                                           crawl (Facebook excluded). --tone-consent opts in
                                           to using the crawled posts to shape voice/tone, not
                                           just topics. --handle accepts @handle or a full URL.
                                           Per-brand 5-minute cooldown applies (returns 429).
                                           Wraps POST /api/agent/v1/brands/{brandId}/crawl-profile.

pking brand audience edit [brandId] --instructions <text> [--sections <csv>] [--subsections <spec>] [--wait] [--timeout <seconds>] [--json]
                                           AI vibe-edit the brand's audience-review profile.
                                           Mirrors the web audience-review page. If --sections
                                           is omitted, the CLI first calls the preprompt
                                           analyzer to auto-pick which sections / subsections
                                           the instructions should touch (same behaviour the
                                           web flow uses before the heavy ai-edit).
                                           --subsections format: 'section:sub1,sub2|section2:sub3'.
                                           Async — returns an operationId. Pass --wait to block
                                           until completion (default 180s, override with
                                           --timeout). Poll endpoint:
                                             GET /api/agent/v1/brands/{brandId}/operations/{operationId}
                                           Wraps POST /api/agent/v1/brands/{brandId}/audience-review/ai-edit.

pking brand audience preprompt [brandId] --instructions <text> [--json]
                                           Run only the preprompt analyzer. Returns which
                                           audience sections / subsections a free-text edit
                                           prompt would touch — useful for previewing the
                                           target set before kicking off the heavy ai-edit.
                                           Synchronous (no operationId).
                                           Wraps POST /api/agent/v1/brands/{brandId}/audience-review/ai-edit/preprompt.
```

## Posts

```
pking posts list [--status <s>] [--platform <p>] [--limit <n>]
pking posts view <postId>
pking posts generate --platform <p> [--theme <t>] [--variations <n>] [--voice <id>]
pking posts generate-bulk --platform <p> [--voice <id>] [--frequency <f>] [--posts-per-day <n>] [--times <csv>] [--days <n>]
                                           Generate + schedule across a date range. frequency:
                                           daily|every_other|every_third|weekdays.
pking posts create --platform <p> --content "<text>" [--schedule <iso>]
pking posts approve <postId> [--variation <n>] [--schedule <iso>] [--timezone <tz>]
pking posts schedule <postId> --date <iso> [--variation <n>] [--timezone <tz>]
pking posts calendar [--days <n>]          Upcoming scheduled posts.
pking posts cancel <postId>
pking posts reschedule <postId> --date <iso>
pking posts delete <postId>
```

## Repurpose

```
pking repurpose --source-type <url|text|blog|social_post> --target-type <social|blog|text>
                [--source-url <url> | --source-content <text> | --source-blog <id> | --source-post <id>]
                [--target-platforms <csv>] [--variations <n>] [--angle <text>]
                [--specific-goal <text>] [--text-length <short|medium|long|custom:<words>>]
                [--voice <id_or_x:id,linkedin:id>] [--theme-id <id>] [--include-link]
                                           Turn a URL, text, blog, or post into
                                           platform-tailored content. No positional arg.
```

## Voice

```
pking voice list [--platform <p>] [--filter <shallow|deep>]
                                           List public voice profiles. Returns
                                           id, display name, supported
                                           platforms, and a description
                                           (social proof + tone). Use
                                           --platform (x, linkedin, threads,
                                           blog, lp) to narrow to voices
                                           trained on that medium.
pking voice rewrite --profile_id <id> --text <t> [--platform <p>]
                                           Rewrite text in a specific voice profile.

pking voice brand list [brandId] [--include-public] [--json]
                                           List voice profiles attached to a brand.
                                           By default shows brand-owned profiles only;
                                           --include-public also shows public catalog
                                           profiles available to the brand.
                                           Wraps GET /api/agent/v1/brands/{brandId}/voice-profiles.

pking voice brand update <voiceProfileId> [--brand <id>] [--name <t>] [--active | --inactive] [--adapter <modalAdapterId>] [--json]
                                           Update a brand-owned voice profile.
                                           --adapter sets the Modal LoRA id and promotes
                                           the profile to deep voice. At least one of
                                           --name, --active, --inactive, --adapter required.
                                           Wraps PATCH /api/agent/v1/brands/{brandId}/voice-profiles/{voiceProfileId}.

pking voice brand delete <voiceProfileId> [--brand <id>] --destructive [--json]
                                           Delete a brand-owned voice profile. --destructive
                                           is required to confirm.
                                           Wraps DELETE /api/agent/v1/brands/{brandId}/voice-profiles/{voiceProfileId}.

Voice profile CREATION (extracting tone from X / LinkedIn / Threads / URLs)
runs through async extract endpoints and is currently web-only — direct
users to /dashboard/brands/{brandId}/voice-profiles to add a new profile.
The CLI surface above covers list / update / delete, which is what an agent
needs for parity with the rest of the onboarding chain.
```

## Trends

PostKing crawls top-performing posts every 3 days for three niches —
`ai-saas`, `marketing`, `web3` — and deconstructs each one (hook, template,
pattern, virality reason). Use this as inspiration / writing prompts.
Currently only X is supported; more platforms coming.

```
pking trends list [--niche <ai-saas|marketing|web3>] [--platform <x>]
                  [--days <n>] [--limit <n>] [--sort <engagement|recent>]
                  [--json]
                                           Defaults: niche=ai-saas,
                                           platform=x, days=3 (the freshest
                                           crawl batch), limit=20,
                                           sort=engagement.
```

`--json` returns the full payload including the deconstruction object
(`hook`, `template`, `pattern`, `viralityReason`, `topic`) — feed that
into `pking posts generate` or `pking repurpose` as inspiration.

## Social

```
pking social check                         List connected social accounts.
pking social connect                       Generate generic OAuth magic link.
pking social connect-platform --platform <linkedin|x|instagram|threads|facebook>
                                           Magic link pre-targeted to a platform.
pking social disconnect <platform_or_id>
```

## Weekly schedule

```
pking weekly-schedule get
pking weekly-schedule set [--monday <spec>] [--tuesday <spec>] ... [--sunday <spec>]
                          [--timezone <tz>] [--lead-time <days>] [--voice <id>]
                          [--enable] [--disable]
                                           spec: "linkedin:1,x:1". Empty string clears a day.
pking weekly-schedule enable
pking weekly-schedule disable
pking weekly-schedule delete
pking weekly-schedule run-day --date <YYYY-MM-DD>
                                           Generate posts for a single date.
```

## Editor utilities

```
pking editor rewrite --text <t> [--voice <id>] [--platform <p>]
pking editor humanize --text <t> [--platform <p>]
pking editor detect --text <t>             AI-detection score.
```

## Blogs

```
pking blogs list [--status <s>]
pking blogs view <articleId>
pking blogs create --title "..." [--description "..."]
                                           Create a publication (NOT an article).
pking blogs generate --publication <id> --topic "..." [--voice <id>]
                                           [--length <short|medium|long>] [--keywords <csv>]
                                           [--wait] [--timeout <sec>]
                                           Async draft generation.
pking blogs status <articleId>             Poll a generation job.
pking blogs publish <articleId> [--connections <csv>]
pking blogs delete <articleId>

pking publications list
pking publications create --title "..." [--description "..."]

pking authors list
pking authors create --first-name <n> --last-name <n> [--email <e>]

pking categories list --publication <id>
pking categories create --publication <id> --name "..." --slug <s> [--description "..."]
```

## Jobs

```
pking jobs list [--status <s>] [--limit <n>]
                                           All async background jobs.
```

## Domains

```
pking domains list
pking domains add <domain>
pking domains verify <domain>
pking domains delete <id>
pking domains connect <id> --target <lp:<slug>|publication:<id>>
                                           Attach a verified domain.
```

## SEO / GEO pipeline

```
pking seo seeds <kw1> <kw2> ... [--brand <id>]
                                           Register seed keywords.
pking seo generate [--brand <id>] [--count <n>]
                                           Expand seeds → ~100 keywords. Async.
pking seo keywords [--brand <id>] [--limit <n>]
                                           List generated keywords.
pking seo categorize [--brand <id>]        Tag intent (informational, commercial,
                                           navigational, transactional).
pking seo keywords edit <keywordId> [--intent <i>] [--tags <csv>] [--priority <0..1>] [--exclude-from-clustering] [--brand <id>]
                                           Housekeeping. Edit a single keyword:
                                           override intent label, replace user
                                           tags, nudge priority, or hold the
                                           keyword out of the next clustering
                                           pass. MCP: seo_edit_keyword.
pking seo keywords delete <keywordId> --destructive [--brand <id>]
                                           Housekeeping. Soft-delete a single
                                           keyword (sets deletedAt — the row
                                           stays but is filtered out of all
                                           queries). MCP: seo_delete_keyword.
pking seo cluster [--brand <id>]           Group keywords into topic pillars.
pking seo clusters list [--brand <id>]     Show clusters.
pking seo clusters approve <id> [--brand <id>] [--no-wait] [--json]
                                           Approve a SINGLE cluster — gates
                                           brief generation. Also fires an
                                           async seo_brief_generate Operation
                                           for that cluster.
pking seo clusters reject <id> [--brand <id>] [--json]
                                           Reject a SINGLE cluster (detaches
                                           its scored keywords).
pking seo clusters bulk-approve <ids...> [--brand <id>] [--wait] [--json]
                                           Approve multiple clusters in one
                                           call and trigger brief generation
                                           for each. Async.
pking seo clusters bulk-reject <ids...> [--brand <id>] [--json]
                                           Reject multiple clusters in one
                                           call.
pking seo clusters unapprove <id> [--brand <id>] [--json]
                                           Revert an approved cluster to
                                           pending_review. Fails (409) if
                                           briefs already exist for it.
pking seo clusters restore <id> [--brand <id>] [--json]
                                           Restore a rejected cluster to
                                           pending_review.
pking seo roadmap [--cluster <id>] [--limit <n>] [--brand <id>]
                                           List items, or generate topics
                                           from a cluster.
pking seo roadmap view <id> [--brand <id>]
pking seo roadmap edit <id> [--action <action>] [--status <status>] [--brand <id>]
                                           Update a roadmap item's action or
                                           status only — there is NO
                                           --title/--priority flag.
                                             --action  ignore|restore|start|complete
                                             --status  suggested|ignored|in_progress|completed
pking seo roadmap delete <id> --destructive
pking seo briefs list [--status <csv>] [--type <csv>] [--cluster <id>] [--limit <n>] [--brand <id>]
                                           List SeoBriefs (the H2/FAQ
                                           outline produced after roadmap).
pking seo briefs view <briefId> [--brand <id>]
                                           Inspect a single brief's
                                           briefData outline.

Brief content editing is MCP/dashboard-only — there is no `pking seo
briefs edit` command (briefData is a structured H2/FAQ outline, not a
freeform field a CLI flag can safely patch).

pking seo briefs approve <briefId> [--brand <id>] [--hero-image] [--voice <id>] [--no-wait] [--json]
                                           Approve a SINGLE brief and trigger
                                           article generation (L4). Async —
                                           unlocks `pking seo write`.
pking seo briefs reject <briefId> [--brand <id>] [--json]
                                           Reject a single brief.
pking seo briefs bulk-approve <ids...> [--brand <id>] [--hero-image] [--wait] [--json]
                                           Approve multiple briefs in one
                                           call and trigger article
                                           generation for each. Async.
                                           (There is no briefs bulk-reject —
                                           reject one at a time.)
pking seo briefs regenerate <briefId> [--brand <id>] [--no-wait] [--json]
                                           Re-run L3 for one brief. Async —
                                           returns operationId.
pking seo write <roadmapItemId> [--brand <id>] [--hero-image] [--voice <id>] [--no-wait] [--json]
                                           Draft the article for a roadmap
                                           item whose brief is approved.
                                           Positional roadmapItemId — there is
                                           no --roadmap-id flag and no --count;
                                           this generates a single article.
                                           Async — returns operationId; polls
                                           to completion unless --no-wait.
pking seo gap [--brand <id>]               Gap analysis.
pking seo competitor --domain <domain> [--brand <id>]
                                           Competitor diff.
pking seo publish --article-id <id> [--publication <id>] [--schedule <iso>] [--brand <id>]
pking seo stats [--brand <id>]             Roadmap progress.

CTA auto-assignment is MCP/dashboard-only — there is no `pking blogs
auto-assign-cta` command. Use the `seo_auto_assign_cta` MCP tool instead.

`pking lp side generate <slug> --type <type>` is currently BROKEN — the
inner route ignores the `<slug>` path param and requires
`name`/`slug`/`landingPageId` in the body, so it always returns 400. Use
the MCP tool `generate_side_page({ slug, key, sidePageType })` instead
(`sidePageType` is `landing`|`text`|`comparison`).
```

## Landing pages

```
pking lp list
pking lp view <slug>
pking lp generate --topic "..." [--slug <s>] [--voice <id>]
                                           Async; returns slug + operationId.
pking lp edit <slug> [--title <t>] [--instructions <text>]
                                           AI edit pass or manual title.
pking lp publish <slug>
pking lp delete <slug> --destructive       --destructive is required to confirm.
pking lp regenerate <slug> [--voice <id>] [--instructions <t>] [--section <id>]
pking lp draft view <slug>                 Preview pending changes.
pking lp versions list <slug>
pking lp versions view <slug> <versionId>

pking lp vibe <slug> --instructions "..." [--scope <full|section>] [--section-id <id>] [--wait]
                                           Vibe-edit. Slug is positional.
pking lp vibe status <slug> <operationId>  Poll a vibe edit.

pking lp set <slug> [--title <t>] [--file <path>] [--metadata-file <path>]
                                           Manually set content/metadata (no AI).
```

### Side pages

```
pking lp side list <slug>
```

`pking lp side generate <slug> --type <type>` is currently BROKEN — the
inner route ignores the `<slug>` path param and requires
`name`/`slug`/`landingPageId` in the body, so it always returns 400. Use
the MCP tool `generate_side_page({ slug, key, sidePageType })` instead
(`sidePageType` is `landing`|`text`|`comparison`).

```
pking lp side view <slug> <sideKey>
pking lp side edit <slug> <sideKey> [--instructions <text>]
pking lp side delete <slug> <sideKey> --destructive
pking lp side section <slug> <sideKey> --id <sectionId>
                                           [--content <text> | --file <path> | --instructions <text>]
pking lp side state <slug> <sideKey> [--publish | --unpublish]
pking lp side status <slug> <operationId>  Poll an async side-page op.
```

## Visuals — asset library

All library commands operate on the active brand. `upload` requires `--file
<path>`; `import-url` and `search-stock` take their target as a positional
arg (NOT a `--url` / `--query` flag).

```
pking visuals list [--type <image|video|document|link|lottie>] [--tags <csv>] [--search <q>] [--limit <n>]
pking visuals view <assetId>
pking visuals upload --file <path> [--name <n>] [--description <d>] [--tags <csv>]
pking visuals import-url <url> [--name <n>] [--tags <csv>]
pking visuals import-csv <file>            Bulk import (≤50 URLs; one per line or JSON array).
pking visuals tag <assetId> [--add <csv>] [--remove <csv>]
pking visuals delete <assetId>
pking visuals tags                         List all tags in use.
pking visuals suggest --context "<text>" [--limit <n>]
                                           AI-pick library assets for a caption.
pking visuals search-stock <query> [--platform <p>]
                                           Stock photo/video search (Unsplash + Pexels).
```

## Visuals — on a post

The post-scoped commands live under the SAME `visuals` namespace (NOT
`visuals-post`). `options` already returns library matches + card templates +
quote templates + stock results in one call — you do NOT need to upload an
asset first to get a carousel.

```
pking visuals options <postId> [--platform <p>] [--category <smart|card|quote|photo|video>]
                                           Numbered list of every candidate
                                           (library, cards, quotes, stock).
                                           Marks the recommended pick with ★.
                                           Caches index→pickArgs at
                                           ~/.postking/cache/visuals-<postId>-<platform>.json
                                           so the next `pick --pick <N>` works.
pking visuals regenerate <postId> [--load-external] [--platform <p>]
pking visuals pick <postId> --platform <p> --pick <N>
                                           Recommended path. N is the index
                                           printed by the most recent `options`
                                           call (cached for 24h).
pking visuals pick <postId> --platform <p> [--style <s> --variant <n> | --asset <id> | --slot <key>]
                                           Power-user override — explicit flags
                                           beat --pick when both are given.
pking visuals clear <postId> --platform <p>
pking visuals cards list <postId>
pking visuals cards edit <postId> --card <n> [--title <t>] [--body <t>] [--number <t>] [--rerender]
pking visuals cards set  <postId> --file <cards.json> [--rerender]
pking visuals carousel <postId> [--style <s>] [--variant <n>] [--title <t>]
                                           Render a multi-slide PDF from the post's cards.
```

### Recipe — "pick a visual for this post"

`options` is the discovery surface. It prints a `► Recommended` block, then
numbered sections (Library matches, Cards, Quotes, Stock photos, Stock
videos) with each row showing the rendered card text and an OSC-8
hyperlinked preview URL.

For card and quote templates, each row also prints the **resolved render
params** — the colors, avatar, fonts, and quote text that would actually
be drawn. Read these back to the user when they ask "what would this look
like" — you don't need to render a preview; the params ARE the spec.

The footer of every `options` call includes:

- A `Load more stock photos/videos: pking visuals regenerate <postId> --load-external` line — that's the canonical "show me more" path (no separate `--more` flag).
- A `To change brand colors or default avatar: <settingsUrl>` line — colors and avatar are NOT overridable per-pick. If the user wants different colors or a different avatar, they have to update brand settings in the dashboard at the URL printed there. Surface it verbatim.

```
pking visuals options <postId> --platform linkedin
# → user sees [1]…[N] with resolved colors/avatar/font under each template,
#   plus footer hints for "load more" and "change brand colors"
pking visuals pick <postId> --platform linkedin --pick 3
```

The `pick` call now renders quote/card template images **synchronously**
(typically 1–3 s) and writes the real PNG URL into `post.assets[0].url`,
so the dashboard shows it immediately. The response includes a `webUrl`
field — the dashboard URL where the user can review the post. Surface it
to the user when you confirm the pick.

The agent should NOT try to assemble `--style/--variant/--asset/--slot`
itself — that's the power-user path. `--pick <N>` is the canonical flow
because the CLI already cached every option's `pickArgs` from the
`options` call.

### Recipe — "make me a carousel" (no library asset required)

```
# 1. Confirm cards exist (auto-generated from post copy on creation).
pking visuals cards list <postId>

# 2. (Optional) tweak any card — title / body / stat number.
pking visuals cards edit <postId> --card 2 --body "New punchline" --rerender

# 3. Render the carousel PDF. Style is optional; defaults look fine.
pking visuals carousel <postId> --style glass-morphism --variant 2
```

If `cards list` returns an empty array, the post was created without
carousel-friendly content — write cards manually with
`pking visuals cards set <postId> --file cards.json` (a JSON array of
`{ number?, title?, body? }` objects), or regenerate the post with a
carousel-friendly theme via `pking posts generate`.

## API keys

```
pking keys list
pking keys create [--name "..."] [--scope <read|write>]
                                           Returns plaintext key once.
pking keys revoke <keyId>
```

---

## Error envelope

PostKing returns errors as JSON with consistent shape:

```json
{
  "error": "RATE_LIMITED",
  "message": "Too many requests",
  "retryAfter": 30,
  "checkoutUrl": "https://try.postking.app/billing?..."
}
```

Common codes:

| Code | Meaning | Action |
|---|---|---|
| `UNAUTHORIZED` | Invalid / expired token | `pking login` |
| `RATE_LIMITED` | Throttled | Wait `retryAfter` seconds |
| `INSUFFICIENT_CREDITS` | Out of plan credits | Surface `checkoutUrl`; stop |
| `FREE_CAP_REACHED` | Free-tier publish cap hit | Surface `checkoutUrl`; stop |
| `VALIDATION_ERROR` | Bad input | Show `message`, ask user to correct |
| `NOT_FOUND` | Bad id | Re-list and ask user to pick |

The CLI surfaces these as exit code != 0 with the JSON in stderr.
