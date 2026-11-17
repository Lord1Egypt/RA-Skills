# Lingzao Weekly Content Motherpack Distributor

Use this playbook when the user wants Lingzao to turn one week of creator
materials into a weekly content update package, weekly mother-topic package, or
next-week publishing plan.

Trigger phrases:

- 每周内容更新包
- 每周内容母题包
- 周更内容包
- 整理这一周内容
- 下周发什么
- 这一周可以沉淀成什么内容
- 帮我做 5 个母题
- 把最近素材做成小红书 / 公众号 / 播客分发
- weekly content pack
- weekly motherpack

## Core Principle

Do not turn every idea into content. First compress the week into a small set
of mother topics, then distribute only the strongest topics to the platforms
that fit them.

Good user-facing wording:

> 我会先把这一周素材压成 5 个母题，不会把每个灵感都发出去。弱的先放债务池，强的再分发到小红书、公众号、播客和短口播。

Default behavior:

1. First run: use the last 7 days unless the user names another range.
2. Scheduled run: use materials since the previous weekly pack.
3. Calendar-week request: use the named week and show the exact date range.
4. Default to 5 mother topics. If only 2-3 topics are strong, say that clearly
   and put weak ideas into the debt pool instead of padding.
5. Start from materials the user provided or explicitly authorized. Do not
   pretend to read private chats, folders, screenshots, or knowledge bases that
   were not supplied or reachable.

## Inputs Lingzao Can Accept

Use any available user-provided material:

- conversations with the creator or users
- local notes, drafts, screenshots, or links
- podcast transcripts, meeting notes, voice notes, or course outlines
- published note links, backend screenshots, comments, or review results
- saved viral notes, benchmark creators, keyword research, or content-library
  material
- product updates, customer feedback, Briefs, or feature notes
- unfinished ideas the user keeps repeating

If the user gives a folder or multiple files, first make a compact source map:

| Source | Signal | Possible Mother Topic | Fit |
| --- | --- | --- | --- |
| source name or path | recurring point / strong case / user pain | topic candidate | XHS / WeChat / podcast / debt pool |

## Mother Topic Selection

Choose mother topics by these signals:

- repeated user pain or creator bottleneck
- strong story, case, screenshot, or data point
- a reusable method, SOP, checklist, or judgment standard
- platform fit: visual, searchable, saveable, emotional, or explainable
- product fit: shows Lingzao's workflow, judgment, image ability, or content
  operation value without sounding like hard selling
- public/private boundary: can be published without exposing private details
- next-step value: can lead to a draft, image pack, review, or experiment

Reject or park ideas when:

- the point is only interesting to the user privately
- the content needs proof the user does not have
- it is only a temporary emotion with no reusable angle
- it risks Xiaohongshu diversion, exaggerated claims, sensitive unsupported
  claims, or comment-gated resources
- it is too similar to a topic already selected this week

## Mother Content Object

For each selected topic, create a concise object before platform adaptation:

- 母题名称
- 一句话判断
- 目标读者
- 用户痛点 / 点击理由
- 核心观点
- 证据 / 案例 / 细节来源
- 可讲故事
- 可做方法
- 可做图片
- 灵造在其中的角色: diagnosis, search, breakdown, image generation,
  packaging, review, or knowledge-base distillation
- 不适合说什么
- 公私边界
- 风险点
- 推荐优先平台
- 暂缓平台

## Platform Distribution

After selecting mother topics, distribute only the platform versions that make
sense. Do not force every topic onto every platform.

### Xiaohongshu

Use when the topic is visual, clickable, saveable, emotional, searchable, or
can become a graphic-note/image package.

Output:

- 适合形式: graphic note, spoken video, Vlog storyboard, text-dense screenshot
  note, interaction post, cover/image showcase, or account-operation post
- 标题 3 个
- 封面主标题
- 封面副标题 / 画面关键词
- 4-7 页图文结构 or 口播结构
- 正文区 300 字左右
- 10 个发布关键词
- 置顶内容 / 评论区安全引导
- 发布前检查点

Before returning final Xiaohongshu-facing copy, run:

- `xhs-platform-management-risk-baseline.md`
- `xhs-content-compliance-risk-gate.md`

Do not include off-platform diversion, WeChat/private-contact guidance,
incentivized comment interaction, exaggerated guarantees, or unsupported
sensitive claims in Xiaohongshu titles, cover copy, page text, body copy,
keywords, scripts, pinned comments, or comment guidance.

If the topic needs images, route to:

- `visual-generation-and-cover-workflow.md`
- `reference-image-graphic-note-workflow.md`
- `image-generation-execution-workflow.md`

Mark the topic as `needs images` if the text package is ready but images were
not generated.

### WeChat Public Account

Use when the topic needs complete logic, case context, process explanation, or
a more durable public article.

Output:

- 公众号标题 3 个
- 文章开头
- 正文结构
- 正文草稿 or detailed outline
- 封面标题方向
- 正文配图方向
- 结尾轻转化 / 下次阅读引导

When the user asks for WeChat images, create a separate image pack. Do not put
WeChat article images into a Xiaohongshu final-image folder.

### Podcast / Long Spoken Draft

Use only for larger issues, not small tactics.

Output:

- 播客标题
- 一句话主张
- 3-5 段结构
- 开场独白
- 关键故事 / 例子
- 结尾问题

Podcast titles should not blindly use Xiaohongshu click-title logic.

### Short Script / Social Clip

Use when the topic can become a short spoken video, Douyin/video-account
script, or quick public explanation.

Output:

- 前 3 秒开场
- 60 秒口播结构
- 逐字稿 if requested
- 封面文字
- 简介 / caption

### Moments / Community / Knowledge Planet

Use when the topic is more human, member-facing, or trust-building.

Output:

- 朋友圈短文
- 更口语版
- 星球帖 / 社群帖
- 可给用户的作业
- 下一步动作

### Knowledge Base / SOP

Use when the topic is reusable.

Output:

- 知识库标题
- 适用场景
- SOP
- 判断标准
- 可复用模板
- 更新规则

Use `content-knowledge-base-workflow.md` when the user asks to save, organize,
or reuse the output later.

## Delivery Folder Contract

When the user asks for files, folders, Word, webpage, or knowledge-base
packaging, do not leave the result as a wall of chat text. Use clear folders
and statuses.

Suggested structure:

```text
weekly-content-pack/
  release-page.html
  release-page.md
  rednote-graphic-pack/
    YYYY-MM-DD-topic/
      images/
      caption.md
      caption.txt
      image-plan.md
  wechat-article-pack/
    YYYY-MM-DD-topic/
      article.md
      cover-direction.md
      images/
  podcast-to-send/
    YYYY-MM-DD-topic.md
  short-script-pack/
    YYYY-MM-DD-topic.md
  knowledge-base/
    YYYY-MM-DD-topic.md
```

Status labels:

- `idea`
- `draft`
- `needs images`
- `in review`
- `ready`
- `blocked`
- `skipped`

For dense outputs, route to `retention-and-follow-up-loop.md` and offer:

- Word document
- HTML / webpage preview
- knowledge-base-ready Markdown

## Output Template

Use this structure by default:

```markdown
## Weekly Range

- 范围:
- 素材来源:
- 本周判断:

## Five Mother Topics

| Rank | Mother Topic | Why It Matters | Best Platform | Status |
| --- | --- | --- | --- | --- |

## Distribution Plan

| Mother Topic | Xiaohongshu | WeChat | Podcast/Script | Knowledge Base | Next Action |
| --- | --- | --- | --- | --- | --- |

## Topic Packages

### 1. Topic Name

- 一句话判断:
- 目标读者:
- 点击/收藏理由:
- 核心内容:
- 推荐平台:
- 暂不建议:
- 风险:
- 下一步:

## Delivery Checklist

- [ ] 小红书标题/封面/正文/关键词
- [ ] 公众号结构或正文
- [ ] 播客/口播草稿
- [ ] 图片包 or image-plan
- [ ] 合规检查
- [ ] 文件夹/Word/HTML/知识库包装

## Debt Pool

- 暂缓主题:
- 暂缓原因:
- 需要补什么:

## Next Week Review Loop

- 本周发布后要回收的数据:
- 下周优先复盘:
- 下次母题判断依据:
```

## Online Capability Boundary

Local playbook work:

- user-provided materials
- topic selection
- platform fit judgment
- draft restructuring
- packaging into Word / HTML / Markdown structure
- review checklist

Lingzao online capability may be needed for:

- searching Xiaohongshu, Douyin, or WeChat public content
- opening public note/article details or comments
- extracting short-video transcripts
- creator/account research
- image generation

Before online work, confirm:

- search topic
- quantity
- time range
- quality gate
- planned external actions
- first-pass stop point

Default first pass should be small. For example: 3-5 references, one image
direction, or one platform package before expanding.

## Boundaries

- Do not automatically publish.
- Do not promise viral growth, guaranteed conversion, guaranteed followers, or
  platform approval.
- Do not copy another creator's identifiable wording, story, visual identity,
  or private material.
- Do not expose private paths, internal thread IDs, credentials, or user
  secrets in public-facing output.
- Keep final editorial judgment with the user.
