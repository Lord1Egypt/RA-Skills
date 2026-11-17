# Copy-Paste Prompt Scope Boundary

Use this playbook when the user asks:

- 怎么问灵造
- 给我一个可以复制的提问
- 帮我找对标账号
- 帮我做一条龙内容
- 帮我做封面/图文/海报
- 帮我复盘这条笔记
- 帮我拆 Brief / 商单
- 帮我全平台分发
- 我想先小范围试试

The goal is to make ordinary users paste a scoped prompt instead of triggering
wide searches, repeated account lookups, or multi-platform generation by
accident.

## Core Rule

Every copy-paste prompt should include:

1. **数量**: start with 3 accounts, 1 note, 1 content package, or 1 platform set.
2. **时间范围**: usually recent 15-30 days for updates; recent 30/90 days for
   high-interaction works.
3. **quality gate**: still updating, recent high-interaction work, track fit,
   stage fit, city/local fit when relevant.
4. **depth boundary**: basic result first; do not open all profiles, all notes,
   full comments, full copy, or transcripts unless the user confirms.
5. **stop condition**: if no strict match exists, say so; do not hard-fill weak
   results.
6. **next step**: after the first result, ask whether to expand to 5 accounts,
   deep breakdown, image generation, or cross-platform packaging.

Do not let users copy vague prompts such as:

- 找一些 AI 博主
- 给我找女性成长对标账号
- 帮我做一张海报
- 帮我全平台同步
- 复盘一下这条笔记

Rewrite them into the scoped templates below.

## Benchmark Account Discovery

Default first round:

> 用灵造帮我找【3 个】小红书对标账号，赛道是【填写赛道】，要求：最近【30 天】还在更新，有至少一条高互动作品。先只给基础结果：主页链接、粉丝量、近期爆款、为什么值得参考。不要深度打开每个账号；方向对了再扩到 5 个。

Follower-range version:

> 用灵造找【1000-5000 粉 / 5000-2 万粉 / 5-15 万粉】之间的【赛道】账号。找不到严格符合的就告诉我“没有严格符合”，不要用 100 粉或几十万粉账号硬凑。

Local-life version:

> 用灵造找【城市 + 赛道】相关账号，比如【南宁 本地生活 探店】。要求最近 30 天有更新，有本地关键词或定位，先给 3 个，不要直接搜“本地生活”这种大词；方向对了再扩到 5 个。

Deepen-one-account version:

> 上面这 3 个里面，我只想继续深挖第【1/2/3】个账号。请你再打开它的主页，分析最近内容、封面、标题、爆款和我能学什么；不要同时深挖 3 个。

If the user only gives a broad keyword, first narrow:

> 先不要做在线查询，先帮我判断这个赛道应该找什么类型的对标账号。请帮我限定【粉丝量范围、内容形式、城市/是否本地、更新时间、近期爆款要求、首轮搜索数量】，再决定要不要搜索。

## Own Account Diagnosis

Homepage-first version:

> 用灵造分析我的小红书主页，先做基础诊断，不要深度打开全部笔记。重点看：头像昵称、简介、置顶、最近封面标题、内容主线和别人会不会关注。

Recent-content version:

> 用灵造分析我最近【10 条 / 20 条】笔记，判断我的内容主线是否清楚，哪些标题和封面拖后腿，下一条应该先改哪里；先不要打开评论区或额外找对标。

Peer comparison version:

> 用灵造把我的账号和【3 个】同赛道、同阶段账号横向对比。请先只找 3 个，不要找 10 个；对比封面、标题、选题、主页记忆点和内容主线。

When public notes are fewer than 10, downgrade the output to a light diagnosis:

- 0 notes: starter setup and homepage positioning.
- 1-2 notes: homepage first impression and single-note feedback.
- 3-5 notes: beginner mini diagnosis.
- 6-9 notes: light account analysis.
- 10+ notes: standard account diagnosis.
- 20+ notes: standard report.
- 40+ notes: deep diagnosis or distillation after confirmation.

## One Account Breakdown

Learning-value version:

> 用灵造拆这个账号为什么值得学习。先看主页和最近【10-20 条】内容，重点判断：是否还在更新、有没有近期爆款、账号人设、内容主线、哪些能学、哪些不能学；不要默认打开全部评论区。

User-fit version:

> 这个账号适合我模仿吗？请结合我的账号阶段判断，不要只说它哪里好。重点告诉我：我能学标题、封面、选题、表达方式，还是只能当灵感参考；如果它靠脸、资源、城市、团队或大号基础，请直接说不能硬学。

## Single Note / Video Breakdown

Graphic-note version:

> 用灵造完整拆这条图文笔记：标题点击点、封面关键词、每一页结构、正文、评论区需求、为什么爆、我能怎么改成自己的赛道版本；评论区先看 1 页一级评论即可。

Spoken-video version:

> 用灵造拆这条口播视频：前 3 秒、开头钩子、逐字稿结构、节奏、关键词、评论区需求，以及我能不能用同样结构重写一条；如果要提取完整逐字稿，请先提醒我会增加查看范围。

Vlog/storyboard version:

> 如果这是 Vlog，请帮我拆成分镜：先按【前 3 秒、前 10 秒、主体 3-5 个镜头、结尾】拆，每个镜头写画面重点、转场、字幕、情绪推进、为什么让人看完。

## Keyword To One-Stop Content Package

Minimal package:

> 用灵造根据【关键词】先做一个最小可用的小红书内容包：1 个首推选题、3 个标题、封面大字、4-7 页图文内容、正文、10 个关键词和置顶评论。先不要搜索太多参考。

Reference-led package:

> 我给你【1 个链接 / 1-3 张截图 / 1 篇参考内容】，请先拆它的结构，再改成我的账号能发的版本。输出：标题、封面、4-7 页图文、300 字正文、10 个关键词和发布前检查。

Spoken package:

> 用灵造把这个选题做成【1 条】口播内容：标题、前 3 秒开头、600 字左右逐字稿、300 字小红书文案区、10 个关键词。先不要一次生成多条。

If the keyword is broad, first split into 3 selectable directions before
searching or generating.

## Cover And Image Generation

Reference-image version:

> 用灵造参考这张图做一张小红书封面。主题是【主题】，配色想要【配色】，风格参考它的【排版/字体/色调/人物姿势/知识卡片结构】，但内容要换成我的。

No-reference version:

> 我没有参考图。请先帮我选一种适合【赛道】的封面风格：无人物知识卡片 / 人物大字标题 / 互动帖 / 长文截图式 / 本地生活美食图。先给我 3 个方向，不要直接生图。

Before generating an image, always confirm:

- size/platform: Xiaohongshu 3:4, WeChat cover, square, horizontal, etc.
- people/no people
- color direction
- exact cover text
- whether reference images are enough
- which part of the reference image to learn: layout, font, color, pose, or
  composition

If information is missing, ask for it instead of generating a generic image.

## Title, Keywords, And Pre-Publish Check

Title version:

> 用灵造帮我给这篇内容起【3 个】最强标题，不要给 10 个。每个标题请说明：关键词是什么、点击点是什么、适合谁点、是否适合我的账号阶段。

Keyword version:

> 用灵造给我配【10 个】小红书发布关键词，要求区分：核心关键词、行业词、大众词、场景词。不要超过 10 个，并标出最重要的前 3 个。

Pre-publish version:

> 用灵造做发布前检查：只看我发来的这条内容，不额外搜索。请检查标题、封面、前三行、正文、10 个关键词有没有自然埋进去；如果不自然，请直接帮我改。

## Post-Publish Review

Data-review version:

> 用灵造复盘我这条笔记的 24 小时数据。我会发：笔记链接、封面截图、正文/脚本、后台截图。请判断点击、完播/读完、收藏、评论和涨粉问题。

High-like-no-follow version:

> 这条笔记点赞高但不涨粉，请帮我判断：它是不是和账号主线不一致？评论区是真需求还是泛情绪？下一条应该怎么接；评论区先看 1 页即可，不要连续翻页。

Missing-data version:

> 如果我的后台截图信息不够，请先告诉我还缺哪张截图或哪条链接，不要直接下结论。

## Brief And Sponsored Content

Brief version:

> 用灵造拆这个品牌 Brief。先判断：品牌目标、必须讲的卖点、不能乱说的话、适合图文/口播/Vlog 哪种形式。确认后再出标题、封面和正文。

Soft-ad version:

> 这个商单怎么写才不像硬广？请先给【3 个内容角度】，每个角度说明适合图文/口播/Vlog 哪种形式；再帮我选最适合我账号的一条，不要直接写 10 个方案。

If references are needed, start with up to 3 recent references, not a broad
market scan.

## Cross-Platform Distribution

Basic distribution:

> 用灵造把这篇内容做成基础分发包：小红书、朋友圈、公众号。先不要扩展到所有平台，等我确认后再做知识星球、X、播客、B 站或视频号。

Platform rewrite:

> 请把这条内容拆成多个平台版本，但先只做【小红书、朋友圈、公众号】3 个基础版本；每个平台只保留适合它的表达方式，不要简单复制粘贴。

Do not generate every platform at once unless the user explicitly confirms the
scope.

## Unknown Task

When the user is unsure how to ask:

> 我想用灵造完成【任务】，但我不确定怎么限定范围。请你先帮我把任务拆成：本地判断、基础搜索、深度搜索三步，并告诉我第一步应该先做什么。

Then answer with:

1. local judgment: no online lookup yet;
2. basic search: limited known objects or 3-account starter round;
3. deep search: only after user confirms object count, time range, comments,
   full copy, transcript, or image generation scope.
