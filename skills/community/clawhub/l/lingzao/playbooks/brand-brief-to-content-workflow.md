# Brand Brief To Creator Content Workflow

Use this playbook when a user sends an advertising, brand cooperation,
campaign, product, or content brief and wants Lingzao to turn it into
self-media content.

This workflow is for creator-facing content, especially Xiaohongshu. It can also
feed cross-platform packages after the core Xiaohongshu angle is clear.

## Trigger Phrases

Route here when the user says things like:

- 帮我拆一下这个 Brief
- 品牌 Brief 发来了，我应该怎么做内容
- 这个商单怎么写小红书
- Brief 进去后帮我出选题 / 标题 / 封面 / 正文
- 根据这个品牌合作要求给我出内容方案
- 这个广告怎么不硬广
- 先看 Brief，再帮我找对标怎么讲
- 品牌想推这个产品，最近小红书都怎么说

If the user only asks whether an account can monetize, use
`monetization-path-judgment-library.md`. If the user already has a finished
draft and only needs a pre-publish check, use `pre-publish-readiness-check.md`.
If the user only gives a keyword without brand constraints, use
`keyword-to-publishable-content-package.md`.

## Core Principle

Do not turn a Brief into a hard ad.

A good Brand Brief workflow connects three things:

1. what the brand wants to say
2. what the creator can credibly say
3. what the platform user would actually click, save, comment on, or trust

The output should feel like:

品牌要求没有丢，小红书用户也不会一眼觉得这是广告模板。

## Privacy And Scope Boundary

Briefs can contain private business information. Before public-content lookup,
do not paste confidential terms, confidential prices, launch dates, private contact
information, or unreleased product details into searches.

Use safe search terms:

- product category
- user pain
- scenario
- competing public keywords
- public brand/product name only if the user clearly allows it

If the Brief includes high-risk claims, regulated categories, or sensitive
instructions, keep the output conservative and remind the user to confirm with
the brand/legal reviewer.

High-risk categories include:

- medical, health, supplements, weight loss, skincare efficacy
- finance, investment, insurance, income promises
- parenting, baby products, education outcomes
- luxury authenticity, food safety, privacy, employment claims

Do not invent proof, test results, awards, official endorsements, before/after
effects, prices, discounts, or user reviews that are not provided.

For Xiaohongshu deliverables, also run
`xhs-platform-management-risk-baseline.md` and
`xhs-content-compliance-risk-gate.md` before final copy. If the Brief asks for
external links, QR codes, WeChat, private groups, comment-to-receive resources,
or "like/follow/comment to get" mechanics, keep those as Brief requirements to
confirm, but do not put them into the publishable Xiaohongshu version. Rewrite
them into a safer platform-specific alternative or mark them as needing brand
confirmation.

For Brand Briefs, default to "公开价值优先、产品名后置、无导流动作". The content
should not start as a brand slogan. Translate the product into a user problem,
scene, checklist, comparison, story, or method first, then let the product
appear as support.

## Input Contract

Minimum useful input:

- the Brief text, screenshot, document, or a pasted summary
- target platform, default Xiaohongshu if not provided
- creator/account direction if this is for a specific creator

Helpful optional input:

- profile link or recent posts of the creator
- product page, brand page, or official reference material
- required selling points
- forbidden words and compliance notes
- deliverables: graphic note, spoken video, Vlog, article, multi-platform
- required keywords, hashtags, CTA, coupon, landing page, or comment guidance
- desired tone and reference examples
- deadline and brand review rounds

If the user only gives a screenshot or short sentence, do a light Brief intake
first and ask only for missing route-changing fields, such as platform, format,
required selling point, or account direction.

## Workflow

### 1. Brief Intake

Extract the Brief into a structured table:

| Layer | What To Extract |
| --- | --- |
| Brand / product | what is being promoted |
| Campaign goal | awareness, seeding, conversion, trial, store visit, app download, course signup, lead generation |
| Target user | who should care and who should not be targeted |
| Product value | features, benefits, proof points, price, scenario, differentiator |
| Mandatory points | required wording, keywords, scenes, CTA, links, tags |
| Forbidden zone | banned claims, sensitive terms, must-not-say, competitor limits |
| Deliverables | platform, format, duration/pages/word count, number of posts, timeline |
| Brand tone | premium, friendly, professional, playful, local, practical, emotional |
| Creator fit | why this creator can say it credibly |
| Missing info | what must be clarified before final delivery |

When extracting mandatory CTA, separate:

- Brand requested CTA
- Xiaohongshu-safe CTA
- Needs brand/legal confirmation

If the Brief is too vague, do not block the workflow. Produce a "Brief
clarification list" with 3-5 missing items and a draft direction based on what
is already known.

### 2. Creator And Audience Fit

Before selecting topics, judge whether this ad can sit inside the user's account.

Check:

- Does the product match the account's audience?
- Will it attract the desired customer or only random views?
- Is the creator's usual content format able to hold the product?
- Will this damage trust if pushed too hard?
- Can the product be shown as a useful tool, scenario, story, checklist,
  transformation, comparison, tutorial, review, or life detail?

Good diagnosis:

这个 Brief 不能直接按品牌卖点写。它要先变成你账号用户关心的问题，再把产品放进去解决那个问题。

### 3. Public Reference Search

Use `research-scope-guard.md` before expanding online lookup.

Search should not only search the brand name. Search a mix of:

- product category
- user pain
- use scenario
- desired outcome
- audience identity
- competitor/public category wording
- platform-specific content format, such as "测评", "避坑", "清单", "教程",
  "通勤", "新手", "办公室", "妈妈", "自媒体", "AI工具", "本地生活"

Default first round:

- 3-5 keywords
- recent public notes when the category changes fast
- prioritize Xiaohongshu unless the user names another platform
- select 3-5 reference notes or accounts, not a long list

For each selected reference, capture:

- title and direct link
- public signal: likes, saves, comments, publish time when available
- content type: review, tutorial, Vlog, list, comparison, story, problem-solve
- why users click
- how the product/category is embedded
- what can be borrowed
- what not to copy

Do not claim to have read comments or full copy unless those details were
actually opened.

### 4. Topic And Angle Matrix

Turn the Brief into content angles before writing.

Recommended angle types:

| Angle | Use When | Example Shape |
| --- | --- | --- |
| Pain-first | user already has a clear problem | "为什么你总是..." |
| Scenario-first | product solves a daily scene | "上班/旅行/带娃/做账号时..." |
| Result-first | product creates a visible result | "我用它把..." |
| Tutorial | product has steps or workflow | "3 步完成..." |
| Comparison | category has alternatives | "A 和 B 到底差在哪" |
| Checklist | user saves for later | "新手先看这 5 点" |
| Story/Vlog | creator identity is strong | "我为什么开始..." |
| Myth-busting | market has misunderstanding | "很多人以为...其实..." |
| Local/life scene | city/store/food/travel category | "第一次来...怎么选" |

Rank angles by:

- user click reason
- brand message fit
- creator credibility
- production difficulty
- compliance risk
- save/comment potential
- whether it can become a series

Default output should recommend Top 3 angles, with one首推.

### 5. Content Package

After the angle is selected, produce the actual deliverable.

For Xiaohongshu graphic note:

- 3 title options, not 10
- cover copy and cover type
- 4-7 page structure
- page-by-page copy direction
- 300-character body copy
- 10 publishing keywords
- CTA/comment guidance
- brand-mandatory-point checklist

For spoken video:

- 3 title options
- first 3 seconds hook
- 60-120 second spoken script or the requested length
- screen/subtitle emphasis
- product placement point
- body caption
- 10 publishing keywords

For Vlog:

- storyboard by scene
- where the product appears naturally
- narration outline
- caption
- cover direction
- 10 publishing keywords

For cross-platform:

- first finish the Xiaohongshu core angle
- then route to `mother-content-cross-platform-distribution.md` for WeChat
  public account, Moments, Knowledge Planet, Bilibili, Douyin, X, or podcast

### 6. Brand Delivery Check

Before final answer, include a delivery checklist:

- mandatory points included
- forbidden claims avoided
- public value appears before product/brand selling language
- Xiaohongshu risk gate passed or risky CTA rewritten
- platform disclosure/compliance reviewed
- product placement is natural
- title and cover still have user click reason
- first 3 lines / first 3 seconds do not sound like a brand slogan
- CTA matches the Brief as much as possible without站外引流、加微信、诱导评论互动
- missing brand assets or facts to confirm

If the Brief conflicts with creator trust, say so plainly:

这条可以做，但不能按 Brief 原话硬写。原话更像品牌自夸，用户会滑走。我建议保留品牌必须表达的点，但把开头改成用户痛点/场景，再把产品放在解决方案里。

## Output Forms

### Light Brief Breakdown

Use when the user only asks "帮我看看这个 Brief":

1. Brief 摘要
2. 这单适不适合这个账号
3. 用户会关心的入口
4. 3 个可做选题
5. 需要向品牌确认的问题
6. 是否需要继续搜索对标

### Standard Brief To Content Package

Use when the user wants actual content:

1. Brief 拆解表
2. 账号/受众适配判断
3. 搜索范围和对标选择
4. Top 3 内容角度
5. 首推角度的完整小红书内容包
6. 品牌交付检查表
7. 下一步：发给品牌前检查标题/封面/正文，或生成图片

### Deep Campaign Package

Use when the user asks for a campaign, batch content, or multi-platform plan:

1. campaign goal and user journey
2. keyword/search plan
3. benchmark notes/accounts
4. 5-10 topic pool
5. 3 complete deliverables
6. multi-platform distribution plan
7. review workflow and post-publish metrics

## Research Scope Wording

If public lookup is needed, use this wording:

我可以先基于 Brief 做本地拆解；如果你想让我看最近小红书同类产品/同类痛点都怎么讲，我会进入公开内容搜索。建议先搜 3-5 个关键词，找 3-5 条近期参考，再产出内容角度和正文。你确认后我再开始查。

If the user already asks for "找对标" or "看看最近都怎么讲", proceed after
the normal scope confirmation.

## Good Style

Use human, practical language:

- 这不是把 Brief 翻译成小红书，而是把品牌卖点翻译成用户愿意看的内容入口。
- 品牌要的是卖点完整，用户要的是跟自己有关。我们要在中间搭桥。
- 这条广告不能从品牌口号开始，要从用户正在发生的场景开始。
- 先别急着写正文，先判断这个产品应该进入用户的哪一个问题。

Avoid:

- pure slogan copy
- fake personal experience
- unsupported claims
- claiming a product is best/official/guaranteed without evidence
- copying reference notes
- hiding that a post is commercial when disclosure is required
