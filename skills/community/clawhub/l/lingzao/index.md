# Lingzao Skills Index

## Purpose

`lingzao-skills/` owns the distributed Agent Skill package installed by Claude
Code, Codex, OpenClaw, and similar agent runtimes.

## Key Files

- `SKILL.md`: user-facing usage instructions. Keep it short and command-focused.
- `VERSION`: distributed Skill version.
- `skill-card.md`: ClawHub-facing summary card. The current ClawHub CLI filters
  this generated card out of runtime publish artifacts.
- `scripts/setup.sh`: wrapper and saved-config setup.
- `scripts/configure.py`: local config writer.
- `scripts/check_version.py`: remote/local version check.
- `scripts/lingzao_client.py`: CLI implementation for Lingzao commands.
- `agents/openai.yaml`, `agents/openclaw.yaml`: agent metadata.

## Release And Distribution Checklist

Use this checklist whenever a Skill-facing change is intended for public
distribution. The canonical release runbook is
`../docs/runbooks/skill-release-and-clawhub.md`.

1. Confirm the release lane:
   - R2/CDN: `npm run skill:release:r2` updates direct installs from
     `https://assets-tian.midao.site/skills/lingzao`.
   - ClawHub: use the explicit publish command documented in
     `docs/runbooks/skill-release-and-clawhub.md`; do not run the bare CLI
     command.
2. Keep public surfaces aligned before release:
   - `VERSION`
   - `SKILL.md`
   - `index.md`
   - `skill-card.md`
   - `agents/openai.yaml`
   - `agents/openclaw.yaml`
3. Update `skill-card.md` when the public capability set, paid-credit/API-key
   boundary, output type, risk/compliance wording, install link, dashboard
   link, or public positioning changes. Skip it only for internal fixes that do
   not affect marketplace understanding.
4. Run focused Skill validation before publishing. At minimum, run
   `git diff --check` and a package dry run; add Python compile, focused Skill
   tests, typecheck, lint, and unit tests according to release risk.
5. For ClawHub, run `clawhub whoami` first, then a `--dry-run` publish when the
   version or owner is uncertain. The bare command can infer the wrong
   slug/name/version; always pass explicit `--slug lingzao`, `--name "灵造"`,
   `--owner ITxiaohao`, and `--version "$version"`. ClawHub rejects duplicate
   versions; bump `VERSION` before publishing a new runtime package.
6. After ClawHub publish, verify with
   `clawhub inspect lingzao --versions --files --json`.

Current packaging boundary:

- `clawhub skill publish` filters root `skill-card.md` from publish artifacts.
- `scripts/release-skill-r2.ts` includes `SKILL.md`, `VERSION`, `agents/`,
  `playbooks/`, `scripts/`, and `skills/`, but not `skill-card.md`.
- Therefore `skill-card.md` is a repository-maintained marketplace summary and
  review source. Do not assume publishing updates a visible ClawHub card unless
  `clawhub inspect` proves it.

## Change Log

- 2026-06-26 11:38 +0800: bumped `VERSION` to `0.1.66` and updated
  `scripts/lingzao_client.py`, `SKILL.md`, `skill-card.md`, and Skill CLI
  tests; reason was making `get-article-detail --output /tmp/article.md` save
  the complete WeChat official-account article body as a local Markdown file
  while default chat output shows only the file path and short summary. This
  lets agents read the saved file for full-article analysis without pasting the
  entire article body into the conversation. Review follow-up added preflight
  validation so unwritable output paths fail before the paid article request is
  sent. Verification passed with Python compile, focused Skill CLI tests,
  `git diff --check`, and `npm run skill:package`; follow-up is a public Skill
  CDN/R2 and ClawHub release after PR merge.
- 2026-06-25 20:18 +0800: bumped `VERSION` to `0.1.65` and added
  `playbooks/self-account-peer-horizontal-diagnosis.md`; reason was A Tian's
  same-stage account comparison workflow where a user sends their own profile,
  asks Lingzao to find 5-15w follower AI or same-track creators, and wants a
  report explaining current gaps such as unclear frontstage memory, fast speech
  without hierarchy, decorative covers without a visual hammer, weak title
  click reasons, uncolumnized viral assets, or unclear follow reasons. The new
  playbook sits between own-account diagnosis and benchmark discovery: it
  selects 3-5 active peer accounts, shows follower/update/recent-hit evidence,
  compares account memory, title, cover, opening, proof assets, content columns,
  comment demand, follow reason, and acquisition path, then outputs top gaps,
  a 30-day adjustment plan, next content experiments, and a human small-test
  closing. `SKILL.md`, `xhs-operation-task-tree.md`, OpenAI agent metadata, and
  `skill-card.md` were updated to route "横向对比 / 同级账号 / 找 5-15w 和我比"
  requests into this report flow. Review follow-up narrowed generic own-account
  concerns such as "看看我现在的问题" or "我是不是说话太快" back to
  `self-account-diagnosis-report-template.md` unless the user explicitly asks
  for horizontal comparison or peer accounts. Verification passed with
  `git diff --check` and `npm run skill:package`; follow-up is a separate
  public Skill CDN/R2 release after the PR lands.
- 2026-06-25 14:22 +0800: bumped `VERSION` to `0.1.64`, updated `SKILL.md` and
  `playbooks/lingzao-progressive-interaction-map.md`; reason was preventing
  Xiaohongshu `xhslink.com` homepage share text from being routed to one-post
  detail commands while treating title-snippet share text plus
  `前往【小红书】一探究竟吧` as one-post context, normalizing bare short links to
  `https://...`, making one-post wording outrank generic diagnosis wording, and
  requiring a final note URL or note_id plus 图文/视频 before detail lookup;
  verification passed with docs grep, `git diff --check`, and
  `npm run skill:package`.
- 2026-06-25 13:34 +0800: bumped `VERSION` to `0.1.64` and updated
  `SKILL.md`, `agents/openai.yaml`, `agents/openclaw.yaml`,
  `skill-card.md`, and `scripts/lingzao_client.py`; reason was exposing the
  new public WeChat official-account article commands to Skill users from the
  first backend release: `get-article-detail`, `get-article-stats`, and
  `get-related-articles`. Review follow-up added the explicit command examples
  to `SKILL.md` and removed missing engagement metrics from non-empty related
  article Markdown output. The public Skill wording stays command-oriented and
  provider-neutral. Verification passed with Python compile, focused Skill CLI
  tests, full unit tests, lint, typecheck, and Skill package dry run; follow-up
  is a separate public Skill CDN release after the API PR lands.
- 2026-06-24 16:45 +0800: bumped `VERSION` to `0.1.63`, added
  `playbooks/xhs-operation-task-tree.md`, and added a pre-generation
  clarification gate across image-generation playbooks. The task tree captures
  A Tian's latest course/product framing: Lingzao users should complete
  concrete Xiaohongshu operation tasks first, while course/tutorial copy is
  only the instruction manual when a task is blocked. It groups the workflow
  into homepage diagnosis, benchmark discovery, viral-note adaptation, topic
  generation, content production, cover/image work, pre-publish checks,
  post-publish review, acquisition paths, and knowledge-base automation. The
  OpenAI agent metadata now mirrors this task-tree route for operation-task and
  next-step workflow requests. The image gate records A Tian's feedback that
  one-sentence poster requests such as
  "给我做一张某某海报图" often produce generic ugly images when Lingzao generates
  immediately; the Skill now asks for reference images and color preferences
  first, then at most one route-changing detail such as platform/size, exact
  on-image text, or people/no-people before spending image credits.
- 2026-06-24 11:33 +0800: added
  `docs/runbooks/skill-release-and-clawhub.md` as the canonical release
  runbook; reason was making future agents update `skill-card.md` and run
  R2/CDN plus ClawHub publish/inspect intentionally instead of treating
  marketplace publishing as part of the runtime package.
- 2026-06-24 11:33 +0800: added `skill-card.md` as a ClawHub-facing summary
  card for the Lingzao Skill; it documents the public use case, paid-credit
  boundary, references, output shape, and risks without changing runtime Skill
  behavior. The current ClawHub CLI filters this file from publish artifacts.
- 2026-06-20 17:02 +0800: bumped `VERSION` to `0.1.62` and updated
  `scripts/lingzao_client.py`; reason was hiding Douyin similar-creator
  commercial pricing from Skill Markdown output; verification passed with
  Python compile, focused Skill CLI tests, typecheck, lint, build with local
  `DATABASE_URL`, and `git diff --check`.
- 2026-06-20 16:47 +0800: bumped `VERSION` to `0.1.61` and updated
  `scripts/lingzao_client.py`; reason was fixing PR #35 review feedback while
  keeping item-level Douyin commercial signals unavailable in Skill output;
  verification passed with Python compile, focused Skill CLI tests, typecheck,
  lint, build with local `DATABASE_URL`, and `git diff --check`.
- 2026-06-20 16:07 +0800: bumped `VERSION` to `0.1.60` and carried forward
  Douyin Skill updates on top of dev's `0.1.59`; reason was keeping the
  public Skill aligned with Douyin homepage/profile support after the dev
  merge, including unsupported homepage subtitle wording, missing commercial
  flag rendering, and the Douyin recent-post `--limit 20` cap; verification
  planned after resolving the `dev` merge.
- 2026-06-20 14:02 +0800: bumped `VERSION` to `0.1.59` and updated
  `scripts/lingzao_client.py`; reason was extending generate-image polling
  deadlines by the worker download buffer for each requested image, preventing
  slow-but-successful worker downloads from being charged shortly after the CLI
  exits with a timeout.
- 2026-06-20 16:20 +0800: bumped `VERSION` to `0.1.58` and updated
  `scripts/lingzao_client.py`; reason was fixing active generate-image batch
  recovery so `GENERATION_IN_PROGRESS` resumes polling with the server-returned
  active batch `requested_count` instead of the retry command's default count,
  preventing multi-image batches from timing out early after a user retries
  without `--count`.
- 2026-06-20 15:40 +0800: bumped `VERSION` to `0.1.57` and updated
  `scripts/lingzao_client.py`; reason was making the distributed Skill recover
  from `GENERATION_IN_PROGRESS` responses by continuing to poll the returned
  active generate-image batch instead of failing and leaving Codex/WorkBuddy
  users waiting for TTL release after losing the original POST response.
- 2026-06-20 15:20 +0800: bumped `VERSION` to `0.1.56` and carried forward
  Codex/WorkBuddy reference-image handling on top of dev's `0.1.55` Skill
  package; reason was preserving the generate-image PR behavior where
  chat-provided reference images are saved as local files without proactive
  format conversion, and copies are compressed only when inputs exceed 2 MB.
- 2026-06-20 15:02 +0800: bumped `VERSION` to `0.1.55` and added
  `playbooks/mother-content-cross-platform-distribution.md`; reason was A
  Tian's clarification that users asking for "一条龙", "全平台同步", or "分发包"
  should first receive a basic publishable package, not every possible platform
  at once. The new playbook turns one topic, draft, note breakdown, product
  update, screenshot, transcript, or oral idea into a mother content object,
  then defaults to Xiaohongshu + Moments + WeChat public account. It offers
  optional expansion to podcast, X platform, Knowledge Planet, Bilibili, video
  account/Douyin, Xiaohongshu graphic-note image package, Xiaohongshu spoken
  script, Vlog storyboard, or knowledge-base/SOP. The progressive router now
  sends "一条龙 / 全平台同步 / 多平台分发 / 一个模板发多个平台" requests to this
  playbook and only continues to image generation when the user asks for
  Xiaohongshu images, covers, graphic notes, or generated visuals.
- 2026-06-20 14:43 +0800: bumped `VERSION` to `0.1.54` and added a dense-output
  packaging rule across the Lingzao playbooks. Long single-note breakdowns,
  account reports, topic packages, creator distillations, keyword reports, and
  multi-section action plans should no longer end as a wall of chat text. When
  the result is worth saving, studying, sharing, or syncing, Lingzao should
  offer Word document, HTML/webpage preview, or knowledge-base-ready packaging.
  The single-note workflow now explicitly reminds users that a deep breakdown
  can be organized into Word, a colored webpage preview, or a structured
  knowledge-base version with title, cover, script, comment-demand, learnable,
  and do-not-copy libraries.
- 2026-06-20 14:20 +0800: bumped `VERSION` to `0.1.53` and strengthened the
  single-note breakdown trigger and depth rules. User phrases such as
  "完整分析这条笔记", "深度拆解", "拆细一点", "拍摄手法", "分镜", and "剪辑节奏"
  now route to the deeper single-note breakdown layer instead of a short
  summary. Vague note-link tests such as "看看" or "拆一下" should first return
  a light breakdown, then clearly offer the next layers: shooting/editing
  breakdown, comment-demand breakdown, outline/transcript/Vlog storyboard, or
  adaptation into the user's own graphic note, spoken script, or Vlog. The
  single-note playbook now includes a dedicated shooting/editing layer covering
  shooting mode, shot role, camera distance, movement, editing rhythm, sound
  design, production threshold, and beginner remake route.
- 2026-06-20 11:06 +0800: bumped `VERSION` to `0.1.52` and added
  `playbooks/creator-case-general-analysis-framework.md`; reason was A Tian's
  request to turn many accumulated track, creator, visual, comment, and
  benchmark examples into one reusable "一通百通" creator-analysis Skill. The
  new framework analyzes any creator case through 12 layers: surface track,
  memory anchor, new narrative, proof system, audience desire, content engine,
  format engine, comment demand, commercial entry, hidden resources,
  learnable/non-copyable/adaptable parts, and user-fit tests. It also records
  cross-track archetypes such as new-life narrative creators, room-as-identity
  creators, low-follower high-operation creators, face-led identity creators,
  interaction prompt creators, text-dense screenshot creators, high-production
  creators, list/information-source creators, AI workflow creators, and local
  translation creators. `SKILL.md`, the progressive router, and OpenAI agent
  metadata now route vague "这个博主很有意思/怎么拆/能不能学" cases through
  this parent framework before choosing narrower playbooks.
- 2026-06-20 10:28 +0800: bumped `VERSION` to `0.1.51` and added A Tian's
  room-as-identity lifestyle account pattern into Lingzao. The visual reference
  library now includes `Room-As-Identity Lifestyle Cover`, covering study-room,
  bedroom, desk, solo-living, reading, device, and small-room scenes where the
  room proves a life-stage narrative rather than acting as decor. The image
  integration guide now judges good/weak room-as-identity covers by whether the
  room proves age reversal, solo-living freedom, reading/digital setup, or a
  new life direction. The track library and single-note breakdown library now
  separate learnable parts such as title angle, space-as-proof composition,
  series framing, and object-as-ad potential from hidden resources such as prior
  operation experience, savings, property/rent freedom, devices, humor, and
  reading ability.
- 2026-06-19 18:59 +0800: bumped `VERSION` to `0.1.50` and updated
  `playbooks/image-generation-execution-workflow.md`; reason was PR review
  feedback that failed quality gates must not trigger an automatic extra paid
  `generate-image` call. The repair flow now stops at a repair brief unless the
  user already approved a counted batch that includes repairs, and asks for
  explicit confirmation plus credit scope before another paid generation.
  Verification passed with `git diff --check`, Python compile, `npm run
  skill:package`, and focused Skill CLI unit tests. Follow-up: publish the
  Skill package separately after this PR merges if this Skill version is
  released.
- 2026-06-19 02:08 +0800: bumped `VERSION` to `0.1.49` and added A Tian's
  text-dense screenshot graphic-note style into the Lingzao image system. The
  visual reference library now includes `Text-Dense Screenshot Graphic Note`,
  covering public-account/X/Twitter/Weibo/memo-like dense text pages, keyword
  extraction before design, the 1-2 second first-page scanning rule, page-two
  proof/substance, and repeatable account-starting style. The image integration
  guide now treats long drafts, research material, and transcripts as a
  first-class generation flow and rejects raw screenshots or walls of text that
  do not expose the topic and keywords immediately.
- 2026-06-19 01:45 +0800: bumped `VERSION` to `0.1.48` and added A Tian's
  interaction-post visual rules into the Lingzao image system. The visual
  reference library now includes `Interaction Prompt Cover`, covering simple
  yellow-face/sticker covers, highlighted trigger words, staged PPT/comment
  screenshot scenes, comment/dwell-time intent, and the boundary that
  interaction topics must connect to the user's account mainline. The image
  integration guide now treats interaction posts as a first-class generation
  flow, adds good/bad standards, and records the Shantou food account example
  for account-relevant topic generation.
- 2026-06-19 01:18 +0800: bumped `VERSION` to `0.1.47` and added A Tian's
  face-led Xiaohongshu cover judgment into the visual system. The visual
  reference library now includes `Face-Led Keyword Video Cover`, covering
  expression, identity, authority, person/material contrast, top-bottom split
  screens, four-grid/diagonal layouts, and the rule that a face must contribute
  a click reason rather than merely appear. The Agent integration guide now
  distinguishes good face-led covers from weak selfies, warns against abruptly
  turning a graphic-note account into a face-led account, and tells Lingzao to
  switch to no-person knowledge cards when the creator lacks expression,
  authority, proof scene, or a repeatable face-video style.
- 2026-06-19 00:48 +0800: bumped `VERSION` to `0.1.46` and added
  `playbooks/image-generation-agent-integration-guide.md`; reason was A Tian's
  clarification that Lingzao needs not only a drawing Skill, but a stable way
  for domestic Agents to call the image-generation capability without exposing
  provider/model names, raw prompts, stack traces, or long parameter choices.
  The new guide defines a model-agnostic input/output contract, good-vs-bad
  image standards, reference-image remix rules, known generation bugs such as
  Chinese text instability, crowded covers, generic AI poster style, reference
  over-copy/under-follow, hallucinated material, multi-page inconsistency,
  cropping issues, and provider/network failures, plus A Tian's homework format
  for collecting good images, bad images, reference images, and track-specific
  examples.
- 2026-06-19 00:24 +0800: bumped `VERSION` to `0.1.45` and added
  `playbooks/image-generation-execution-workflow.md`; reason was A Tian's
  feedback that Workbuddy-style image generation can produce ugly results if
  the Skill only passes prompts to the model. The new execution workflow adds a
  visual-director layer: route style first, build a compact image brief, keep
  image text short, generate actual images when available, review the result,
  and repair common failures such as crowded covers, weak visual hierarchy,
  generic AI-poster style, dirty colors, wrong logo usage, copied references,
  fake data, and unreadable Chinese text. `visual-generation-and-cover-workflow`
  now points to this execution layer whenever generation is available.
- 2026-06-18 00:46 +0800: bumped `VERSION` to `0.1.44` and added
  `playbooks/single-note-breakdown-workflow.md`; reason was A Tian's
  calibration that one note link needs its own breakdown flow rather than being
  scattered across account breakdown, keyword-to-content, cover, comments, and
  post-publish review. The new workflow breaks one note by evidence scope,
  viral type, title, cover, outline/script, comment demand, why it exploded,
  learnable/non-copyable parts, and how to adapt it into the user's own
  graphic note, spoken script, Vlog storyboard, or knowledge-base card. It also
  adds a type library for dense dry-good tutorials, high-production cinematic
  notes, person/material contrast, female-growth viewpoint notes, and
  list/collection notes, with strict rules not to invent video seconds or
  comment insights when those details were not opened.
- 2026-06-18 00:32 +0800: bumped `VERSION` to `0.1.43` and reframed the
  Lingzao web dashboard as a tutorial and learning hub, not only a payment/API
  Key page. Installed users are now pushed toward the web page to learn how to
  install/configure Lingzao, ask Agent better questions, use Skill workflows,
  and study Agent/self-media operation lessons; paid credits remain the unlock
  for public-content lookup, image generation, and deeper research. Missing API
  Key/base URL CLI errors now mention tutorials and Agent/self-media workflows
  before recharge and API Key setup.
- 2026-06-18 00:20 +0800: bumped `VERSION` to `0.1.42` and added the free
  main-Skill installation plus paid capability entry guidance. Lingzao is now
  described as one free installed Skill that routes title, keyword, account
  diagnosis, benchmark, cover, pre-publish, post-publish, and knowledge-base
  workflows; public-platform users can install first and discover the hidden
  web-dashboard entry when they need paid public-content lookup, image
  generation, account inspection, note details, comments, or video-copy
  extraction. Also softened missing API key/base URL CLI errors so installed
  users are guided to `https://lingzao.atian.vip` for credits and API Key setup
  instead of seeing a cold configuration failure.
- 2026-06-18 00:00 +0800: bumped `VERSION` to `0.1.41` and added
  `playbooks/pre-publish-readiness-check.md`; reason was A Tian's calibration
  that Lingzao should behave as one routed creator-operation skill stack rather
  than isolated skills. The new pre-publish gate first asks whether the content
  is finished, then checks content clarity, image/page readiness, cover
  recognition, title clickability, first 3 lines or first 3 seconds, and
  natural keyword embedding before routing the user back to 24-hour review
  after posting. Also refined progressive routing to infer user interest from
  repeated breakdown requests, distinguish true drift from local-life
  cross-city transfer, and treat graphic/video/Vlog shifts as resource and
  publishing-rhythm decisions when appropriate. Benchmark discovery now filters
  long-stale accounts harder, avoids using 400k+ pure big accounts as ordinary
  imitation targets, handles 100k-300k accounts as possible partial references,
  checks comment quality for real demand, and allows local-life shooting/topic
  methods to transfer across cities.
- 2026-06-17 16:20 +0800: bumped `VERSION` to `0.1.40` and updated
  `scripts/lingzao_client.py` and `SKILL.md`; reason was adding the public
  `generate-image` command on top of `dev`'s `0.1.39` Skill package, using async
  Lingzao batches, automatic polling through `batches/:id`, `--count 1..5`,
  local `--image` multipart reference uploads, `--output` file saving, and fixed
  40-credit pricing with no `--quality` option; verification passed with Python
  compile and focused Skill CLI tests.
- 2026-06-17 18:03 +0800: updated `SKILL.md`,
  `scripts/lingzao_client.py`, and `tests/unit/skills/lingzao-client.test.ts`;
  reason was documenting Douyin `search-users` usage and rendering Douyin
  creator search results as direct profile links; local `VERSION` is `0.1.40`
  after the generate-image merge, so bump again only if `0.1.40` has already
  been released before this API work ships through the distributed Skill;
  verification passed with
  focused Skill CLI tests, typecheck, lint, build, and `git diff --check`.
- 2026-06-17 11:26 +0800: updated `SKILL.md`,
  `scripts/lingzao_client.py`, and `tests/unit/skills/lingzao-client.test.ts`;
  reason was keeping the Skill aligned with Douyin creator homepage support,
  including Douyin sec_user_id examples, profile insight Markdown rendering, and
  explicit guidance that Douyin homepage analysis does not include transcript
  text; local `VERSION` is now `0.1.40`, so bump again only if `0.1.40` has
  already been released before this API work ships through the distributed Skill;
  verification passed with focused Skill CLI unit tests, typecheck, lint, build,
  and `git diff --check`.
- 2026-06-17 10:31 +0800: bumped `VERSION` to `0.1.39` and added a
  post-diagnosis activation standard after user feedback that some users know a
  diagnosis is accurate but still lack action because of thinking inertia and
  psychological resistance. Own-account diagnosis now treats this as an
  activation gap, not a character flaw. The report should create an
  over-expectation feeling through conclusion + action advice + psychological
  reassurance, include one screenshot-worthy/share-worthy diagnosis card, and
  offer a light activation package that turns the diagnosis into the next note's
  topic, 3 titles, cover keyword, opening lines, and review data. Deeper
  activation that needs new benchmarks, note details, comments, backend
  interpretation, or 7/30-day content packages must explain the additional
  credit scope before expanding.
- 2026-06-17 10:19 +0800: bumped `VERSION` to `0.1.38` and added the
  Lingzao "人情味" SOP across global routing, own-account diagnosis, retention
  loops, product judgment, and A Tian's creator judgment framework. The Skill
  now explicitly says "不要让话掉在地上": when users have done account cleanup,
  know their problems, or resist changing, Lingzao should acknowledge that
  state, lower the action to one small next test, and end with one concrete
  follow-up question such as whether to work on the next title, cover keyword,
  opening, topic direction, draft, note link, or backend screenshot.
- 2026-06-17 10:10 +0800: bumped `VERSION` to `0.1.37` and refined
  own-account diagnosis endings after user feedback that the diagnosis was
  accurate but ended too abruptly at "立刻做". Own-account diagnosis now requires
  a human closing that acknowledges the user's resistance, frames change as one
  small experiment rather than a full account overhaul, names the smallest next
  action, and gives a concrete return loop such as sending the next title/cover,
  draft, published note link, or 24-hour backend screenshot for review.
- 2026-06-17 09:55 +0800: bumped `VERSION` to `0.1.36` and refined benchmark
  account recommendation tables after A Tian's live test. Benchmark discovery
  now treats updates within 15 days as strong freshness, prefers recent-hit
  works from the last 30 days, requires follower count, total liked count,
  latest update, recent-hit note metrics, account/content format, and a clear
  "why this can be a benchmark" explanation when available, sorts the visible
  first batch by follower count from high to low, and tells the user when the
  found accounts are mostly口播、图文、Vlog, or another format so Lingzao can
  continue with a pure graphic-note or other format-specific search.
- 2026-06-17 09:49 +0800: bumped `VERSION` to `0.1.35` and refined benchmark
  account discovery scope after A Tian's feedback. Benchmark discovery now
  defaults to up to 5 strong accounts for the first visible delivery, tells the
  user "我这边先给你 5 个你看看是否适合你", and treats 10-20 accounts,
  follower-range filtering, or continued multi-account verification as broader
  batch search that should only happen after the user confirms follower range,
  stage, city, audience, format, or asks for more.
- 2026-06-17 09:41 +0800: bumped `VERSION` to `0.1.34` and refined benchmark
  account discovery output after user feedback. `search-users` Markdown now
  renders direct Xiaohongshu profile links instead of user-facing raw creator
  IDs, and the benchmark discovery/report/knowledge-base playbooks now require
  each recommended account to include specific recent high-interaction works:
  note titles, note links, publish dates when available, visible metrics, and
  why those works are worth learning.
- 2026-06-17 09:33 +0800: bumped `VERSION` to `0.1.33` and added
  `playbooks/benchmark-account-discovery-quality-gate.md`, with routing updates
  in `SKILL.md`, `agents/openai.yaml`,
  `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/comparable-account-breakdown-report-template.md`,
  `playbooks/content-knowledge-base-workflow.md`, and
  `playbooks/search-credit-notice.md`; reason was user feedback that Lingzao
  found benchmark accounts that had already stopped updating. The new default
  quality gate says benchmark discovery should prefer accounts that are still
  updating, have recent high-performing works, and match the user's track,
  format, audience, and stage. Long-stale accounts should be marked as
  historical references, not main benchmarks.
- 2026-06-17 09:26 +0800: bumped `VERSION` to `0.1.32` and added
  `playbooks/xhs-profile-bio-design.md`, with routing updates in `SKILL.md`,
  `agents/openai.yaml`, `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/beginner-account-start-and-topic-radar.md`, and
  `playbooks/self-account-diagnosis-report-template.md`; reason was product
  calibration from A Tian that users also need help designing their
  Xiaohongshu 100-character personal intro. The new bio workflow treats the
  intro as homepage conversion copy instead of a slogan: who the account is,
  who it serves, what it keeps sharing, why to follow, and whether there is a
  city, product, service, or light contact path.
- 2026-06-17 09:17 +0800: bumped `VERSION` to `0.1.31` and added
  `playbooks/product-judgment-and-feedback-loop.md`, with routing updates in
  `SKILL.md`, `agents/openai.yaml`, and
  `playbooks/lingzao-progressive-interaction-map.md`; reason was product
  calibration from A Tian that the plugin standard is not only answering
  requests, but judging where the user is stuck, explaining the product in
  human language, creating content/sales narrative, turning feedback into
  product iteration, and deciding which requests are real demand versus noise.
- 2026-06-17 09:03 +0800: bumped `VERSION` to `0.1.30` and added
  `playbooks/audience-persona-fit-check.md`, with routing updates in
  `SKILL.md`, `agents/openai.yaml`,
  `playbooks/atian-creator-judgment-framework.md`,
  `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/xhs-title-design-check.md`,
  `playbooks/publishing-keyword-design-check.md`,
  `playbooks/keyword-to-publishable-content-package.md`,
  `playbooks/draft-rewrite-and-benchmark-workflow.md`, and
  `playbooks/self-account-diagnosis-report-template.md`; reason was product
  calibration from A Tian that title, keyword, and content-package work must
  first clarify who the content is for and who will click. The new audience
  layer handles female-oriented content, student/young-beginner mismatches,
  local-life city and location keywords, and reverse-infers user persona from
  the user's liked, saved, searched, or benchmark notes when the user does not
  know their audience yet.
- 2026-06-17 08:47 +0800: bumped `VERSION` to `0.1.29` and tightened
  `playbooks/keyword-to-publishable-content-package.md`; reason was addressing
  the remaining PR review thread about paid lookup filters. A/B/C or "用默认"
  now only proceeds when the default platform, note type, time range, and
  sorting have been visibly shown in the current conversation, or when the user
  has explicitly supplied both scope and filters. Otherwise the Agent must show
  the defaults and ask for "默认" or edits before any paid search.
- 2026-06-17 08:36 +0800: bumped `VERSION` to `0.1.28` and added
  `playbooks/xhs-title-design-check.md`, with routing updates in `SKILL.md`,
  `agents/openai.yaml`, `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/keyword-to-publishable-content-package.md`,
  `playbooks/draft-rewrite-and-benchmark-workflow.md`, and
  `playbooks/publishing-keyword-design-check.md`, plus
  `playbooks/self-account-diagnosis-report-template.md`; reason was product
  calibration from A Tian that Xiaohongshu title work should default to 3
  strongest titles rather than 10 titles plus top-3 selection. The new title
  layer checks whether a title has a concrete keyword anchor, a clear click
  reason, a truthful content promise, and cover fit within the usual
  20-character Xiaohongshu constraint; examples include seasonal/search anchors
  such as 高考志愿, contrast paths such as 小镇青年到纽约, curiosity hooks such as
  怎么没人早点告诉我, and numeric/travel guide hooks such as 10天9夜新疆游.
- 2026-06-17 08:21 +0800: bumped `VERSION` to `0.1.27` and updated
  `playbooks/post-publish-data-review-workflow.md`,
  `playbooks/visual-generation-and-cover-workflow.md`, and
  `playbooks/keyword-to-publishable-content-package.md`; reason was product
  calibration from A Tian. Published-note review now tells users to send
  complete Xiaohongshu backend screenshots without needing to understand fields
  like 3-second retention, 5-second retention, click rate, completion, or follow
  conversion; it also requires the note link, title/cover, and script/body text
  for concrete diagnosis. Visual generation now follows the current simple
  loop: keyword or content direction -> confirmed public reference search ->
  distillation/rewrite into original graphic-note pages -> generated images or
  fallback visual instructions -> about 300 Chinese characters of publishing
  copy, 10 keywords, and a comment prompt. Image prompts are treated as internal
  fallback/implementation details, not something ordinary users must write.
- 2026-06-17 08:11 +0800: bumped `VERSION` to `0.1.26` after PR review and
  updated `playbooks/visual-reference-style-library.md`; reason was removing
  private local filesystem paths from the distributable Skill. The visual
  library now keeps only sanitized style-group names and composition rules, so
  ordinary installed users do not see or depend on A Tian's local reference
  folders.
- 2026-06-17 08:05 +0800: bumped `VERSION` to `0.1.25` and refined
  `playbooks/keyword-to-publishable-content-package.md`; reason was simplifying
  the "one-stop content package" into a publishing-format triage instead of a
  heavy fixed pipeline. When users send keywords, saved notes, favorite examples,
  or several references and ask Lingzao to turn them into content, the Agent now
  first confirms whether they want spoken video, graphic note/image, or Vlog
  storyboard. Graphic-note users are guided to send reference images when they
  have them, otherwise Lingzao can produce a no-person knowledge-card version;
  spoken-video users receive direct-read scripts; Vlog users receive concrete
  shot-by-shot scenes and voiceover/on-screen text. Also updated
  `playbooks/lingzao-progressive-interaction-map.md` so vague "use these
  examples to make content" requests route through this light format question
  instead of defaulting into one rigid template.
- 2026-06-17 07:34 +0800: bumped `VERSION` to `0.1.24` and added
  `playbooks/post-publish-data-review-workflow.md`; reason was productizing
  published-note review into 24-hour, 48-hour, and 7-day checkpoints that combine
  note links, backend screenshots, title/cover, script/caption/graphic-note text,
  public metrics, and Xiaohongshu dashboard signals such as exposure, read/play,
  retention, completion, likes, collections, comments, shares, and follow
  conversion; also updated `SKILL.md`, `agents/openai.yaml`,
  `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/draft-rewrite-and-benchmark-workflow.md`,
  `playbooks/retention-and-follow-up-loop.md`,
  `playbooks/keyword-to-publishable-content-package.md`, and
  `playbooks/visual-generation-and-cover-workflow.md` so backend screenshots
  are never judged as isolated numbers and users are guided to send the related
  note link, title/cover, script, or page text; verified with Skill validation,
  package dry run, and repo checks.
- 2026-06-17 07:25 +0800: bumped `VERSION` to `0.1.23` and added
  `playbooks/visual-generation-and-cover-workflow.md` plus
  `playbooks/visual-reference-style-library.md`; reason was formally connecting
  Lingzao's image and cover work beyond reference-image prompts by routing
  Xiaohongshu covers, 4-page/7-page graphic notes, WeChat 1+3 image packs,
  no-person knowledge cards, AI/person tool infographics, travel/food/local-life
  covers, and product/ecommerce conversion images to either runtime image
  generation or ready-to-use prompt packages; also updated `SKILL.md`,
  `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/reference-image-graphic-note-workflow.md`, and
  `playbooks/keyword-to-publishable-content-package.md` so users with reference
  images follow the reference-image route while users without reference images
  get a default style from A Tian's visual reference library; verification
  planned with Skill validation, package dry run, and repo checks.
- 2026-06-17 07:06 +0800: bumped `VERSION` to `0.1.22` and added
  low-note homepage sample-size gates across `SKILL.md`,
  `playbooks/self-account-diagnosis-report-template.md`,
  `playbooks/lingzao-progressive-interaction-map.md`, and
  `playbooks/search-credit-notice.md`, plus strengthened
  `playbooks/keyword-to-publishable-content-package.md` default search
  confirmation rules for A/B/C content-package scopes; reason was preventing
  the Agent from
  forcing a full account diagnosis when a homepage has too few public notes,
  routing 0 notes to beginner setup, 1-2 notes to homepage first impression,
  3-5 notes to starter-account mini diagnosis, 6-9 notes to light account
  analysis, 10+ notes to standard account analysis, 20+ notes to standard deep
  diagnosis, and 40+ notes to deeper diagnosis or knowledge-base distillation
  after credit confirmation, while ensuring Standard/Bulk keyword-to-content
  searches list related terms before paid lookup; verification planned with
  Skill validation, package dry run, and repo checks.
- 2026-06-16 21:18 +0800: bumped `VERSION` to `0.1.21` and expanded
  `playbooks/keyword-to-publishable-content-package.md`; reason was adding A
  Tian's viral-reference filtering standards, including low-follower viral
  judgment, comment-demand checks, non-copyable one-off emotional events,
  interaction post boundaries, hot-topic borrowing rules, high-save/no-follow
  diagnosis, graphic-note vs spoken-script delivery modes, and a cover-style
  judgment library for female growth, AI tools, local life, food/travel, and
  good-product sharing; verification planned with Skill validation, package dry
  run, and repo checks.
- 2026-06-16 20:44 +0800: bumped `VERSION` to `0.1.20` and added
  `playbooks/keyword-to-publishable-content-package.md`, with routing updates
  in `SKILL.md`, `playbooks/lingzao-progressive-interaction-map.md`, and
  `agents/openai.yaml`; reason was adding a one-stop keyword-to-content
  workflow inside the Lingzao plugin that turns confirmed keyword searches into
  publishable Xiaohongshu content packages with topic angles, titles, cover
  copy, 4-page structures, body direction, 10 publishing keywords, visual
  notes, comment guidance, and review loops, while collecting the user's prior
  posts, favorite references, city, tone, and content style before making a
  full sample when available, and keeping ordinary user covers free of
  Lingzao/A Tian logos unless explicitly requested; first track judgment
  library covers female growth, 35+ career, good-product sharing, AI tools,
  local life, and travel guides; verification planned with Skill validation,
  package dry run, typecheck, lint, and focused Skill tests.
- 2026-06-16 20:05 +0800: bumped `VERSION` to `0.1.19` and added
  `playbooks/publishing-keyword-design-check.md`, with routing updates in
  `SKILL.md`, `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/draft-rewrite-and-benchmark-workflow.md`, and
  `agents/openai.yaml`; reason was adding a post-draft Xiaohongshu publishing
  keyword workflow inside the Lingzao plugin that designs the final 10
  keywords, separates industry, general-audience, audience/scenario,
  pain/result, and long-tail words, checks natural embedding across title,
  cover copy, opening lines, and keyword field, and avoids turning every
  keyword request into paid keyword ecosystem research; verification planned
  with Markdown lint checks, Skill package dry run, typecheck, and focused Skill
  tests.
- 2026-06-16 17:13 +0800: merged latest `origin/dev` into PR #24 and resolved
  conflicts in `VERSION` and `index.md`; reason was preserving the PR's newer
  `0.1.18` Skill version while keeping `dev`'s `search-suggestions` Skill CLI
  and release-handoff Change Log entry; verification planned with
  conflict-marker grep, `git diff --check`, and `npm run skill:package`.
- 2026-06-16 16:46 +0800: merged latest `origin/dev` into PR #24 and resolved
  conflicts in `agents/openai.yaml` and `index.md`; reason was preserving
  `dev`'s installed-skill `<skill_root>/playbooks` metadata fix while keeping
  the PR's keyword insight, creator distillation, and content knowledge-base
  playbook routing; verification planned with conflict-marker grep,
  `git diff --check`, and `npm run skill:package`.
- 2026-06-16 16:00 +0800: updated
  `playbooks/lingzao-progressive-interaction-map.md` and
  `playbooks/content-knowledge-base-workflow.md`; reason was addressing PR #24
  review feedback by gating creator homepage distillation to Xiaohongshu profile
  capabilities and routing Douyin creator homepage requests to post-level or
  keyword-level reference workflows instead; verification passed with
  `git diff --check` and `npm run skill:package`; follow-up at 16:04 further
  narrowed the progressive routing sentence itself so Douyin creator homepages
  do not enter the Xiaohongshu profile-based distillation route.
- 2026-06-16 15:50 +0800: updated
  `playbooks/lingzao-progressive-interaction-map.md`; reason was addressing PR
  #24 review feedback by pointing own-account diagnosis reports to the existing
  `self-account-diagnosis-report-template.md` playbook instead of a missing
  template path; verification passed with `rg` for the stale path,
  `git diff --check`, and `npm run skill:package`.
- 2026-06-16 15:40 +0800: updated
  `playbooks/keyword-insight-report-template.md`; reason was addressing PR #24
  review feedback by requiring keyword insight users to confirm
  `search-notes` sorting, note type, and time range, or explicitly accept
  defaults, before paid batch searches begin; verification passed with
  `git diff --check` and `npm run skill:package`.
- 2026-06-16 15:31 +0800: updated
  `playbooks/search-credit-notice.md`; reason was addressing PR #24 review
  feedback by making user-facing credit wording match the workflow rule that
  keyword/comparable-account results are benchmark/reference material, not target
  creator sample top-ups; verification passed with `git diff --check` and
  `npm run skill:package`.
- 2026-06-16 15:24 +0800: updated
  `playbooks/content-knowledge-base-workflow.md`; reason was addressing PR #24
  review feedback by keeping target-creator samples limited to the target
  creator's own available posts and moving keyword/comparable-account results
  into a separate benchmark/reference section; verification passed with
  `git diff --check` and `npm run skill:package`.
- 2026-06-16 15:17 +0800: updated
  `playbooks/keyword-insight-report-template.md`; reason was addressing PR #24
  review feedback by requiring platform selection before keyword insight
  searches, instead of letting agents infer or omit `search-notes --platform`;
  verification passed with `git diff --check` and `npm run skill:package`.
- 2026-06-16 15:04 +0800: updated `SKILL.md`,
  `playbooks/search-credit-notice.md`, and
  `playbooks/keyword-insight-report-template.md`; reason was addressing PR #24
  review feedback by keeping creator-distillation sample top-ups out of
  detail/comment calls and documenting Douyin `search-notes` sort and note type
  limits;
  verification passed with `git diff --check` and `npm run skill:package`.
- 2026-06-16 14:48 +0800: updated
  `playbooks/content-knowledge-base-workflow.md`; reason was addressing PR #24
  review feedback by making creator distillation sample top-ups come from more
  profile posts, confirmed keyword searches, or confirmed comparable-account
  searches, while reserving note details/comments/transcripts for enriching
  selected entries; verification passed with `git diff --check` and
  `npm run skill:package`.
- 2026-06-16 14:45 +0800: bumped `VERSION` to `0.1.17` and updated
  `SKILL.md`, `scripts/lingzao_client.py`, and Skill CLI tests; reason was
  exposing the public `search-suggestions` command while keeping Skill docs
  short and implementation-neutral; verification passed with Python compile, unit
  tests, integration tests, typecheck, lint, build, `npm run skill:package`,
  and `git diff --check`; follow-up is tracked in
  `docs/handoffs/2026-06-16-search-suggestions-skill-release.md` because the
  CDN/R2 Skill release remains a separate action.
- 2026-06-16 14:24 +0800: resolved PR #24 against latest `origin/dev` and
  updated `SKILL.md` plus `playbooks/keyword-insight-report-template.md`;
  reason was keeping the `0.1.18` creator-distillation Skill update mergeable
  while making keyword insight report guidance respect Douyin search sort
  limits; verification passed with `git diff --cached --check`,
  `python3 -m py_compile lingzao-skills/scripts/lingzao_client.py`,
  `npm run skill:package`, `npm run typecheck`, and focused Skill tests
  through `npm run test:unit -- tests/unit/skills/lingzao-client.test.ts
  tests/unit/skills/install.test.ts`.
- 2026-06-14 22:18 +0800: bumped `VERSION` to `0.1.18` and expanded
  `SKILL.md`, `agents/openai.yaml`,
  `playbooks/content-knowledge-base-workflow.md`,
  `playbooks/lingzao-progressive-interaction-map.md`,
  `playbooks/search-credit-notice.md`, and
  `playbooks/retention-and-follow-up-loop.md`; reason was adding creator
  distillation as a first-class knowledge-base workflow, including clear sample
  explanations, quick/standard/deep distillation modes, the standard
  50-representative-entry mix, creator research assets, mismatch refinement
  prompts, sample grouping fields for Word/HTML/CSV-style exports, credit-scope
  wording, and follow-up prompts that lead to export, comparison, or topic
  adaptation; verification planned with Skill validation, Python compile, Skill
  package dry run, manifest inspection, typecheck, and focused Skill tests.
- 2026-06-13 13:22 +0800: bumped `VERSION` to `0.1.17` and added
  `playbooks/keyword-insight-report-template.md`; reason was separating formal
  keyword insight reports from beginner topic radar, including scope tiers,
  related/dropdown keyword credit estimates, report structure, enterprise/brand
  action advice, and knowledge-base follow-up; verification planned with Skill
  validation, Python compile, Skill package dry run, manifest inspection,
  typecheck, and focused Skill tests.
- 2026-06-13 13:52 +0800: bumped `VERSION` to `0.1.16` and updated
  `SKILL.md` plus `playbooks/self-account-diagnosis-report-template.md`;
  reason was adding a lightweight knowledge-sync handoff that asks before
  syncing and routes ima, Obsidian, or Feishu actions to the user's configured
  Agent tools without adding Lingzao backend APIs or local sync commands;
  verification passed with `git diff --check`, `npm run skill:package`, and
  `npm run typecheck`.
- 2026-06-13 12:51 +0800: bumped `VERSION` to `0.1.16` and added
  `playbooks/content-knowledge-base-workflow.md`; reason was adding a
  user-owned content knowledge-base path for saved notes, public links,
  keyword results, viral examples, topic/title/cover libraries, and publishing
  review libraries while staying inside the product boundary of no public
  content database, no raw export, no Feishu plugin promise, and no automatic
  monitoring; added proactive save-destination prompts and portable export
  modes for Feishu-ready, local-folder, Markdown, CSV, Word, HTML, and ZIP-style
  packages; also tightened follow-up wording from automatic tracking to
  reusable user-initiated search templates; verification passed with Skill
  validation, Python compile, Skill package dry run, manifest inspection,
  typecheck, lint, focused Skill tests, and full unit tests.
- 2026-06-13 10:34 +0800: updated `agents/openai.yaml`; reason was fixing the
  OpenAI metadata prompt to point installed agents at `<skill_root>/playbooks`
  instead of the source-tree-only `lingzao-skills/playbooks` path;
  verification passed with path grep, `git diff --check`, and
  `npm run skill:package`.
- 2026-06-13 09:16 +0800: bumped `VERSION` to `0.1.15` and added
  `playbooks/*.md` creator workflow guidance for progressive routing,
  account diagnosis, comparable-account breakdowns, beginner topic discovery,
  track difficulty, monetization paths, draft rewrites, reference-image graphic
  notes, credit reminders, and follow-up loops; reason was moving A Tian's
  Lingzao Agent plugin playbooks into the distributed Skill package while
  keeping `SKILL.md` command-oriented; verification passed with Skill
  validation, Python compile, Skill package dry run, manifest inspection,
  focused Skill unit tests, and typecheck.
- 2026-06-10 15:29 +0800: bumped `VERSION` to `0.1.14`; reason was ensuring
  installed Lingzao Skills update after `get-note-detail` gained the required
  `--xhs-note-type` argument for Xiaohongshu detail calls; verification passed
  with `python3 lingzao-skills/scripts/check_version.py`,
  `python3 -m py_compile lingzao-skills/scripts/lingzao_client.py`,
  `npm run test:unit -- tests/unit/skills/lingzao-client.test.ts`,
  `npm run typecheck`, and `git diff --check`.
- 2026-06-09 11:43 +0800: bumped `VERSION` to `0.1.13` and updated
  `SKILL.md`, `scripts/lingzao_client.py`, and
  `tests/unit/skills/lingzao-client.test.ts` so successful research command
  Markdown includes a conservative estimated time-saved note and agents
  preserve or summarize that value; reason was making Skill value visible
  after each successful use without changing API, billing, or internal routing data;
  verification passed with targeted Skill CLI unit tests and
  `npm run typecheck`.
- 2026-06-10 10:49 +0800: updated `SKILL.md` and
  `scripts/lingzao_client.py` so search/profile list Markdown displays
  `xhs_note_type` as the follow-up `get-note-detail` argument; reason was
  making Agent drill-down from Xiaohongshu list results stable without asking
  users to label every note manually; verification passed with
  `python3 -m py_compile lingzao-skills/scripts/lingzao_client.py`, targeted
  Skill CLI tests, `npm run test:unit`, and `npm run lint`.
- 2026-06-10 10:49 +0800: updated `SKILL.md` drill-down wording to avoid
  internal routing mechanics; reason was keeping user-facing Skill guidance to
  the stable action of passing `--xhs-note-type` or asking 图文/视频; verification
  passed with public wording grep and `python3 -m py_compile
  lingzao-skills/scripts/lingzao_client.py`.
- 2026-06-09 20:57 +0800: updated `SKILL.md` and
  `scripts/lingzao_client.py` so `get-note-detail` accepts
  `--xhs-note-type image|video`; reason was matching Xiaohongshu split detail
  behavior while keeping the public Skill command explicit;
  verification passed with `python3 -m py_compile
  lingzao-skills/scripts/lingzao_client.py`, targeted Skill CLI tests,
  `npm run typecheck`, `npm run test:unit`, and `npm run lint`.
- 2026-06-09 09:36 +0800: bumped `VERSION` to `0.1.12` and updated
  `SKILL.md`, `scripts/lingzao_client.py`, and Skill CLI tests so agents ask
  for search/comment parameters before calling and never pass
  `--sort most_liked` for Douyin comments; reason was clarifying user intent
  before paid API calls and matching the Douyin comments endpoint boundary;
  verification planned with Skill CLI unit tests and full unit/lint checks.
- 2026-06-09 09:28 +0800: updated `SKILL.md` and
  `scripts/lingzao_client.py` so `get-note-comments` accepts
  `--sort latest|most_liked` and renders the selected sort; reason was adding
  Xiaohongshu liked-count sorting to the Skill command while documenting
  Douyin as latest-only; verification passed with targeted Skill CLI unit
  tests.
- 2026-06-09 09:15 +0800: extended
  `tests/unit/skills/lingzao-client.test.ts` for the new
  `get-note-comments` command payload and Markdown rendering; reason was
  locking the user-facing Skill CLI behavior after adding comments support;
  verification passed with targeted Node unit tests; follow-up is to publish a
  Skill package release if this capability rolls out.
- 2026-06-08 22:03 +0800: bumped `VERSION` to `0.1.11` and added
  `get-note-comments` to `SKILL.md` and `scripts/lingzao_client.py`; reason was
  exposing the new platform-neutral public comment command for Xiaohongshu and
  Douyin; verification planned with typecheck, unit tests, integration tests,
  lint, and a future Skill package release.
- 2026-06-08 20:15 +0800: bumped `VERSION` to `0.1.10` and published the
  Skill package to R2; release includes search-note sort/type/time filters,
  public `图文笔记` wording, and Douyin `search-notes` examples; verification
  passed by checking public `VERSION`, `manifest.json`, discovery index, and
  the local `v0.1.10.zip` contents.
- 2026-06-08 19:05 +0800: changed `scripts/lingzao_client.py` so
  `search-notes --note-type` exposes `图文笔记` instead of `普通笔记`; reason was
  keeping the user-facing Chinese label clear across XHS and Douyin;
  verification passed through targeted Skill CLI tests in `npm test`.
- 2026-06-08 18:15 +0800: updated `SKILL.md` examples so `search-notes` shows
  Douyin topic search alongside XHS examples; reason was adding Douyin support
  behind the same platform-neutral command; verification passed with
  `npm run typecheck` and `npm test`; follow-up is to publish a Skill package
  release if these docs are included in rollout.
- 2026-06-07 16:09 +0800: updated routine Skill update guidance to prefer
  direct CDN overwrite install instead of `npx skills update lingzao -g`;
  reason was update commands can stop at a well-known skill notice without
  replacing the local package; verification inherited from prior Skill update
  command tests in this working tree; follow-up is to revisit if the skills CLI
  update behavior changes.
- 2026-06-07 12:23 +0800: created `lingzao-skills/index.md` to map Skill package
  structure, update rules, and release-sensitive files; verification skipped
  because this is a docs-only change; follow-up is to update this index when
  CLI commands, versioning, or install behavior changes.

## Gotchas

- Do not put internal service names, internal endpoints, raw payload details,
  cache URLs, or billing internals into user-facing `SKILL.md`.
- Routine updates must preserve saved config in `~/.lingzao/config.json`.
- Do not tell users to re-enter API config unless setup is repairing a broken
  wrapper path.
- Use direct CDN overwrite install for routine updates:
  `npx skills add https://assets-tian.midao.site/skills/lingzao --skill lingzao -g --copy`.
  Do not prefer `npx skills update lingzao -g`, because it can stop at a
  well-known skill notice without replacing the local package.
- Prefer versioned release archives in discovery metadata; `latest.zip` can be
  cached and should not be the only source of truth.
- Keep Skill CLI commands aligned with public capabilities and Dashboard install
  instructions.
