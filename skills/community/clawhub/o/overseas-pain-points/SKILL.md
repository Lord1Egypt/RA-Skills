---
name: overseas-pain-points
description: "出海痛点雷达 / Overseas pain points for Chinese sellers. 给一个产品或品类（英文词，如 robot vacuum、portable power station）：先看 Bing 和 YouTube 的英文搜索联想（海外买家在搜什么），再读 YouTube 和 TikTok 上排在前面的评测视频（口播和画面文字），把相同的痛点、需求、购买顾虑归到一起，由代码数出每一条出现在几条视频里（N/M），英文原话逐字保留并附中文；有人在搜、视频都没讲的列成「机会」。用于出海选品、Listing 卖点、差评预判、新品立项。速查 12 条约 41 积分。不要账号、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，¥9.9 支付宝 50 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/chuhai-tongdian?ref=skill-overseas-pain-points
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-overseas-pain-points&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/chuhai-tongdian?ref=skill-overseas-pain-points"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-overseas-pain-points&next=/app/keys"
    required_for: "searching and reading YouTube and TikTok review videos and counting overseas buyers' pain points; sign-up gives 10 free credits, no card"
---

# 出海痛点雷达（YouTube + TikTok）

出海选品时最贵的错，是做了一个海外买家早就在抱怨的东西。这个技能把一个品类在 YouTube、TikTok 上排在前面的评测视频读完（口播 + 画面文字），告诉你海外买家在抱怨什么、看重什么、搜什么，结果用中文写，英文原话逐字保留。

## 一条命令

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-overseas-pain-points&next=/app/keys
python3 {baseDir}/scripts/radar.py "robot vacuum"
```

- 品类词用英文（海外买家搜的词）：`"portable power station"`、`"massage gun"`。
- `--size standard`（24 条）/ `--size deep`（48 条），默认速查 12 条。
- `--preview`：只看英文搜索需求词（1 积分）。
- `--language en`：报告用英文写；默认中文。
- `--weekly`：每周再跑一次，对比变化。`--format json`：结构化结果。
- 一次通常 10–20 分钟，脚本自己等；超时会给出 `--radar-id`。

## 一次返回什么

痛点（`sections.pain`）、需求与卖点（`needs`）、购买顾虑（`blockers`）、被点名的品牌型号（`products`）、没人回答的问题（`open_questions`）、英文搜索需求（`demand`）、机会（`gaps`）、和上次相比的变化（`diff`）。每一条写成 `count_posts`/读到的条数，附 1–3 句英文原话和中文 `gloss`，能点回原视频。

**计数是代码数的**：模型只把说同一件事的原话归组，条数由代码按视频编号去数；原话是引擎在口播或画面文字里逐字找到的（`verified: true`）。中文是翻译，原话以英文为准。

真实运行（2026-11-07，「robot vacuum」速查，11 条在题）：痛点「低矮家具无法进入」3/11（"if it's a small area like a dresser…"）、「毛发缠绕与堵塞」2/11（"it's totally clogged up with hair."）；需求「自动清洗与烘干拖布」4/11；被点名最多的是 Roborock（7/11）和 MOVA（5/11）；机会：海外买家在搜 troubleshooting / problems，读到的评测都没讲。

## agent 怎么用

1. 用户问「美国人买 XX 最在意什么」「这个品类海外差评在哪」「做 XX 出海有什么机会」时跑它。
2. 回答引用 `count_posts/posts` 和英文原话（附中文），给出视频链接（`notes[n-1].url`）。
3. 说明样本：只读了公开搜索排在前面的评测视频；评测视频可能有品牌合作；**不读评论**（YouTube 不对我们的服务器开放评论，我们也不用 Cookie），也不读亚马逊、Reddit。
4. 告诉用户花了多少积分（stderr 最后一行）和分享链接。

## 费用

两次搜索（YouTube、TikTok 各 1 积分）+ 每条视频读取和洞察（每条最多 5 积分，长视频按预算读开头；读过的 0 积分）+ 汇总 3–6 积分。速查约 41 积分。积分不够返回 402、不扣费，附 ¥9.9 买 50 积分（支付宝）的链接。

## 读不到的

评论区、私密或下架的视频、需要登录的内容；亚马逊评论和 Reddit（平台条款不允许，我们不做）。

## 隐私

只把你给的品类词发给 linkdigest.dev，不读任何账号或 Cookie。https://linkdigest.dev/privacy · 出海品类库（每周更新）：https://linkdigest.dev/zh/chuhai-tongdian · support@linkdigest.dev
