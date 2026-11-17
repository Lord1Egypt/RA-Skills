# Benchmark Account Discovery Quality Gate

Use this playbook when the user asks Lingzao to find benchmark accounts,
reference creators, same-track accounts, low-follower viral accounts, or
accounts worth learning from.

This is a product-quality gate, not only a search prompt. Users should not have
to remember to add "持续更新并有爆款作品的账号" every time. That should be the
default quality standard when Lingzao finds benchmark accounts.

## Core Decision

The answer to the user's feedback is:

不用每次都自己加这句话。灵造默认就应该按「持续更新 + 近期有高互动作品 + 和你阶段匹配」来找对标账号；如果你自己已经找到账号，也可以直接发给我，我会帮你判断它值不值得学、适不适合你、哪些能学、哪些不能照抄。

So the workflow has two valid entrances:

1. User asks Lingzao to find accounts:
   - Lingzao must search and then verify freshness, hit performance, and stage
     fit before recommending.
2. User sends accounts they found:
   - Lingzao should skip discovery and use
     `comparable-account-breakdown-report-template.md` to judge fit.

Do not put the burden on the user to write perfect search wording.

## Default Discovery Standard

When the user asks for benchmark accounts, default to active, learnable
accounts:

- Active: still updating recently.
- Proven: has at least one recent high-performing work or a clear spike.
- Relevant: belongs to the user's track, format, and audience.
- Learnable: the user can imitate structure, topic, title, cover, or operation
  logic without needing the same face, wealth, city, job, product, team, or
  mature follower base.
- Stage-fit: beginners should see same-stage, low-follower, or early-path
  references first; mature accounts can appear as positioning references, not
  copy targets.

## Hard Gate: Benchmark Account vs Note Sample

Do not confuse a note that has some interaction with an account that is worth
benchmarking.

Main benchmark accounts must pass account-level proof. As a default:

- **Minimum account scale:** at least 1,000 followers for a main benchmark,
  unless the user explicitly asks for 0-1,000 follower seed-account observation.
- **Minimum account signal:** total liked count should not be tiny. For an
  early-stage benchmark, prefer at least several thousand total likes or a
  visible pattern of multiple notes getting meaningful engagement. An account
  with around 100 followers and a few hundred total likes is not a main
  benchmark.
- **Hit proof:** at least one clear high-performing note or a visible spike.
  For 1,000-5,000 follower accounts, a note with 300+ likes, or unusually high
  saves/comments, can be a useful proof note only if the account itself also
  has enough scale and a repeatable content lane.
- **Repeatability:** one lucky note is not enough. Check whether recent notes
  share a stable content lane, format, topic, or audience demand.
- **Currentness:** the account is still updating or the recent hit is still
  platform-relevant.

If an account is below 1,000 followers, do not label it as "主对标" or "对标账号"
by default. It can only be:

- `单篇样本`: one note can be studied for title, cover, opening, comment demand,
  or topic angle.
- `起号观察`: useful only when the user explicitly wants seed-account examples.
- `不推荐`: too little proof, too low scale, or no repeatable content lane.

Bad recommendation example:

- 100+ followers, 400+ total likes, one note with hundreds of likes/comments.
  This may be a **single-note topic/comment-demand sample**, but it is not a
  benchmark account for ordinary users.

User-facing wording:

这个账号目前粉丝和总赞都太低，不能当你的主对标。它最多只能作为「单篇样本」：这条笔记的标题、开头或评论需求可以看一眼，但不能证明这个账号已经跑出稳定方法。

## Follower Range Hard Constraint

When the user gives a follower range, treat it as a hard filter for main
recommendations, not a loose preference.

Examples:

- `1000-5000 粉`: main benchmark table can only include accounts in 1,000-5,000
  followers.
- `5000 左右`: main benchmark table should stay close to 5,000, usually around
  3,000-10,000 followers unless the user approves a wider range.
- `5-15 万粉`: main benchmark table can include 50,000-150,000 followers; 10k
  accounts and 300k+ accounts should not be mixed into the main table.

Use three result zones:

1. `严格符合`: within the requested follower range and passes benchmark proof.
2. `相邻可参考`: slightly outside the range but still useful. Keep separate from
   the main table.
3. `不作为主对标`: far outside the range, unknown follower count, too small, too
   large, stale, or weak proof.

If Lingzao search returns accounts outside the requested range, do not hide the
problem. Say:

这轮搜索返回了不少账号，但严格落在「1000-5000 粉」且有一波爆款证据的账号不足。我不会把 100 多粉或十几万粉的账号硬塞进主对标表里。可以继续用「近期爆款笔记反查作者」或放宽到 800-8000 粉再搜一轮。

If follower count is missing from `search-users`, do not claim the range was
met. Either verify selected candidates with profile lookup after scope confirmation,
or label them as `粉丝待核验` and keep them out of the strict main benchmark
table until verified.

## Context And Transfer Rules

Infer the user's interest from repeated requests. If the user keeps sending
similar accounts or notes, say the pattern back:

我发现你最近让我拆的内容都集中在「某某方向」。你是不是最近对这个方向感兴趣？你现在有自己的账号吗，还是先在找方向？

Use city only when city matters:

- For female growth, AI tools, career, health, fashion, good products, and most
  personal-IP content, city is usually not a main benchmark filter unless the
  user says it matters.
- For food, travel, local life, stores, city guides, city events, and local
  services, city matters for publishing, positioning, keyword, location, and
  audience.
- Local-life examples can transfer across cities. If a Nanning creator sends
  Yunnan, Beijing, Kunming, Shanghai, or other city references, do not call it
  scattered by default. They may be learning shooting style, topic selection,
  cover style, title formula, route design, or comment demand, then applying it
  to Guangxi/Nanning.

If references suddenly jump to a truly different audience or track, ask whether
this is still the old account direction or a new account direction. Then judge:

- can this be a new series inside the current account?
- should it become a separate account?
- will it confuse the target user?
- which parts are safe to borrow without changing account positioning?

## Display And Ranking Defaults

Do not make the user open every profile link just to judge whether an account is
worth learning.

For each recommended benchmark account, show these visible fields when
available:

- direct Xiaohongshu homepage link
- follower count
- total liked count / total account likes
- latest update time or latest visible post date
- content format: 图文、口播、Vlog、探店、美食、AI 教程、混合 etc.
- recent-hit works from the last 30 days when available, including note title,
  note link, public likes, collections, comments, and publish date
- why this account can be a benchmark
- what not to copy

Default ranking:

- Sort the first recommendation table by follower count from high to low when
  follower counts are visible.
- If follower count is missing for some accounts, put known-count accounts
  first and keep unknown-count accounts lower with "粉丝数未返回".
- Do not sort only by personal preference or search-result order when follower
  data is available.

If `search-users` already returns follower and liked counts, reuse those
numbers. If the final starter candidates are strong but profile stats are missing,
either call `get-user-info` for the selected candidates after scope confirmation, or
mark the field as unknown; do not silently omit the field from the output.

## Default Result Count

The first visible delivery should be 3 starter accounts, not 10-20 accounts.
After the user confirms that the direction is right, expand to 5 or more only
when they ask for it or provide a clearer scope.

Use this user-facing wording before or after the first recommendation table:

我这边先给你 3 个值得看的账号，看看方向是否适合；如果方向对，再扩到 5 个或按粉丝数量、账号阶段、内容形式、城市范围继续搜。这样首轮结果更聚焦，也更容易判断是否值得继续。

Rules:

- Verify enough candidates to return up to 3 strong accounts in the first
  starter round.
- Keep the first round inside the stop rule from
  `research-scope-guard.md`: no more than 5 lookups without another scope
  confirmation.
- Do not default to 5, 10, or 20 benchmark accounts when the user has not
  confirmed direction. More accounts mean a broader search.
- If fewer than 3 candidates pass the active/recent-hit/stage-fit gate, return
  the actual number and explain why the rest were filtered out.
- Only expand beyond 3 when the user asks for more or confirms a clearer
  follower range, stage, city, audience, or format.
- If the user wants follower count control, first narrow the follower range
  before continuing the search instead of making online requests on broad discovery.
- If the user gave a follower range and no candidates pass it, return "0 个严格
  符合" rather than filling the table with accounts that are too small or too
  large.
- If the user only gives a broad topic such as "AI 博主", "女性成长", or
  "本地生活", ask or infer a small starter scope before searching: follower
  range, topic angle, account format, city/local scope when relevant, result
  count, recent update, and at least one recent high-interaction work.

## Freshness Defaults

Use these as defaults unless the user gives another range:

- If the account updated within the last 15 days and the track/format fits, it
  can be directly included as an active candidate after the normal benchmark
  checks.
- Prefer accounts with at least one high-performing work in the last 30 days.
  For ordinary users, "最近一个月有爆款内容" is easier to understand than an
  abstract "recent-hit status".
- Fast-changing tracks such as AI tools, local life, hot topics, platform
  operation, and content workflows: last post ideally within 30 days; recent
  high-performing work ideally within 90 days.
- Evergreen tracks such as parenting, career, female growth, beauty, good
  products, health, and travel guides: last post ideally within 60 days; recent
  high-performing work ideally within 180 days.
- If an account has no public update in 90+ days, do not recommend it as a main
  benchmark unless the user explicitly wants historical archive analysis.
- If an account has no public update in the most recent month, usually do not
  recommend it as a main benchmark. Treat it as historical reference at most,
  especially when the user expects current benchmark accounts.
- If update dates are unavailable, mark freshness as unknown and do not rank it
  above verified active accounts.

Definition:

- "Recent active benchmark" means there is visible recent activity plus at
  least one work that performs noticeably better than the account's usual level
  or has strong public interaction.
- "Historical reference" means the account has useful positioning, title,
  cover, or content structure, but is not suitable as a current main benchmark
  because it stopped updating or its old viral works may not reflect the
  current platform environment.

## Recommended Search Flow

Before searching, follow `research-scope-guard.md`.

### If User Only Gives A Track Or Keyword

Example: "帮我找女性成长对标账号"

1. State the default quality gate in user language:

   我默认不只按关键词搜账号，会优先筛「还在持续更新、近 90/180 天有高互动作品、和你阶段匹配」的账号。断更很久的账号我最多放到历史参考，不会当主对标推荐。

   我这边先给你 3 个值得看的账号，看看方向是否适合；如果方向对，再扩到 5 个或按粉丝数量、账号阶段、内容形式、城市范围继续搜。

2. Confirm or infer:
   - track / keyword
   - target audience
   - user's current stage if known
   - preferred format: 图文、口播、Vlog、本地生活、好物、AI 教程 etc.

3. Candidate collection:
   - use creator search for the keyword when suitable
   - use note search for recent high-performing notes when creator search gives
     old or weak accounts
   - collect candidate authors from recent high-performing notes when possible

4. Candidate verification:
   - verify enough candidates to return up to 3 strong accounts in the first
     starter round
   - inspect recent public posts for each candidate before recommending
   - check latest update time
   - if the last visible update is within 15 days, treat freshness as strong
   - check whether the recent works include high-performing or clearly
     above-average posts
   - prefer the account's high-performing works from the last 30 days; if none
     are available, say so instead of implying it has a current hit
   - write down the specific high-interaction works that made the account pass:
     title, note link, publish date when available, and visible likes/
     collections/comments
   - check whether the content lane is stable or only had one unrelated spike
   - apply the account-level proof gate: follower scale, total liked signal,
     recent hit proof, and repeatability
   - if the user specified a follower range, separate candidates into
     `严格符合`, `相邻可参考`, and `不作为主对标`; only the first zone can enter
     the main recommendation table
   - check whether the format and resources are learnable for the user
   - filter out long-stale accounts, especially those with no recent-month
     updates
   - avoid treating 400k+ pure big accounts as ordinary imitation targets; use
     them only for mature positioning, broad market signal, or historical
     reference unless there is a very specific learnable part
   - when the user sends 100k-300k accounts, inspect briefly but clearly
     separate "可以局部参考" from "不建议现阶段照抄"
   - inspect comment quality: comments such as "太棒了", "太好了", "真的吗"
     may be low-value or inflated interaction; comments such as "求教程",
     "这是什么软件", "收藏了", "我也遇到这个问题", "求地址", "怎么做"
     indicate real demand and are more useful for benchmark judgment

5. Output ranked accounts only after verification. Default to sorting visible
   recommendations by follower count from high to low.

### If User Sends Their Own Found Accounts

This is often better when the user already has taste or a niche reference.

Do:

- say "可以，直接发你找到的账号会更精准"
- analyze each account with `comparable-account-breakdown-report-template.md`
- still check freshness and recent-hit status
- judge whether it is a main benchmark, local reference, historical reference,
  or not recommended

Do not:

- treat every user-provided account as worth copying
- skip stage-fit judgment
- ignore that an account may be stale even if the user likes it

## Candidate Labels

Every recommended account should receive one label:

- 主对标：active, relevant, recent-hit, and stage-fit.
- 局部参考：some parts worth learning, but not the whole account.
- 历史参考：good old structure or positioning, but stale or not current.
- 趋势观察：useful for topic direction, not for direct imitation.
- 单篇样本：the account is not qualified as a benchmark, but one note can be
  studied for title, cover, opening, topic, or comment demand.
- 起号观察：only for explicit seed-account study, not ordinary benchmark
  recommendation.
- 不建议学：stale, mismatched, too resource-dependent, off-track, or
  unlearnable for the user.

## Output Structure

For benchmark discovery, output:

1. 一句话判断：本轮是否找到了真正适合学的账号。
2. 筛选标准：say the default gate used, such as "持续更新 + 近期爆款 + 同阶段可学".
3. 推荐账号表:
   - default first starter round: up to 3 accounts
   - account name and direct Xiaohongshu profile link
   - follower count and total liked count / total account likes when available
   - freshness
   - latest visible update date or "半个月内有更新" when that is known
   - content format, such as 口播 / 纯图文 / 图文知识卡 / Vlog / 探店 / 混合
   - 1-3 recent high-interaction works, each with note title, note link,
     publish date when available, and public likes/collections/comments
   - follower/stage if visible
   - content lane
   - why it is worth learning
   - what not to copy
   - label
   - if fewer than 3 accounts pass, state the actual count instead of filling
     the table with weak accounts
4. 被筛掉的账号类型:
   - accounts below 1,000 followers with no account-level proof
   - accounts with around 100 followers / a few hundred total likes; these can
     only be single-note samples unless the user asks for seed-account
     observation
   - accounts outside the user's requested follower range; keep them out of the
     main recommendation table
   - accounts whose follower count is missing and has not been verified
   - long-stale accounts
   - old viral-only accounts
   - big accounts with mature trust only
   - 400k+ pure big accounts that mainly rely on mature IP and accumulated
     trust
   - accounts with uncopyable face/resource/city/product/team advantages
   - accounts whose interaction looks inflated or low-intent
   - one-off emotional viral notes that are hard for an ordinary creator to
     repeat
5. 下一步:
   - analyze one selected account
   - compare with user's own account
   - turn selected benchmarks into 7-day topics/title/cover package
   - save to content knowledge base
   - if the recommended accounts share the same format, offer a format-specific
     follow-up search

## If Results Are Weak

Do not pretend weak results are good.

Say:

这批搜索里有账号能参考，但真正适合当主对标的不多。主要问题是：有些账号断更，有些只有旧爆款，有些和你的阶段不匹配。我建议下一轮改成按「近期爆款笔记反查作者」或放宽/收窄关键词继续找。

Then offer:

- change keyword
- narrow by format
- narrow by city/audience/life stage
- search recent high-performing notes and reverse-find authors
- let user send accounts they already like

## Emotional Virality And Long-Term Keywords

Do not copy one-off emotional events just because they are viral. A breakup,
marriage, family conflict, or dramatic personal event can receive support and
encouragement, but it may not be repeatable or appropriate for the user's
account.

However, do not reject all emotional content. In long-term demand tracks such
as female growth, career anxiety, self-worth, emotional stability, parenting,
or relationship boundaries, emotional value plus clear keyword coverage can be
a real repeatable content model. Judge whether the account repeatedly covers
the same demand with title, cover, state, keywords, and structure, not whether
one story happened to explode.

## Good User-Facing Wording

Use this when replying to ordinary users:

你不用每次都加“持续更新并有爆款作品”这句话。以后我帮你找对标账号时，会默认优先筛：最近还在更新、近 90/180 天有高互动作品、和你当前阶段更接近的账号。断更很久的账号我会标成“历史参考”，不会当主对标推荐。

如果你自己已经收藏了几个喜欢的账号，也可以直接发给我。这样会更精准，因为我可以直接判断：它值不值得你学、你能学哪一部分、哪些是它自己的脸/资源/城市/粉丝基础，不能照抄。

When showing results, use direct links:

- Show the creator's Xiaohongshu homepage link, not only the creator ID.
- Show follower count and total liked count when available, so the user can
  judge stage-fit without opening the profile.
- Show the high-interaction note links, not only note IDs.
- Show public likes/collections/comments for the specific recent-hit notes.
- If the search result only has the 24-character `users[].id` returned by
  `search-users`, you may show a readable Xiaohongshu profile URL for users,
  but keep that ID for follow-up `--platform xhs --user-id ...` commands.
  Do not build profile URLs from `RED ID`, bio text, or custom short IDs.
- Direct IDs can stay in machine-readable data, but they should not be the
  visible user-facing deliverable.

When most recommended accounts are the same format, summarize that plainly:

这 3 个里面大部分是口播型账号，适合学选题、标题和表达节奏；如果你想做纯图文，我可以继续帮你找一批纯图文/知识卡账号。

Use the same logic for other formats:

- If most are 口播, offer pure graphic-note or no-face graphic references.
- If most are 图文, offer口播/Vlog references if the user wants to show up on
  camera.
- If most are local-life video探店, offer pure photo/card-style local-life
  accounts if the user cannot shoot video.

When the user asks for more after the first 3, narrow the next search before
expanding:

如果这 3 个里面方向对了，我可以继续帮你按粉丝量筛，比如 1000-5000 粉、5000-3 万粉、3-10 万粉；也可以按图文/口播/Vlog/本地城市继续找。这样会比一次性给你 10-20 个更聚焦，也更容易找到真正能模仿的账号。

## Do Not

- Do not recommend long-stale accounts as main benchmarks.
- Do not return 10-20 benchmark accounts by default; first deliver up to 3
  strong accounts.
- Do not keep verifying more candidates after the first round would exceed 5
  lookups unless the user has confirmed a larger scope.
- Do not treat account search results as final recommendations before checking
  recent posts.
- Do not call 100+ follower / few-hundred-like accounts "benchmark accounts" for
  ordinary users. Label them as single-note samples or reject them.
- Do not put accounts outside the requested follower range into the main table.
  Separate them as adjacent references or reject them.
- Do not claim an account is 1000-5000 followers if follower count was not
  returned or verified.
- Do not use "viral" if the account's only strong works are too old for the
  current task.
- Do not return creator IDs as the only visible result. Users need direct
  creator homepage links and specific high-interaction works. When the agent
  will verify profiles after discovery, keep the 24-character `users[].id`
  returned by `search-users` and do not substitute `RED ID` from bios.
- Do not omit follower count, total liked count, and recent-hit note metrics
  when the data is available.
- Do not mix口播、图文、Vlog accounts without telling the user what formats were
  found and whether a format-specific follow-up search is needed.
- Do not hide that additional account verification can add searches.
- Do not make online requests on a broad follower-range search before the user has
  confirmed the desired range or stage.
- Do not over-filter until no references remain; if there are few active
  accounts, say so and offer another search strategy.
