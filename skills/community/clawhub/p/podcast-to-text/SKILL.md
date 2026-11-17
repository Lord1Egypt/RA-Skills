---
name: podcast-to-text
description: "播客转文字 / Podcast to text：小宇宙、Apple Podcasts 单集链接 → 带时间的逐字稿、节目简介（shownotes）、要点（每条附逐字核对过的原文）、播放和评论数、小宇宙页面上的热评。用户发来 xiaoyuzhoufm.com/episode/… 或 podcasts.apple.com/…?i=… 链接，要整理播客笔记、提取金句、做摘要、找某段说了什么时使用。只读声音：每开始的 2 分钟 1 积分，不收基础积分，45 分钟一集 23 积分；读过的单集再读 0 积分，读不出来不扣费。不登录小宇宙或 Apple 账号。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.0
homepage: https://linkdigest.dev/platforms?ref=skill-podcast-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-podcast-to-text&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/platforms?ref=skill-podcast-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-podcast-to-text&next=/app/keys"
    required_for: "transcribing podcast episodes; sign-up gives 10 free credits, no card"
---

# 播客转文字（小宇宙 · Apple Podcasts）

一集一两个小时的播客，agent 自己打不开、也听不了。这个技能把单集链接交给 LinkDigest：读公开的单集页面和音频，转成带时间的逐字稿，再给要点和节目简介。

## 一条命令

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-podcast-to-text&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py "https://www.xiaoyuzhoufm.com/episode/XXXXXXXXXXXXXXXXXXXXXXXX"
```

- 长单集第一次会先返回一个任务号，脚本自己等着取结果（默认最多等 15 分钟）。
- `--format json` 拿结构化结果：`transcript`（`{t, text}`，t 是秒）、`caption`（节目简介）、`key_points`、`key_point_support`、`stats`、`comments`。
- `--ask "嘉宾怎么看 XX？"` 就这一集问一个问题，回答附它依据的原话（+1 积分）。
- `--translate-to en` 加一份译文（+1 积分）。

## 支持的链接

| 来源 | 链接长什么样 |
| --- | --- |
| 小宇宙 | `https://www.xiaoyuzhoufm.com/episode/<24 位 id>`（App 里 分享 → 复制链接，带 `?s=` 也行） |
| Apple Podcasts | `https://podcasts.apple.com/<地区>/podcast/<名字>/id<数字>?i=<数字>`（要带 `?i=`，那是单集） |

Spotify 不支持：不登录只给 30 秒试听。很多节目同时在小宇宙或 Apple Podcasts 上，贴那边的链接。喜马拉雅暂不支持。

## agent 怎么用

1. 用户贴单集链接、问「这期讲了什么」「帮我整理笔记」「找出嘉宾说 XX 的那段」时，跑脚本。
2. 引用原话只用 `key_point_support` 里 `verified: true` 的；需要定位时给出 `transcript` 的时间。
3. 告诉用户这次花了多少积分（stderr 最后一行）。

## 费用

只读声音，不抽帧：每开始的 2 分钟 1 积分，不收基础积分。30 分钟 15 积分，45 分钟 23 积分，1 小时 30 积分。读过的单集再读 0 积分；付费单集、读不出来的不扣费。积分不够时返回 402、不扣费，返回体里有付款链接：¥9.9 买 50 积分、¥36 买 250 积分（支付宝），一次性、不订阅、不过期。免费账号单集最长 60 分钟，付费账号 2 小时。

## 隐私

只把你给的链接发给 linkdigest.dev，不用任何小宇宙、Apple 账号；音频读完即删，只留文字结果。https://linkdigest.dev/privacy · 远程 MCP：`https://linkdigest.dev/mcp`（`digest_url`）· support@linkdigest.dev
