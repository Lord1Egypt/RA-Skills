# Lingzao Skill Index

- 2026-10-15 +0800：0.1.114 源码支持小红书深度主页 full_page/cursor；CLI --full-page/--no-full-page/--cursor，旧调用仍省略参数。整页50积分；按limit保持50/100。抖音新参数不支持。尚未发布。

- 2026-10-14 +0800：博主近期作品每次上限20条；所有平台旧请求limit=21–100按20返回并提示，继续原样使用next_cursor。0.1.113源更新，尚未发布。

- 2026-10-05 +0800: Image guidance now explains whole-batch reservation, available balance and shared queue retry. CLI commands are unchanged; this source update is unpublished.

- 2026-10-05 (unpublished): image execution and Agent integration playbooks
  distinguish an accepted queue entry from a retryable, uncharged rejection.
  Recovery reuses the original request ID and never delivers another intent's
  batch. The existing CLI and source version are unchanged; no package released.

## Purpose

Unpublished 0.1.111 accepts Xiaohongshu long URLs, `/discovery/item/`, note IDs
and short links without a media type for content, metrics and copy. Untyped
video details have `media.video=null`; query with `video` only when playback or
duration is needed (20 credits per successful query). It also accepts Douyin
`v.douyin.com` short links and copied share sentences for homepage and comment
workflows; each service resolves and validates the target identity before
continuing. Video generation (`generate-video`, added in unpublished 0.1.108) was
removed from the source on 2026-09-28 and has never been published.

This folder contains the Lingzao Skill package for Agent runtimes. Lingzao helps
Agents route creator-operation work, prepare creator research, run public
content lookups when the user has configured access, and generate creator image
assets within a confirmed task scope.

## Package Files

- `SKILL.md`: main Agent instructions and command guidance.
- `VERSION`: current Skill package version.
- `agents/`: Agent metadata.
- `assets/lingzao-logo.png`: packaged brand icon used by Agent metadata.
- `playbooks/`: creator-operation workflows used before answering.
- `playbooks/router-index.json`: centralized route cards for every playbook.
- `playbooks/router-cases.json`: representative user prompts and expected
  primary routes.
- `scripts/`: setup, version check, configuration, and CLI command scripts.
- `skill-card.md`: marketplace summary source.

## Public Boundaries

- Keep user-facing wording focused on Lingzao, creator research, and workflow
  support.
- Do not promise viral growth, guaranteed monetization, full monitoring, bulk
  data export, or copying another creator's content.
- Proceed directly for clear small online tasks. Before expanding keywords,
  accounts, details, comment pages, transcripts, profile depth, or image count,
  confirm only the added business scope.
- Keep Agent instructions focused on task scope. The CLI owns user-visible
  service-result wording derived from structured server responses.
- For service failures, use concise Lingzao retry language and include
  `error_id` only when it is returned.
- Keep credentials, temporary local paths, and sensitive debug details out of
  user-facing output.

## Release Checklist

Before publishing a new Skill package:

1. Confirm `VERSION` is bumped when user-visible behavior changes.
2. Keep `SKILL.md`, `agents/`, `playbooks/`, CLI output, and marketplace copy
   aligned.
3. Run focused Skill CLI tests plus Python compile.
4. Run project checks required by the release risk.
5. Inspect the published package or marketplace file list after release.

## Recent Version Notes

- `0.1.109`: Xiaohongshu `get-note-detail` accepts `xhslink.com` and
  `xhslink.cn` one-post short links without a note ID or `xhs_note_type`. The
  source package remains unpublished.
- `0.1.110`: Douyin homepage and comment commands accept `v.douyin.com` short
  links/share text and fail closed when the resolved identity is not a creator
  or numeric work ID. The source package remains unpublished.

- `0.1.108` review follow-up (historical; video generation was removed from the
  source on 2026-09-28 and never published): incomplete video downloads preserve existing files;
  failed downloads explain how to retrieve the completed video with the same UUID.
  This version remains unpublished.

- `0.1.108` (historical; removed from the source on 2026-09-28, never
  published): adds `generate-video` for text-to-video and single-start-image
  image-to-video. The CLI uses a stable request UUID, polls the independent
  asynchronous video worker, reports only real queue/status data, and downloads
  the completed video through the authenticated Lingzao route. At the time, source
  pricing was marked as limited-time: 480P 40 credits/second and 768P 65
  credits/second. This source version has not been published.

- `0.1.107`: `extract-video-copy` accepts canonical TikTok video URLs and
  returns complete native WebVTT plus plain text. Missing captions are
  no-charge; this source version has not been published to any marketplace.

- `0.1.106`: `extract-video-copy` now accepts canonical WeChat Channels
  `https://weixin.qq.com/sph/...` share links directly. Agents do not need a
  detail lookup first and must not attempt media download or decryption. This
  source-only package has not been published.

- `0.1.105`: Douyin `get-note-detail` now documents valid HTTPS
  `v.douyin.com/<short-code>` inputs alongside standard post URLs and numeric
  IDs. The top-level router uses detail for one-post content and reserves
  `extract-video-copy` for spoken copy, subtitles, or transcripts. Agents pass
  the original short URL to Lingzao without opening or expanding it first.
  Invalid formats ask for the original HTTPS share URL instead of automatic
  fallback or another paid detail attempt. This source-only package has not
  been published.

- `0.1.104`: `extract-video-copy` now sends a fresh explicit operation ID for
  each new intent and accepts `--operation-id <UUID>` to safely recover an
  ambiguous or interrupted request within 24 hours. Retrying with the printed
  ID and unchanged URLs replays the completed result without another online
  extraction; different URLs require a new ID. This source-only package has
  not been published. Replayed Markdown reports zero additional cost and tells
  the Agent to reuse the current ID for retries or create a new ID for a new
  intent; it never suggests the profile-only `--force-new` option.

- `0.1.103`: runtime prompts now describe task scope only. The old
  credit-notice gate is replaced by `research-scope-guard.md`: clear small tasks
  proceed directly, while broader keywords, accounts, details, comment pages,
  transcripts, profile depth, or image counts require business-scope
  confirmation. Structured service outcomes are converted into concise
  user-visible CLI guidance instead of being modeled as routine Agent policy.
  This source-only package has not been published.

- `0.1.102`: Xiaohongshu image-note detail Markdown now shows the complete
  ordered body-image list with a count and expiring-link reminder. JSON output
  remains structured and unchanged. It also adds command guidance for the six
  WeChat Channels research atoms. Creator discovery reuses verified finder IDs;
  video detail accepts
  search references or share URLs, while latest-only comments use the same
  numeric detail ID on every cursor page. Default Markdown preserves both the
  search reference and numeric detail ID for those follow-up calls.
  Agent and discovery metadata advertise the same platform support. The package
  retains the published `0.1.101` security hotfix described below and does not
  reintroduce its removed journal, file lock, or credential-derived fingerprint.
  An earlier dev-only WeChat Channels snapshot temporarily used source version
  `0.1.101`, but was never published under that identity; its changes are now
  included in this unpublished `0.1.102` rollup.

- `0.1.101` (published main hotfix): removed the implicit cross-process image request journal, file
  lock, and credential-derived fingerprint. `generate-image` now prints its
  request UUID before submitting; Agents explicitly restore an ambiguous or
  interrupted request with `--client-request-id <UUID>`. Omitting the option
  starts a new intent. Server-side idempotency and active-batch protection are
  unchanged. R2/CDN currently identifies this package as `0.1.101`; this is the
  sole published meaning of that version. Marketplace publication is tracked
  separately.
- `0.1.100`: insufficient-credit API and asynchronous image-batch failures now
  render one concise Chinese recharge instruction instead of exposing the raw
  `INSUFFICIENT_CREDITS` code or an English internal error, including
  partial-success batches whose remaining items cannot continue. The source
  package is prepared locally only and has not been published.

- `0.1.99`: added explicit one-to-one reference mapping. Callers can pair each
  ordered `--image` with one ordered output by setting
  `--reference-mode one_to_one` and matching `--count`; the CLI rejects
  mismatches and batches above four references before sending a paid request.
  Shared multi-reference behavior remains the default. This source-only
  package has not been published. Its former implicit retry journal was removed
  in `0.1.101`.
- `0.1.98`: `generate-image --count N` remains one real batch with N image
  items. The CLI keeps a privacy-safe pending request ID so an ambiguous
  POST response, interrupted poll, or repeated third-party Agent process
  resumes the same batch instead of generating and charging again. Terminal
  commands clear the pending intent, so an explicit later generation uses a
  new ID. If another batch is already active, the CLI waits for it to finish
  and then submits the new intent with its own unchanged ID instead of returning
  the old batch. This historical implicit journal behavior was removed in
  `0.1.101`; the package was not published.

- `0.1.97`: added one machine-checkable router for all 40 playbooks and a
  WeChat benchmark-fit/original-writing workflow. Agents now load at most one
  primary plus two gate/support playbooks, while liked article links remain
  optional when the user provides their own content. PR #294 review follow-up
  makes all 24 representative cases execute the routing decision, reports the
  actual successful-item charge for partial transcript batches, and includes
  WeChat official accounts in generated discovery metadata. This source-only
  package preserves the unreleased `0.1.95` and `0.1.96` changes and has not
  been published.

- `0.1.96`: short-video copy Markdown now preserves per-item retry, no-charge,
  and shorter-video guidance when one item is too large. This package change
  is prepared locally and has not been published.

- `0.1.95`: Instagram `search-notes` now explicitly searches Reels. Agents use
  `--note-type 视频笔记`, while legacy `不限` input is accepted and normalized
  to video semantics. This package change is prepared locally and has not been
  published.

- `0.1.94`: after a successful Lingzao install or update, the installing Agent
  now proactively shares the Lingzao feature usage manual once. Dashboard
  prompts for Codex, Claude Code, WorkBuddy, and QoderWork use the same link;
  failed installs and ordinary later conversations do not repeat it. Focused
  install tests, the focused Dashboard E2E, typecheck, focused lint, and the
  package dry run passed. R2/CDN and ClawHub `0.1.94` were published and
  publicly verified through their separate release lanes.
- `0.1.93`: adds Instagram public content and creator research to the same six
  platform-neutral commands. It preserves lossless creator/media IDs, exposes
  public avatar, cover, image, carousel, and video URLs present in the current
  response, and keeps search limited to the image/reel fields verified from
  live responses. Instagram cursors are request-identity bound, and mismatched
  profile/post targets fail closed without charging. Media URLs may expire and
  are not downloaded, proxied, or stored by Lingzao. Generated Skill discovery
  metadata lists Xiaohongshu, Douyin, TikTok, Instagram, and YouTube consistently.
  The package now keeps only the Lingzao logo under `assets/`; obsolete bundled
  visual samples and their Agent/marketplace references were removed before release.
- `0.1.92`: binds TikTok opaque cursors to the original search, creator, or
  content request; rejects mismatched TikTok/YouTube returned targets without
  charging; and routes YouTube channel/profile URLs to creator commands instead
  of asking for a content-type hint. Generated Skill discovery metadata now
  lists Xiaohongshu, Douyin, TikTok, and YouTube consistently. Existing
  capabilities and pricing are unchanged.
- `0.1.91`: adds YouTube public content and creator research to six existing
  commands, including canonical channel IDs, video/Short detail, top-level
  comments, and opaque pagination cursors. YouTube profile commands require a
  channel ID or `/channel/UC...` URL; ambiguous detail IDs and URLs require an
  explicit `--content-type video|short` hint. It preserves the TikTok V1
  guidance and adds audited no-charge handling for stale YouTube cursors and
  mismatched channel targets.
- `0.1.90`: added platform-neutral TikTok guidance for the six V1 public
  research commands, including canonical URL/ID rules, 20-item list limits,
  opaque cursor continuation, service-default comment order, and the explicit
  `analyze-user-profile` exclusion. The CLI now forwards list cursors and
  comment limits, rejects unsupported TikTok options before API calls, and
  restarts from page one when an overflow cursor becomes stale.
- `0.1.86`: added `account-report-evidence-visual-contract.md` and connected it
  to own-account diagnosis, comparable-account breakdown, and same-stage peer
  diagnosis. Formal account reports now have a shared standard for one-screen
  conclusions, public-data/sample boundaries, direct account/note links, real
  cover audits, viral asset reuse, account-evolution evidence, no fake backend
  metrics, and Word/HTML/Feishu/knowledge-base packaging when requested.
- `0.1.85`: added `weekly-content-motherpack-distributor.md` for weekly content
  update packages. Agents can turn the last 7 days, a scheduled interval, or a
  named calendar week of creator materials into 5 mother topics, park weak
  ideas in a debt pool, distribute strong topics to Xiaohongshu, WeChat public
  account, podcast/short scripts, community posts, and knowledge-base packages,
  and offer folder, Word, HTML/webpage, or Markdown delivery with image
  readiness, review gates, paid-scope boundaries, and next-week review loops.
- `0.1.84`: clarified `analyze-user-profile --force-new` guidance. Agents
  should not loop forced refreshes; repeated forced refreshes in the short
  protection window may be rejected with no charge, while ordinary repeat
  requests can still reuse the recent successful result.
- `0.1.83`: added starter creator-operation playbooks for zero-beginner
  onboarding, copy-paste prompt scope boundaries, benchmark-account starter
  discovery, visual reference style routing, travel handdrawn map workflows, and
  Xiaohongshu platform management and content compliance risk gates. Agents
  should start broad benchmark discovery with a narrow 3-account first pass,
  keep paid lookups inside the confirmed first-pass budget, expand only after
  the user confirms the direction, use public value first/product name
  later/no diversion action as the default Xiaohongshu management baseline, and
  check final Xiaohongshu-facing copy for off-platform diversion,
  private-contact guidance, incentivized comments, exaggerated guarantees, or
  unsupported sensitive claims before returning publishable text.
- `0.1.82`: made `generate-image` prompt handling more robust for Agents and
  Windows-style shells. The CLI now rejects empty prompts before sending a
  request, supports `--prompt-file` for UTF-8 long or multiline prompts, and
  supports `--prompt-stdin` for piped prompt input. Use these alternatives when
  shell quoting or command-line encoding might drop the prompt.
- `0.1.81`: clarified direct API recovery for `generate-image`, added visible
  partial-data guidance for Douyin `analyze-user-profile`, clarified
  Xiaohongshu `get-note-detail` routing, and improved `search-users` Markdown
  display. For `GENERATION_IN_PROGRESS` with a returned `poll_url`, keep
  polling the active batch instead of POSTing again; without `poll_url`, wait
  briefly and retry. Agents should keep successful homepage works separate from
  unavailable optional insight data, reuse `xhs_note_type` from
  list/homepage/profile results, and treat RED ID as display-only metadata
  while using public profile URLs for follow-up context.
- `0.1.80`: added an explicit paid-search budget stop rule for calling Agents.
  Agents now keep the first paid pass to 5 lookups or about 100 credits by
  default, ask before plans that exceed 100 credits, and require explicit user
  confirmation before starting plans over 200 credits.
- `0.1.79`: expanded `generate-image` CLI output for users and calling Agents.
  Markdown results now explain that short-window identical requests, including
  `prompt/size/output_format/count` and reference images, return the same Batch
  and should be polled instead of posted again. Active-batch recovery stderr
  also tells Agents to use one counted `--count N` request for same-prompt
  multi-image work instead of looping repeated `--count 1` calls.
- `0.1.78`: added `analyze-user-profile --force-new` for explicit fresh paid
  profile analysis while keeping default exact same-request reuse guidance and
  a no-charge reuse notice so repeat Agent calls can return the recent
  successful result without spending credits again. It also clarified
  `generate-image` batching guidance: when a user wants multiple images from
  the same prompt, Agents should make one counted request with `--count 2..5`
  instead of looping identical `--count 1` calls.
- `0.1.77`: retired the `search-suggestions` Skill command after the public
  Lingzao capability was removed from runtime discovery. Agents should use
  `search-notes` for topic/content ideas or `search-users` for creator
  discovery instead. The CLI no longer exposes the command; existing API route
  compatibility is handled server-side with a no-charge retired response.
- `0.1.76`: updated the Skill routing guidance and CLI error rendering so
  Agents can use structured Lingzao correction fields such as
  `agent_action`, `suggested_capabilities`, `expected_input`, and examples
  when a link, nickname, numeric ID, or platform-specific profile ID is sent
  to the wrong capability. Review follow-up routes ordinary homepage/basic
  homepage analysis to `get-user-posted-notes` first, reserving
  `get-user-info` for explicit profile stats/metadata. The CLI keeps
  service/provider internals out of user-facing output.
- `0.1.75`: merged the one-stop content package and benchmark quality-gate
  branch onto the latest `origin/dev`; keeps the Chinese WorkBuddy/SkillHub
  first screen and marketplace copy while preserving routes for keyword/link/
  image/inspiration inputs, brand Brief content packages, benchmark-copy
  template extraction, strict follower-range benchmark filtering, and the
  package/playbook changes from `0.1.74`.
- `0.1.74`: public-safe package index. The index now stays short and suitable
  for runtimes or marketplaces that include root package files.
- `0.1.73`: tightened service-failure wording and public playbook wording so
  Agents use fixed retry language and avoid unnecessary technical detail.
- `0.1.72`: rendered service-unavailable and timeout errors as Lingzao service
  status while preserving `error_id`.
- `0.1.71`: made creator search output show the follow-up user ID clearly and
  routed Xiaohongshu follow-up checks through that ID.

- 2026-10-14：新增小红书商品搜索、详情、评价；价格20/30/20积分。说明销量未知/下限、评价去标识化、详情评分缺失仍收费与单页边界；包更新尚未发布。
- 2026-10-14 (#649): Creator posted-notes signed cursor, stable same-page remainder and limit 20 across platforms; Skill 0.1.112. Per-call 20 credits unchanged. Douyin posted-notes accepts profile short links and share text, resolves them internally, and still charges 20 credits per public page without a preceding get-user-info call. Mock verification and pending real checks: docs/handoffs/2026-10-14-creator-post-pagination.md.

- 2026-10-15：版本 0.1.114：同时保留商品研究与创作者作品分页、旧 limit 兼容提示；源码更新尚未发布。

- 2026-10-16 +0800：0.1.115：商品评价不支持只看有图；搜索跨页可能重复SKU，汇总时按SKU去重。源码验证通过，未发布。 验证与待发布事项见 `docs/handoffs/2026-10-14-xhs-commerce.md`。
