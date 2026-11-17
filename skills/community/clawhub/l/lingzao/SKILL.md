---
name: lingzao
description: 灵造是给 WorkBuddy、OpenClaw、Codex 等 Agent 使用的跨平台创作者研究与自媒体运营 Skill。安装免费，可先做选题、标题、封面、账号诊断、发布检查、复盘，以及公众号对标适配判断和原创写作；查询公开内容、评论、短视频文案、公众号文章数据或生成图片时需要配置灵造 API Key。
---

# 灵造：跨平台创作者研究与自媒体运营 Skill

灵造是一个主 Skill，不需要拆成标题、封面、账号诊断、图片生成等多个 Skill。
安装后，WorkBuddy、OpenClaw、Codex 等 Agent 会先把你的问题路由到合适的
创作者运营 playbook；只有当你需要查询公开内容、读取评论、提取短视频文案、
查看公众号文章数据、研究小红书商品或生成图片时，才需要配置灵造 API Key。

## 安装完成后的首次提示

当当前对话刚刚完成灵造 Skill 的安装或更新时，只有确认安装成功后，才在最终回复中
主动告诉用户一次下面的使用手册；安装失败、尚未验证成功或普通后续对话不要重复发送：

> 灵造已安装完成。你可以查看《灵造功能使用手册》：
> https://my.feishu.cn/docx/Y2HQdj5mzoFx4vxfij3cl9TRnjh?from=from_copylink
> 快速了解灵造的功能和使用方法～

## 从这里开始

| 你现在想做 | 可以直接这样问 Agent |
| --- | --- |
| 找内容方向 | “用灵造帮我围绕这个关键词做小红书、抖音、TikTok、Instagram 或 YouTube 选题，给我 10 个可发方向。” |
| 找对标账号 | “帮我找这个赛道值得学习的对标账号，并说明每个账号适合学什么。” |
| 拆一条笔记或视频 | “分析这条内容为什么有效，拆成标题、封面、结构、评论需求和可复用模板。” |
| 改标题和封面 | “基于我的草稿，给我 3 个最强标题和 5 个小红书封面方向。” |
| 做发布前检查 | “发布前帮我检查标题、封面、前 3 行、关键词和用户点击理由。” |
| 做发布后复盘 | “根据这条内容的数据和评论，帮我判断下次要调整什么。” |
| 做每周内容包 | “用灵造把我这一周的素材整理成 5 个母题，并分发成小红书、公众号、播客和短口播。” |
| 校准公众号对标 | “我发几篇喜欢的公众号文章和一篇自己的内容，你先判断适不适合我学，不适合再补找对标，然后帮我写成自己的文章。” |
| 做图片素材 | “先帮我设计封面/配图方向；如果需要生成图片，再按我确认的方向生成。” |
| 保存长结果 | “把这份分析整理成 Word、网页预览或知识库 Markdown 版本。” |

## 免费能做什么

不配置 API Key 时，灵造仍然可以作为创作者运营路由和 playbook 使用。适合：

- 判断账号定位、赛道难度、内容主线和商业路径。
- 设计小红书标题、封面方向、发布关键词和图文结构。
- 改写草稿、拆解用户已经提供的内容材料、做发布前检查。
- 根据用户提供的数据截图或复盘信息，输出下一步实验建议。
- 把用户提供的一周素材整理成 5 个母题，并规划小红书、公众号、播客、
  短口播、社群和知识库分发。
- 把长分析整理成 Word、网页预览或知识库 Markdown 结构。

## 什么时候需要 API Key

当 Agent 需要让灵造服务实际查询或生成内容时，需要到
<https://lingzao.atian.vip> 配置 API Key，包括：

- 搜索小红书、抖音、TikTok、Instagram、YouTube 或视频号公开内容和公开创作者；用结果辅助关键词/选题扩展。
- 查看创作者主页、近期公开内容、主页深度分析和对标账号证据。
- 打开小红书、抖音、TikTok、Instagram、YouTube 或视频号单条公开内容详情，读取一级公开评论。
- 打开公众号公开文章详情，查看公开文章数据，扩展相关文章。
- 提取公开短视频口播文案、字幕或 transcript。
- 根据提示词和参考图生成创作者封面、配图或海报素材。

用户已给出明确任务且属于小范围时，直接执行；首轮最多做 5 次外部查询。
如果需要扩大关键词、账号、内容详情、评论分页、文案提取或生图数量，说明新增的业务范围并请用户确认。

## 小红书商品研究

用户问“这个品类在卖什么、价格带、买家抱怨什么”时，先搜索商品，再按需读取详情和评价：

```bash
lingzao search-products --platform xhs --keyword "年会互动游戏" --limit 20
lingzao get-product-detail --platform xhs --sku "<搜索返回的sku>"
lingzao get-product-reviews --platform xhs --sku "<搜索返回的sku>" --sort latest --limit 20
```

详情或评价也可用
`--url "https://www.xiaohongshu.com/goods-detail/<sku>"`。裸 sku 必须来自同一用户此前成功的搜索；不要编造 ID 或链接。
搜索和评价用 `--cursor "<next_cursor>"` 翻页，原样复用并保持关键词、商品、排序和 limit 不变。不支持只看有图；搜索不同页可能重复 SKU，汇总时按 SKU 去重。
价格为人民币元。缺少销量是未知，带 `+` 是下限；店铺销量不等于商品销量。
`review_overview.status=unavailable` 表示详情已读取但评分缺失，应明确告诉用户。
买家评价取自评价工具原文，无买家身份；展示时间无年份，不推断日期。抽样评价不代表全部买家。
仅支持小红书，不做批量采集、自动监控或下载。

## 调用公开数据工具前

- 小红书、抖音、TikTok、Instagram 或 YouTube 内容链接：看内容用详情工具，看评论用评论工具，不要当主页链接。视频号 `/sph/` 分享链接可用于详情；评论必须先从详情取得纯数字内容 ID。
- 小红书、抖音、TikTok、Instagram 或 YouTube 主页链接：普通主页查看或基础主页分析先用
  `get-user-posted-notes`；只有用户明确要粉丝数、简介、关注数、总获赞等主页资料时
  才用 `get-user-info`；深度主页分析看 `analyze-user-profile`。
- 用户只给昵称、账号名、抖音号或数字 ID 时，不要自己拼 URL；先用
  `search-users` 找创作者，再用返回的主页链接或 ID 调主页工具。
- 视频号主页只接受 `search-users` 返回的 finder ID，不接受主页 URL，也不支持 `analyze-user-profile`。
- 抖音博主作品工具接受标准主页 URL、`search-users` 返回的 `MS4w...` ID，以及
  `v.douyin.com` 短链/分享口令；灵造内部解析，每页仍为 20 积分，无需先调用
  `get-user-info`。`get-user-info` 和 `analyze-user-profile` 也支持短链/分享口令。若识别结果是
  视频链接，改用 `get-note-detail`、`get-note-comments` 或 `extract-video-copy`，不要
  把视频身份当成主页身份继续查询。
- YouTube 主页工具只接受 `search-users` 返回的 channel ID 或 `/channel/UC...`
  URL；不要把 `@handle`、`/c/` 或 `/user/` 直接传给主页工具，也不要自动解析。
- TikTok 主页工具接受 canonical `https://www.tiktok.com/@handle` 或
  `search-users` 返回的 ID；单条内容接受 canonical `/@handle/video/<id>`、
  `/@handle/photo/<id>` 或显式 `--platform tiktok --note-id <id>`。不要传
  `vm.tiktok.com`/`vt.tiktok.com` 短链或裸 `@handle`。
- TikTok V1 不支持 `analyze-user-profile`。需要主页资料和近期内容时，按需分别调用
  `get-user-info` 与 `get-user-posted-notes`，不要隐藏组合调用。
- Instagram 主页工具接受 canonical `https://www.instagram.com/<username>/` 或
  `search-users` 返回的十进制字符串 ID；内容工具接受 canonical `/p/<code>`、
  `/reel/<code>`、`/reels/<code>`、`/tv/<code>`。评论命令的裸 `--note-id` 是
  shortcode，不是十进制 media ID。Instagram V1 不支持 `analyze-user-profile`，
  不要把主页资料与近期内容隐藏组合调用。
- 视频号创作者先用 `search-users --platform wechat_channels`，主页工具只复用返回的
  `v2_...@finder` ID。视频搜索返回的 `export/...` ID 可立即用于详情；评论必须使用
  详情返回的纯数字内容 ID。视频号口播文案提取直接使用公开
  `https://weixin.qq.com/sph/...` 分享链接，不需要先调用详情。视频号不支持深度主页分析、
  下载或解密。
- 如果 API 返回 `agent_action`、`suggested_capabilities` 或 `expected_input`，
  先按这些字段改调工具；仍不确定时问用户要主页链接或笔记/视频链接。

## 常见问题

**我没有 API Key，还能用吗？**
可以。先用灵造做选题判断、标题封面、账号诊断、草稿修改、发布检查和复盘。
等需要查公开内容、评论、短视频文案、公众号文章数据或生成图片时，再配置 API Key。

**为什么 SkillHub 里显示需要 API Key？**
因为灵造包含在线公开内容查询和图片生成能力。安装主 Skill 免费，但深度查询和
生成动作需要已开通的在线服务和 API Key。

**WorkBuddy 用户应该怎么用？**
优先安装这一个 `lingzao` 主 Skill。装好后直接把任务说给 WorkBuddy，例如
“帮我找对标账号”“帮我拆这条笔记”“帮我做发布前检查”。需要查公开数据时，
再按灵造网页教程配置 API Key。

**灵造能保证爆款、涨粉或变现吗？**
不能。灵造只做公开内容研究、运营判断和工作流辅助。输出用于帮助你做判断和
复盘，不是保证结果，也不能用于复制他人内容。

**网络或服务失败怎么办？**
先保留当前问题和链接，不要重复扩大查询范围。检查 `doctor`、API Key 和
网络状态；图片生成或短视频文案提取这类异步任务可能需要等待轮询完成。
如果灵造返回服务暂时不可用或响应超时，只用固定话术告诉用户：“灵造服务暂时
不可用，请稍后重试。”如果返回了 `error_id`，可以附上 `error_id`，方便后续排查。
如果 CLI 返回了明确的用户可见原因和下一步，保留该指引，不要改写成其他故障，也不要自动重试。

## Agent Playbooks

For higher-level creator strategy tasks, use the playbooks in
`<skill_root>/playbooks/` before answering. They turn Lingzao's public-content
tools into creator workflows instead of isolated lookups.

## Playbook Routing Contract

Before reading a playbook, read `<skill_root>/playbooks/router-index.json`. Do not scan every playbook or use the long progressive map as an always-on prompt.

Route in this order:

1. Classify `input_shape`: homepage, single content, keyword, draft, image, Brief, metrics, or vague request.
2. Classify `platform`: Xiaohongshu, Douyin, TikTok, Instagram, YouTube, WeChat, cross-platform, or unknown.
3. Classify `content_stage`: no content, in progress, finished before publishing, published, or recurring system.
4. Classify `intent`: direction, benchmark, diagnosis, production, visual, publish check, review, distribution, or knowledge base.
5. Classify `requested_output`: chat judgment, report, publishable copy, image brief, saved files, or reusable library.

Then select:

- exactly 1 primary playbook when a workflow is needed
- no more than 2 gate/support playbooks
- 0 primary playbooks when a direct CLI command or simple answer is sufficient

If confidence is high, load only the selected files and proceed. If two primary routes remain plausible, ask one question that requests the material that changes the route. Do not show users the internal playbook list.

Each entry in `router-index.json` is the centralized route card for one playbook:

- `role`: router, primary, gate, or support
- `category` and `platforms`
- user-like `signals`
- `required_inputs`
- expected `outputs`
- `avoid_when`
- allowed `companions`

Use the specialized routers only when needed:

- vague or link-only input -> `progressive-interaction`
- unclear Xiaohongshu operation stage -> `xhs-operation-tree`
- online lookup with expandable scope -> add `research-scope-guard`
- final Xiaohongshu-facing content -> add the relevant management/compliance gate
- formal evidence-backed report -> add `report-evidence-contract`

Never select a gate or support playbook as the main workflow. Never load more files merely because they are related.

The registry is complete only when this command passes:

```bash
python3 <skill_root>/scripts/check_playbook_router.py
```

`router-cases.json` contains representative user prompts and expected primary routes for regression checks.

Keep public wording focused on creator-content research and workflow support.
Do not promise viral growth, guaranteed monetization, full monitoring, bulk data
export, or copying another creator's content.

## Before Returning Xiaohongshu Copy

Before returning any final Xiaohongshu-facing title, cover copy, page text,
body/caption, publishing keywords, pinned comment, comment guidance, spoken
script, Vlog storyboard, Brand Brief deliverable, one-stop package, or
Xiaohongshu section of a cross-platform package, run
`playbooks/xhs-platform-management-risk-baseline.md` first, then
`playbooks/xhs-content-compliance-risk-gate.md`.

If the draft contains off-platform diversion, WeChat/private-contact guidance,
incentivized comment interaction, exaggerated guarantees, or sensitive
unsupported claims, do not leave those lines in the publishable version. Show a
short risk note and rewrite them into a safer Xiaohongshu version. Never
promise platform approval; say the rewrite lowers risk.

For commercial or product-related Xiaohongshu outputs, keep the order:

1. public value first
2. product or brand name after the reader benefit is clear
3. no off-platform diversion action in the publishable Xiaohongshu copy

## Install And Online Capability Entry

Lingzao is installed as one free main Skill. Users do not need to install
separate title, keyword, account-diagnosis, benchmark, cover, or review skills.
After installation, this main Skill routes the user's request to the right
playbook.

There are two user acquisition paths:

1. Community/course users:
   - They may already have A Tian's course, install link, setup steps, and
     API Key setup instructions.
   - Keep the in-chat explanation short: install the Skill, open the Lingzao web
     dashboard, follow the tutorial, enable online access, copy the API Key, then
     run setup.

2. Public-platform users from Xiaohongshu, Douyin, or other public content:
   - Do not require them to open the web dashboard and pay before they
     understand what Lingzao can do.
   - Let them install the free main Skill first.
   - Then explain the online entry in friendly language: the local
     playbooks can help judge drafts, titles, covers, directions, and
     publishing plans; when they need Lingzao to search public content, inspect
     accounts, open note/article details, read comments, inspect article data,
     extract video copy, or generate creator image assets, they need to open
     the Lingzao web dashboard, follow the tutorial, enable online access, and
     configure an API Key.

Present the web dashboard as the user's learning and setup hub:

- learn how to install and configure Lingzao
- learn how to ask Agent better questions instead of waiting in a group chat
- learn how to use Skill workflows for self-media operation
- learn account diagnosis, benchmark breakdown, title/keyword, pre-publish, and
  post-publish review workflows
- enable online access and get the API Key when they need public-content lookup or
  image generation

Use this wording when a user has installed the Skill but has not configured an
API Key yet:

你已经装好灵造 Skill 了。安装本身是免费的，它会先帮你判断你现在是在找方向、拆账号、写内容、做封面、配关键词，还是复盘数据。
如果你要继续查小红书、抖音、TikTok、Instagram、YouTube 或公众号公开内容、找对标账号、看账号主页、打开内容或文章详情、看评论区、查看公众号文章数据、提取短视频文案或生成创作者图片素材，就需要到灵造网页版开通在线服务并配置 API Key。
你可以打开 https://lingzao.atian.vip 看安装教程和使用教程，里面也会教你怎么用 Agent 做自媒体运营、怎么问问题、怎么用这些 Skill。需要查公开内容或生成图片的时候，再在网页里获取 API Key，配置好以后回来继续问，我会接着刚才的问题往下做。

Frame the two capability layers as:

- free install = get the workflow brain and routing layer
- web dashboard = tutorial, usage examples, self-media operation lessons, and
  API Key setup
- online access = unlock public-content lookup, image generation, and deeper
  research actions

Knowledge sync handoff:

- After a useful Lingzao research result or diagnosis report, do not sync it
  automatically. Ask first: 要不要把这份结果同步到你的知识库？可以选择
  ima / Obsidian / 飞书 / 暂不同步。
- If the user chooses a target, prepare a clean Markdown version and ask the
  current Agent environment to use the user's configured knowledge tool.
- For ima, call the installed ima Skill or ima knowledge-base tool if the user
  has configured one.
- For Obsidian, use the user's Obsidian CLI, Obsidian Skill, or approved vault
  workflow to write Markdown under a user-approved `Lingzao/` path.
- For 飞书, use the user's Lark/Feishu CLI or Skill with user authorization to
  create or update a document.
- Do not ask for or store ima, Obsidian, or Feishu credentials inside Lingzao.
  Synchronized content should contain only the user-approved report, public
  links, and useful conclusions; leave out credentials and details the user does
  not need.

Profile workflow:

- If the user asks for a creator homepage or a basic homepage analysis, use `get-user-posted-notes` by default. It returns recent posts and enough author/post data for a basic read.
- If the user sends a Xiaohongshu short link such as `xhslink.com/m/...` or
  `xhslink.cn/m/...`, or a copied share sentence such as
  `@... 查看Ta的主页>> https://xhslink.cn/m/...`,
  extract the short link, normalize bare links to `https://...`, and read the
  surrounding words before choosing a command. Do not classify the short link by
  path alone. If the context says account, homepage, creator, profile,
  benchmark, account diagnosis, homepage diagnosis, `Ta的主页`, or recent posts,
  treat it as a creator-homepage request and call
  `get-user-posted-notes --url "https://<short link>"`.
- If the user sends a Douyin `v.douyin.com` short link or copied share sentence,
  use the surrounding words to choose homepage or single-post intent. For
  homepage wording such as 账号、主页、博主、对标 or recent posts, pass the
  original short link/share sentence directly to `get-user-posted-notes`,
  `get-user-info`, or `analyze-user-profile` when those capabilities match the request.
  For recent posts, Lingzao resolves the target internally; each page costs 20 credits
  without a preceding `get-user-info` call;
  if it reports a video target, switch to the suggested single-post tool.
- If a Xiaohongshu short link has no context, ask whether the user wants creator
  homepage recent posts or one-post detail before making an online request. If the
  context says this note, comments, copy, transcript, one-post breakdown, or is
  a normal note share sentence with a title snippet plus `前往【小红书】一探究竟吧`,
  treat it as a one-post candidate, not a homepage. One-post words such as
  `这条` or `这篇` take priority over generic diagnosis wording. Do not route it
  to homepage tools. For either short-link domain, call `get-note-detail` with
  the extracted short URL directly; no final URL, note_id, or 图文/视频 question
  is needed. Ask only if the user's intent is still unclear between homepage and
  one-post detail.
- Only add `get-user-info` when the user specifically needs full profile-level stats such as bio, follower count, following count, total likes, total collections, or total note count.
- Use `analyze-user-profile` for Xiaohongshu deeper homepage copy/script/subtitle analysis, recent post text, covers, commercial signals, or product-note signals. For Douyin spoken copy or transcript text, use `extract-video-copy` on specific video URLs.
- YouTube V1 does not support `analyze-user-profile`. Compose the basic homepage tools explicitly only when the user asks for both recent videos and profile-level stats.
- Do not call `get-user-info` and `get-user-posted-notes` as a fixed pair unless the user asks for both profile-level stats and recent-post analysis.
- Do not force a full account diagnosis when the homepage has too few public
  posts. Route by visible sample size:
  - 0 posts: no account diagnosis; switch to beginner start/account setup
    guidance.
  - 1-2 posts: homepage first impression plus single-post feedback only.
  - 3-5 posts: starter-account mini diagnosis.
  - 6-9 posts: light account analysis.
  - 10+ posts: standard account analysis can be offered.
  - 20+ posts: standard deep diagnosis can use `analyze-user-profile --limit 20`
    after confirming that deeper scope.
  - 40+ posts: deep diagnosis, creator distillation, or knowledge-base
    distillation can use `--limit 40` after confirming that deeper scope.

Post drill-down workflow:

- Xiaohongshu list-style commands (`search-notes`, `get-user-posted-notes`,
  `analyze-user-profile`) return `xhs_note_type` on each note item when
  Lingzao can identify whether it is 图文 or 视频.
- When continuing from one of those note items to `get-note-detail`, pass the
  returned `xhs_note_type` directly as `--xhs-note-type`; do not infer the type
  from the URL.
- If a Xiaohongshu note item has no `xhs_note_type`, reuse its canonical URL or
  note_id directly, just like an `xhslink.com` or `xhslink.cn` short link.
  Content, metrics, and copy do not require a type. Untyped video results have
  `xhs_note_type=video` and `media.video=null`; request `--xhs-note-type video`
  only when playback or duration is needed. `get-note-comments`
  can still be called without this type.
- If `get-note-detail` returns `NOTE_NOT_FOUND_OR_INACCESSIBLE`, do not retry
  the same request or probe the other Xiaohongshu type automatically. Ask the
  user to confirm the note is public or provide the original share link.

## Setup

Resolve this `SKILL.md` directory as `<skill_root>`, then run setup once:

```bash
bash "<skill_root>/scripts/setup.sh" --base-url "https://your-lingzao-domain.com"
```

Environment variables override saved config:

```bash
export LINGZAO_API_KEY="lgz_xxx"
export LINGZAO_BASE_URL="https://your-lingzao-domain.com"
```

Check the connection:

```bash
~/.lingzao/bin/lingzao doctor
```

Before using Lingzao commands, check whether the skill has an update:

```bash
~/.lingzao/bin/lingzao check-version
```

If an update is available, stop the current Lingzao operation and update the skill first. Do not continue using an outdated Lingzao Skill for search, profile, subtitle, or extraction work.

To update the skill, rerun the installer. For `npx skills`, try:

```bash
npx skills add https://assets-tian.midao.site/skills/lingzao --skill lingzao -g --copy
```

Updating keeps the saved API config in `~/.lingzao/config.json`; no API key setup is needed again.

If `~/.lingzao/bin/lingzao` is missing or points to the wrong directory, repair the command wrapper:

```bash
bash ~/.agents/skills/lingzao/scripts/setup.sh --skip-doctor
```

If `~/.agents/skills/lingzao` does not exist, find the directory that contains `lingzao`'s `SKILL.md`, then run `scripts/setup.sh --skip-doctor` from that directory.

## Before Calling

Before running a command, ask only for inputs that change the call and cannot be
inferred. For `search-notes`, that is only a missing platform; missing filters
use the defaults below and are stated in the reply.

- Track external Lingzao commands internally for the current user request. Keep
  the first pass to at most 5 lookups or one confirmed image batch. If more
  keywords, accounts, details, comment pages, transcripts, profile depth, or
  images are needed, show the exact added actions and wait for scope confirmation.
- For broad creator or benchmark-account searches (`search-users`, "找对标账号",
  "找参考博主", "找同赛道账号"), do not start with a wide search. First ask or
  state a narrow starter scope: follower range, track/topic, account format,
  city/local scope when relevant, recent-update requirement, recent-hit
  requirement, and starter result count. Recommend starting with 3 accounts,
  then expanding only after the user confirms the direction. This keeps the
  research focused and avoids returning 100-follower seed accounts or huge mature
  accounts when the user asked for a specific stage.
- If the user asks how to write prompts for Lingzao or gives a broad copy-paste
  request, use `copy-paste-prompt-scope-boundary.md` first. Provide a
  ready-to-copy prompt that includes the smallest useful scope instead of
  telling the user to add broad instructions by themselves.
- If the user says they know nothing about self-media, are starting from zero,
  do not know what to post, or only say they want to make money, use
  `zero-beginner-onboarding-gate.md` before any search. Do not call online
  lookup first. Start with a free life-signal intake, give the lowest creator
  cognition, and move them to one concrete first task.
- For `search-notes`, ask one short question only when the platform is missing
  and cannot be inferred. When sorting, note type, or time range is not
  specified, do not ask first: use `general`, `不限`, and `不限` and state those
  defaults in one sentence at the start of the reply. Allowed values:
  sort can be `general`, `most_liked`, `popularity_descending`,
  `comment_descending`, or `collect_descending`; note type can be `不限`,
  `视频笔记`, `图文笔记`, or `直播笔记`; time range can be `不限`, `一天内`,
  `一周内`, or `半年内`.
- Douyin and TikTok `search-notes` currently support only `general`, `most_liked`, and
  `popularity_descending`. Do not pass `comment_descending` or
  `collect_descending` for Douyin or TikTok searches.
- Douyin and TikTok `search-notes` note type currently supports only `不限`, `视频笔记`,
  and `图文笔记`. Do not pass `直播笔记` for Douyin or TikTok searches.
- YouTube `search-notes` supports only `--sort general`, `--note-type 不限|视频笔记`,
  and `--time-filter 不限|一天内|一周内`; use the returned opaque `next_cursor`
  with `--cursor`, repeat the same keyword and filters, and do not infer internal
  pagination fields. Changing a filter invalidates the cursor before another lookup.
- For `get-note-comments`, ask whether the user wants latest comments or
  liked-count sorting before calling Xiaohongshu. Use `--sort latest` for latest
  comments and `--sort most_liked` for Xiaohongshu liked-count sorting.
- Douyin, TikTok, and Instagram comments currently support only `latest`;
  TikTok uses the service default order. Do not ask for or pass
  `--sort most_liked` on these platforms.
- YouTube comments support `latest` and `most_liked`; only top-level comments
  are returned. Reuse `next_cursor` unchanged and repeat the same `--sort` on
  every next-page request; omitting it after `most_liked` defaults to `latest`
  and invalidates the cursor before another lookup.
- Instagram content search is Reels-only. Use `--sort general`,
  `--note-type 视频笔记`, and `--time-filter 不限`; `--note-type 不限` remains a
  compatibility input but is executed and reported as 视频笔记. Do not use
  `search-notes` for account records; use `search-users`.
- Instagram profile, posted-note, and detail results may include public avatar,
  cover, carousel-image, and video URLs from the current response. Current
  `search-notes` returns Reels identity, canonical URL, author identity, and
  author avatar only, so do not expect it to supplement text, metrics, or
  content media. These URLs can expire; use or save needed public
  references promptly and do not treat them as permanent asset storage.
- For TikTok and Instagram `search-notes`, `search-users`,
  `get-user-posted-notes`, and
  `get-note-comments`, pass the returned `data.page.next_cursor` unchanged with
  `--cursor` to fetch one next page. Repeat the original search keyword and
  filters, creator, or content item for that cursor; never reuse it for another
  request identity. Never parse the opaque cursor or hide multi-page fanout.
  TikTok cursors created before Skill `0.1.92` and Instagram search cursors
  created before Skill `0.1.95` are invalid: discard them and restart from the first
  page. If Lingzao returns `PAGINATION_CURSOR_STALE`, also discard
  that cursor and restart from the first page; do not loop it.
- Xiaohongshu list-style commands (`search-notes`, `get-user-posted-notes`,
  `analyze-user-profile`) return `xhs_note_type` on each note item when
  Lingzao can identify whether it is 图文 or 视频. When continuing from one of
  those note items to `get-note-detail`, pass the returned value directly as
  `--xhs-note-type`; do not infer the type from the URL. If a Xiaohongshu note
  item has no `xhs_note_type`, use its canonical URL, `/discovery/item/` URL,
  note_id, or short link directly. Content, metrics, and copy need no type;
  request `--xhs-note-type video` only when playback or duration is needed. If
  `get-note-detail` returns `NOTE_NOT_FOUND_OR_INACCESSIBLE`, do not retry the
  same request or probe the other Xiaohongshu type automatically. Ask the user
  to confirm the note is public or provide the original share link.
  `get-note-comments` can still be called without this type.
- Missing search filters use the documented defaults without asking; state the
  defaults used in the reply.

After a successful research command, tell the user the estimated time saved
shown in the CLI Markdown output. If you called multiple Lingzao research
commands for one user request, summarize the total once. Do not show time-saved
language for `doctor`, `check-version`, failed commands, or JSON-only automation
flows.

## Commands

### Search Notes

```bash
~/.lingzao/bin/lingzao search-notes --platform xhs --keyword "AI写作"
~/.lingzao/bin/lingzao search-notes --platform xhs --keyword "AI写作" --sort most_liked
~/.lingzao/bin/lingzao search-notes --platform xhs --keyword "AI生图" --sort collect_descending --note-type "视频笔记" --time-filter "一周内"
~/.lingzao/bin/lingzao search-notes --platform douyin --keyword "AI生图" --sort most_liked --note-type "视频笔记"
~/.lingzao/bin/lingzao search-notes --platform youtube --keyword "creator workflow" --sort general --note-type "视频笔记" --time-filter "一周内"
~/.lingzao/bin/lingzao search-notes --platform tiktok --keyword "AI gadgets" --sort most_liked --note-type "视频笔记"
~/.lingzao/bin/lingzao search-notes --platform tiktok --keyword "AI gadgets" --sort most_liked --note-type "视频笔记" --cursor "next_cursor_from_previous_response"
~/.lingzao/bin/lingzao search-notes --platform instagram --keyword "creative coding" --sort general --note-type "视频笔记" --time-filter "不限"
~/.lingzao/bin/lingzao search-notes --platform wechat_channels --keyword "人工智能" --sort general --note-type "视频笔记" --time-filter "一周内"
```

Use this when the user wants public notes around a topic.
When the user has not specified `--sort`, `--note-type`, or `--time-filter`,
use `general`, `不限`, and `不限` and state those defaults in the reply instead
of asking first.
Instagram content search always means Reels search; choose `--note-type 视频笔记`.
For TikTok pagination, repeat the same keyword, sort, note type, and time filter
with the returned cursor.
`search-suggestions` has been retired. For keyword expansion or topic discovery,
use `search-notes` for content ideas or `search-users` for creator discovery.

### Search Creators

```bash
~/.lingzao/bin/lingzao search-users --platform xhs --keyword "母婴博主"
~/.lingzao/bin/lingzao search-users --platform douyin --keyword "AI生图"
~/.lingzao/bin/lingzao search-users --platform youtube --keyword "creator workflow"
~/.lingzao/bin/lingzao search-users --platform tiktok --keyword "tech.bytes"
~/.lingzao/bin/lingzao search-users --platform instagram --keyword "creative coding"
~/.lingzao/bin/lingzao search-users --platform wechat_channels --keyword "央视新闻"
```

Use this when the user wants creators in a topic or niche.
For TikTok pagination, repeat the same keyword with the returned cursor.
When continuing from `search-users` to profile verification, pass the returned
`users[].id` with `--platform xhs --user-id ...`, `--platform douyin --user-id ...`,
`--platform tiktok --user-id ...`, or `--platform instagram --user-id ...`.
For WeChat Channels, reuse the exact finder ID with
`--platform wechat_channels --user-id "v2_...@finder"`.
For YouTube, the returned ID is a
canonical channel ID; reuse it with `--platform youtube --user-id ...` and
treat `handle` as display metadata only.
The output may include RED ID and follower count for screening, but RED ID is
display metadata only. Do not extract Xiaohongshu RED ID values from bios or
build `/user/profile/<RED ID>` URLs.

### Get Creator Profile

```bash
~/.lingzao/bin/lingzao get-user-info --url "https://www.xiaohongshu.com/user/profile/..."
~/.lingzao/bin/lingzao get-user-info --platform xhs --user-id "63c21e0f000000002801a1bb"
~/.lingzao/bin/lingzao get-user-info --platform douyin --user-id "MS4wLjABAAAA..."
~/.lingzao/bin/lingzao get-user-info --platform youtube --user-id "UC..."
~/.lingzao/bin/lingzao get-user-info --url "https://www.tiktok.com/@creator"
~/.lingzao/bin/lingzao get-user-info --url "https://www.instagram.com/creator/"
~/.lingzao/bin/lingzao get-user-info --platform wechat_channels --user-id "v2_...@finder"
```

Use this when the user provides a creator profile URL or platform user ID and needs full profile-level stats. For Douyin bare user IDs, use the profile `sec_user_id`. For YouTube, use a channel ID or `/channel/UC...` URL; if the user only has a handle, call `search-users` first. For basic homepage analysis, prefer `get-user-posted-notes` and avoid calling both commands by default.

### Get Creator Recent Posts

```bash
~/.lingzao/bin/lingzao get-user-posted-notes --url "https://www.xiaohongshu.com/user/profile/..."
~/.lingzao/bin/lingzao get-user-posted-notes --platform xhs --user-id "63c21e0f000000002801a1bb"
~/.lingzao/bin/lingzao get-user-posted-notes --platform douyin --user-id "MS4wLjABAAAA..." --limit 20
~/.lingzao/bin/lingzao get-user-posted-notes --platform youtube --user-id "UC..." --limit 20
~/.lingzao/bin/lingzao get-user-posted-notes --platform tiktok --user-id "<search-users returned id>" --limit 20
~/.lingzao/bin/lingzao get-user-posted-notes --platform tiktok --user-id "<search-users returned id>" --cursor "next_cursor_from_previous_response"
~/.lingzao/bin/lingzao get-user-posted-notes --platform instagram --user-id "<search-users returned id>" --limit 20
~/.lingzao/bin/lingzao get-user-posted-notes --platform instagram --user-id "<search-users returned id>" --cursor "next_cursor_from_previous_response"
~/.lingzao/bin/lingzao get-user-posted-notes --platform wechat_channels --user-id "v2_...@finder" --limit 20
```

Use this when the user wants to understand what a creator has posted recently. Use this by default for basic creator homepage analysis. 每次返回单页最多 20 条公开作品，可能少于 limit；需要更多请原样使用 next_cursor，每次分页独立调用，不保证返回 limit 条。所有平台每次返回上限 20 条，可能更少；旧请求 limit=21–100 按 20 返回，并附 data.notice=limit_clamped 和 data.notice_message；超过 100、非整数或小于 1 返回 400、不扣费。更多请原样传 next_cursor，每页独立 20 积分。 Douyin recent posts accept canonical profile URLs, search-users creator IDs, v.douyin.com short links, and profile share text. Lingzao resolves short links internally; each page still costs 20 credits, with no preceding get-user-info call required. WeChat Channels requires the finder ID returned by `search-users`; profile URLs are not accepted. YouTube reads the Videos list only and does not add a separate Shorts request. If the response has `next_cursor`, reuse it with `--cursor`; for every platform, repeat the same creator identity. If the user asks for full profile-level stats, add `get-user-info`; if the user asks for Xiaohongshu post copy, scripts, captions, or transcript text across recent posts, use `analyze-user-profile` instead. For Douyin transcript text, use `extract-video-copy` on selected video URLs. TikTok, Instagram, YouTube, and WeChat Channels V1 do not support `analyze-user-profile`.

### Analyze Creator Profile

```bash
~/.lingzao/bin/lingzao analyze-user-profile --url "https://www.xiaohongshu.com/user/profile/..." --limit 20
~/.lingzao/bin/lingzao analyze-user-profile --platform xhs --user-id "63c21e0f000000002801a1bb" --limit 40
~/.lingzao/bin/lingzao analyze-user-profile --platform douyin --user-id "MS4wLjABAAAA..." --limit 20
```

Use this when the user wants deeper creator profile data, including post text, covers, commercial signals, and profile-level content signals. For Xiaohongshu, it also includes subtitle/script previews. For Douyin, it does not extract homepage subtitles or transcript text; use `extract-video-copy` on selected video URLs when the user needs spoken copy.
Use `--limit 20` by default. The default Markdown output shows readable subtitle previews when the platform provides them.
Short-window repeats with the same request parameters may reuse the recent successful result. Use `--force-new` only when the user explicitly needs a fresh run, and do not loop it: repeated forced refreshes in the short protection window may be rejected.
If Douyin profile insight sections are temporarily unavailable, the API and CLI can show `partial_data`, `warnings`, or `unavailable_sections`. Explain that homepage works data still returned successfully, and do not treat the missing insight section as proof that there is no data.

Important for Xiaohongshu: the complete profile subtitle/copy Markdown artifact is a top-level response field, not a per-note subtitle URL. Always check:

`data.artifacts.subtitle_markdown.status`
`data.artifacts.subtitle_markdown.url`

Do not search only inside `items[]`. If `data.artifacts.subtitle_markdown.status == "ready"` and `url` exists, download it before deep script or subtitle analysis:

```bash
curl -L "$subtitle_markdown_url" -o /tmp/lingzao-profile-subtitles.md
```

Use the downloaded Markdown file for complete subtitle/copy analysis. Use `--format json` when the user needs the structured fields. JSON includes `data.artifacts.subtitle_markdown.url` for the complete Markdown file when available, and inline `items[].text.subtitle.content/plain_text` are preview-sized to keep the response readable. If the artifact is unavailable, use the inline subtitle fields. For Douyin, expect `data.artifacts.subtitle_markdown.status == "unsupported"` and use the returned profile insights plus selected-video extraction instead.

### Get Post Detail

```bash
~/.lingzao/bin/lingzao get-note-detail --url "https://www.xiaohongshu.com/explore/..." --xhs-note-type image
~/.lingzao/bin/lingzao get-note-detail --url "https://xhslink.cn/o/..."
~/.lingzao/bin/lingzao get-note-detail --platform xhs --note-id "69690331000000001a02266a" --xhs-note-type video
~/.lingzao/bin/lingzao get-note-detail --platform douyin --note-id "7372484715782352169"
~/.lingzao/bin/lingzao get-note-detail --url "https://v.douyin.com/<short-code>"
~/.lingzao/bin/lingzao get-note-detail --url "https://www.youtube.com/watch?v=..." --content-type video
~/.lingzao/bin/lingzao get-note-detail --platform youtube --note-id "..." --content-type short
~/.lingzao/bin/lingzao get-note-detail --url "https://www.youtube.com/shorts/..."
~/.lingzao/bin/lingzao get-note-detail --url "https://www.tiktok.com/@creator/video/7349541381817355521"
~/.lingzao/bin/lingzao get-note-detail --url "https://www.instagram.com/reel/<code>/"
~/.lingzao/bin/lingzao get-note-detail --platform instagram --note-id "<decimal media id>"
~/.lingzao/bin/lingzao get-note-detail --platform wechat_channels --note-id "export/..."
~/.lingzao/bin/lingzao get-note-detail --url "https://weixin.qq.com/sph/..."
```

The `/shorts/` URL form preserves Short type automatically. For a bare ID,
`watch?v=` URL, or `youtu.be/` URL, pass the `content_type` returned by search as
`--content-type video|short`; Lingzao does not guess type from duration.
YouTube channel/profile URLs are not content-detail inputs. Use
`get-user-info` or `get-user-posted-notes`; for `@handle`, `/c/`, or `/user/`
URLs, use `search-users` first to obtain the canonical channel ID.

Use this when the user asks to analyze one public post.
For Douyin, pass a standard post URL, numeric `aweme_id`, or a valid HTTPS
`v.douyin.com/<short-code>` URL directly. Do not open or expand the short link
first. If Lingzao reports that the short-link format is invalid, ask for the
original HTTPS share URL instead of retrying another detail form automatically.
For Xiaohongshu, canonical URLs, `/discovery/item/` URLs, note IDs, and
`xhslink.com`/`xhslink.cn` short links can all omit the type for content, metrics,
and copy. Lingzao identifies the returned type; untyped video details have
`xhs_note_type=video` and `media.video=null`. There is no automatic follow-up.
When playback or duration is needed, query with `--xhs-note-type video`
in a separate query. If the note came from `search-notes`,
`get-user-posted-notes`, or `analyze-user-profile`, reuse that item's
`xhs_note_type` value. If detail returns `NOTE_NOT_FOUND_OR_INACCESSIBLE`,
do not switch `--xhs-note-type` and retry automatically; ask the user to confirm
the note is public or provide the original share link.
For a Xiaohongshu image note, default Markdown shows `正文图片（N 张）` followed
by every ordered body-image link. Use `--format json` for structured
`data.item.media.images`. Public image links may expire; do not describe them
as downloaded, proxied, or permanently stored by Lingzao.

### Get Post Comments

```bash
~/.lingzao/bin/lingzao get-note-comments --url "https://www.xiaohongshu.com/explore/..."
~/.lingzao/bin/lingzao get-note-comments --url "https://www.xiaohongshu.com/explore/..." --sort most_liked
~/.lingzao/bin/lingzao get-note-comments --platform xhs --note-id "69690331000000001a02266a"
~/.lingzao/bin/lingzao get-note-comments --platform douyin --note-id "7372484715782352169"
~/.lingzao/bin/lingzao get-note-comments --url "https://v.douyin.com/<short-code>/"
~/.lingzao/bin/lingzao get-note-comments --platform tiktok --note-id "7349541381817355521" --limit 20
~/.lingzao/bin/lingzao get-note-comments --url "https://www.instagram.com/p/<code>/" --limit 20
~/.lingzao/bin/lingzao get-note-comments --platform instagram --note-id "<shortcode>" --cursor "next_cursor_from_previous_response"
~/.lingzao/bin/lingzao get-note-comments --url "https://www.douyin.com/jingxuan?modal_id=..." --cursor "next_cursor_from_previous_response"
~/.lingzao/bin/lingzao get-note-comments --url "https://youtu.be/..." --sort most_liked --limit 20
~/.lingzao/bin/lingzao get-note-comments --platform wechat_channels --note-id "<numeric object id>" --sort latest --limit 20
```

Use this when the user asks for public comments on one post. The first version returns top-level comments only. Use `--sort most_liked` for Xiaohongshu or YouTube liked-count sorting; Douyin, TikTok, Instagram, and WeChat Channels support only `latest`, with TikTok using service-default order. If the response has `data.page.next_cursor`, pass that opaque value unchanged with `--cursor` to fetch one next page. For TikTok or Instagram, repeat the same content URL or ID; for WeChat Channels, repeat the same numeric object ID; for YouTube, repeat the same `--sort` with every cursor request.
Before calling Xiaohongshu comments, ask whether the user wants latest comments
or liked-count sorting. For Douyin, TikTok, Instagram, and WeChat Channels comments, use only `--sort latest`;
do not pass `--sort most_liked`.

### Get WeChat Official-Account Articles

```bash
~/.lingzao/bin/lingzao get-article-detail --url "https://mp.weixin.qq.com/s/..."
~/.lingzao/bin/lingzao get-article-detail --url "https://mp.weixin.qq.com/s/..." --output /tmp/article.md
~/.lingzao/bin/lingzao get-article-stats --url "https://mp.weixin.qq.com/s/..."
~/.lingzao/bin/lingzao get-related-articles --url "https://mp.weixin.qq.com/s/..."
```

Use these when the user provides a public WeChat official-account article URL
and asks to analyze the article, inspect public engagement metrics, or expand
from that article to related public articles. The first version is URL-only.
An empty related-articles list is a valid response.
Do not use these commands for account article history, account listing, or
multi-page fanout unless Lingzao adds a separate capability.

For full article analysis, prefer `get-article-detail --output /tmp/article.md`.
The command saves the complete article text as a local Markdown file and prints
only the file path plus a short summary in chat. Read the saved Markdown file
for detailed analysis instead of asking the CLI to paste the full article body
into the conversation.

### Extract Short-Video Copy

```bash
~/.lingzao/bin/lingzao extract-video-copy --url "https://www.xiaohongshu.com/explore/..."
~/.lingzao/bin/lingzao extract-video-copy --url "https://v.douyin.com/..."
~/.lingzao/bin/lingzao extract-video-copy --url "https://www.tiktok.com/@creator/video/1234567890123456789"
~/.lingzao/bin/lingzao extract-video-copy --url "https://weixin.qq.com/sph/..."
~/.lingzao/bin/lingzao extract-video-copy --operation-id "<上一次打印的 UUID>" --url "https://v.douyin.com/..."
```

Use this when the user asks for short-video spoken copy, transcript, subtitles, or口播文案.
Xiaohongshu, Douyin, TikTok, and WeChat Channels public video links are supported.
TikTok requires a canonical `/@handle/video/<id>` URL and returns the complete
native WebVTT caption plus plain text when available. It does not fall back to
speech recognition; a missing caption is a terminal no-result. Do not mix TikTok and
other platforms in one batch. For
WeChat Channels, pass the canonical `https://weixin.qq.com/sph/...` share link
directly; do not call detail first or attempt download/decryption.
The CLI prints a stable extraction request ID before submitting. If the response
is ambiguous, interrupted, or not consumed, repeat the same command within 24
hours with `--operation-id <UUID>` and keep every `--url` unchanged. Omit
`--operation-id` for a new extraction intent. Never reuse an old operation ID
with different URLs and do not invent an automatic retry loop.
If one item reports that the video is too large, do not retry that URL. Explain
which item failed, preserve any successful results in the same batch, keep the
CLI-provided failure guidance, and ask for a shorter video link.

### Generate Image

```bash
~/.lingzao/bin/lingzao generate-image --prompt "一张小红书封面图，主题是 AI 生图新手避坑，干净明亮，中文大标题留白" --output /tmp/lingzao-image.png
~/.lingzao/bin/lingzao generate-image --prompt "极简产品海报，白底，柔和阴影" --size 1024x1536 --output /tmp/poster.png
~/.lingzao/bin/lingzao generate-image --prompt "参考两张图，保留人物风格，把产品界面换成灵造首页截图" --size 1536x2048 --image /tmp/style.png --image /tmp/product.png --output /tmp/poster.png
~/.lingzao/bin/lingzao generate-image --prompt "每张参考封面分别改成 AI 工作台主题，替换原人物身份、原文字和品牌" --count 3 --reference-mode one_to_one --image /tmp/top-1.png --image /tmp/top-2.png --image /tmp/top-3.png --size 1024x1536 --output /tmp/poster.png
~/.lingzao/bin/lingzao generate-image --prompt "批量生成 3 张封面草稿" --count 3 --size 1024x1536 --output /tmp/poster.png
~/.lingzao/bin/lingzao generate-image --prompt-file /tmp/lingzao-prompt.txt --output /tmp/poster.png
```

Use this only when the user asks to generate a creator image asset. For normal
research, do not call image generation automatically.

When the user wants N images from the same prompt, call `generate-image` once
with `--count N` for N=2..5. Do not loop the same prompt as multiple
`--count 1` calls. The CLI prints a stable request ID before submitting that
batch. If a POST response is ambiguous or polling is interrupted, the Agent
must save that UUID and repeat the same command with
`--client-request-id <UUID>`; keep the prompt, size, count, output format,
reference mode, and reference images unchanged. Omit `--client-request-id` for
every new generation intent. Do not reuse an old ID for new content and do not
invent another network-retry loop. Multiple intents can queue; a retryable
`GENERATION_IN_PROGRESS` without a `poll_url` means this request was not
accepted. Retry the same ID later and follow the CLI-provided guidance.
If the user wants distinct concepts, vary the prompt
for each concept or use one counted batch for same-prompt variants.
When each reference image should produce its own corresponding output, pass the
references in output order, set `--count` to the same number, and add
`--reference-mode one_to_one`. The CLI rejects mismatched counts before the API
request. One-to-one batches support 1-4 reference images; `count=5` remains
available only for prompt-only or shared-reference generation. Without that
option, repeated `--image` inputs are shared references that jointly influence
every output.

Before calling `generate-image`, run the minimal intake gate. If the user only
says something like "给我做一张某某海报图" or provides only a broad topic, do
not generate immediately. Ask for the two visual anchors first:

1. 你有没有参考图？可以发 1-3 张你喜欢的封面/海报/图文截图。
2. 你有没有想要的配色？比如明亮白底、绿色清爽、黑金高级、蓝色科技感。

If those are still unclear, ask at most one extra route-changing question, such
as the publishing platform/size, exact on-image text, or whether the user wants
people/no people. Only proceed directly without asking when the user already
provided enough constraints: topic + platform/format + visual style/reference
or color + on-image text/material.
Use `--image` for local reference images; repeat it for multiple images. The
Skill uploads those files directly to Lingzao for the current request, so the
user does not need to upload them elsewhere first. Supported reference image
formats are png, jpeg, and webp.
For long, Chinese, or multiline prompts, prefer writing the prompt to a UTF-8
text file and passing `--prompt-file /path/to/prompt.txt`, or pipe the prompt
with `--prompt-stdin`, to avoid shell quoting or command-line encoding issues.

#### Reference Image Handling

For Codex, WorkBuddy, and other agent runtimes:

- `--image` accepts local filesystem paths only. If the user provides a
  reference image through a chat attachment, pasted image, screenshot, or input
  box, first materialize that image as a local file before calling the CLI.
  Preserve the original supported image format when saving the file.
- Use a per-run temporary directory for runtime-provided images, for example
  `/tmp/lingzao-image-inputs/<run-id>/ref-1.png` and
  `/tmp/lingzao-image-inputs/<run-id>/ref-2.png`. Use absolute paths in the CLI
  call.
- If the user already provided a stable local path, such as a file under
  `/Users/...`, you may pass that path directly. If the runtime-provided image
  lives in a temporary attachment path, copy it into the per-run temp directory
  first.
- Do not proactively convert image formats. If the input image is already png,
  jpeg, or webp and its file size is reasonable, pass it as-is. Do not convert
  png to webp or jpeg just because an example path uses a different extension.
- Only when a reference image is larger than 2 MB, create a smaller copy in the
  temp directory and pass that copy with `--image`. Keep the file extension and
  actual image bytes consistent. If resizing or compression fails, use the
  original supported image file instead of trying another format.
- Do not overwrite the user's original image file. Do not store reference
  images in the repo. If the runtime cannot save an uploaded or pasted image to
  a local path, ask the user to save the image locally and provide the path.
- In the prompt, state what should be borrowed from the reference images, such
  as layout, color palette, product shape, character style, or composition. Do
  not say only "reference this image" when a more specific instruction is
  possible.

Example with a runtime-provided reference image:

```bash
mkdir -p /tmp/lingzao-image-inputs/run-001 /tmp/lingzao-image-outputs/run-001
~/.lingzao/bin/lingzao generate-image \
  --prompt "参考这张图的排版和明亮色彩，生成一张小红书封面图，主题是 AI 生图新手避坑，中文大标题留白" \
  --size 1024x1024 \
  --image /tmp/lingzao-image-inputs/run-001/ref-1.png \
  --output /tmp/lingzao-image-outputs/run-001/result.png
```

The command creates a Lingzao async batch and automatically polls the returned
status URL until the background job finishes or the command timeout is reached.
Image generation can take several minutes; `--timeout` can extend waiting for
large or slow batches, but does not shorten the built-in per-image polling
window. For one image, `--output` writes the result to the exact path you
provide. For `--count` greater than 1, `--output /tmp/poster.png` writes every
successful image as numbered files such as `/tmp/poster-1.png`,
`/tmp/poster-2.png`, and so on. Default Markdown output requires `--output` so
generated images are saved locally. If a direct API caller receives
`GENERATION_IN_PROGRESS` with a returned `poll_url`, that active batch belongs
to another intent: poll it only until the concurrency slot is free, then submit
the current request again with its original `client_request_id`. Do not return
the other batch as the current request's result. If no `poll_url` is returned
and the error is retryable, this attempt was not accepted;
wait briefly and retry with the same ID. The CLI automatically waits for a
returned active batch; a rejection without a polling URL exits with the request
ID and retry guidance. Rerun with the same parameters and
`--client-request-id <printed-id>`. Use `--format json` only when you need structured automation
data.

## Usage Notes

- For profile and post URLs, pass the URL directly when possible.
- For direct IDs, include `--platform`. For Xiaohongshu follow-up profile checks,
  prefer the 24-character `users[].id` returned by `search-users`; RED ID is
  display metadata only.
- Omit `--limit` unless the user asks for a specific count.
- Search notes default to comprehensive sorting, all note types, and all time; use `--sort`, `--note-type`, and `--time-filter` when the user asks for ranked or filtered note search.
- Use `--format json` only when another tool needs structured output.
- Default output is Markdown for agents to read and summarize.
- If the API key or account needs attention, ask the user to open the Lingzao dashboard.

### 深度主页翻页

小红书深度分析支持 `full_page=true`：每次一整页，首通常22条含置顶，之后通常20条，忽略 limit，每页固定50积分。不传 full_page 或传 false 时按 limit 返回，后续只需传上一页 `page.next_cursor`，1–20条50积分、21–40条100积分。小红书所有 next_cursor 均为签名 cursor，必须原样回传，不解析、不跨博主或能力混用。两个参数都省略时仅 next_cursor 升级为签名格式，其他数据保持原行为；旧缓存也免费返回签名 cursor。不同 full_page/cursor 不复用，完全同参60分钟内复用且不扣费。抖音暂不支持这两个参数（含 false），传入返回400、不扣费；继续省略参数使用原分析。

CLI：`analyze-user-profile --url <主页URL> --full-page`；续页加 `--cursor <next_cursor>`；按 limit 首次直接用 `--limit 20`（也可加 `--no-full-page`），之后用 `--cursor <next_cursor> --limit 20`。
