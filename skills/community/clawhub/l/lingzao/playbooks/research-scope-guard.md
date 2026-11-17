# Lingzao Research Scope Guard

Use this whenever a task may trigger Lingzao search, account lookup, note lookup,
keyword research, comparable-account research, comment lookup, transcript
lookup, full-copy lookup, batch reference discovery, or image generation.

## Core Rule

Confirm business scope only when it changes the result materially. If the user
already gave a clear, small request, proceed without a separate scope notice.

## Internal Stop Rule

Use these as silent operating limits for one user request:

- Keep the first pass to at most 5 Lingzao lookups or one confirmed image batch.
- Do not launch many searches concurrently from one broad instruction. Search,
  inspect the evidence, then decide whether another lookup is necessary.
- Stop before adding unrequested keywords, accounts, note details, comment
  pages, transcripts, profile depth, or image variants.
- Before expanding, state the exact added business scope and ask one concise
  question.
- A clear user request for a known single link, one keyword search, one profile,
  or one image batch does not need an extra confirmation message.

## Scope Semantics

- One search can return multiple results. Do not describe it as one operation
  per returned item.
- Each actually searched keyword is a separate search. Group related terms and
  start with the smallest useful set.
- Opening selected note details, comments, full copy, subtitles, transcripts,
  or deeper structure expands the task beyond the initial list search.
- Creator discovery and creator verification are different scopes. Start with
  discovery, then verify only the strongest candidates needed for the answer.
- Do not hide pagination or multi-page fanout. Fetch another page only when the
  user requested more coverage or the first page cannot answer the task.
- For benchmark discovery, recommend up to 3 strong starter accounts. Expand to
  5 or more only after the user confirms the direction.
- For account diagnosis, match the workflow to the visible sample size:
  - 0 posts: beginner setup, not account diagnosis.
  - 1-2 posts: homepage first impression and single-post feedback.
  - 3-5 posts: starter-account mini diagnosis.
  - 6-9 posts: light account analysis.
  - 10+ posts: standard account analysis can be offered.
  - 20+ posts: standard deep diagnosis can use `--limit 20`.
  - 40+ posts: deep diagnosis or distillation can use `--limit 40` after the
    user confirms that deeper deliverable.

## Choice-First Rule

Ask the user to choose only when both a small and a materially broader route are
plausible.

### A. 基础查询

Use for one known account, one known note, one keyword, or a small starter set.
It should return the most important visible signals and a first judgment.

### B. 深度查询

Use for multiple keywords, multiple accounts, full-copy analysis, transcripts,
comment demand, repeated pattern comparison, or a formal report. State the
planned sample and deliverable before starting.

User-facing wording:

> 这个需求可以先做快速判断，也可以直接做更完整的深度分析。
> A. 基础查询：先看 1 个账号 / 1 条内容 / 少量结果，给你快速判断。
> B. 深度查询：扩大到多个关键词、账号或内容，并视需要查看完整正文、
> 字幕、逐字稿或评论需求。
> 你回复 A 或 B，我就按这个范围开始。

Do not show this choice for every command. A precise single-object request
should proceed directly.

## Common User-Facing Scope Wording

For a small lookup:

> 我先按你给的这个对象做首轮判断，不额外扩大到更多账号、详情或评论页。

For batch reference search:

> 我先用当前关键词和小样本做第一轮筛选。如果方向成立，再决定是否扩大
> 关键词、打开更多详情或查看评论需求。

For benchmark-account discovery:

> 我先按「持续更新 + 近期高互动 + 和你阶段匹配」筛出 3 个值得先看的账号。
> 如果方向对，再扩到 5 个或按粉丝量、内容形式、城市继续筛。

For deeper work:

> 这一步会从当前的快速判断扩大到【新增关键词 / 账号 / 内容详情 /
> 评论页 / 字幕或逐字稿】，交付物会升级为【具体交付物】。你确认按这个范围继续吗？

## Image Generation

- If the user asks for one image and provides enough visual constraints,
  proceed with one image generation request.
- If the user asks for variants, use one `--count N` batch when supported.
- Ask before generating another batch or materially changing the concept.
- Frame the question around the new image direction or count.

## CLI Failure Guidance

When the CLI returns a user-visible failure reason and next step, preserve that
guidance in the response and do not automatically retry the failed operation.

## Placement And Tone

- Scope confirmation belongs immediately before a material expansion, not
  before every routine lookup.
- Prefer one short question.
- Do not finish all possible searches first and explain the expanded scope
  afterward.
