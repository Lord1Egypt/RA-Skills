---
name: linkdigest-wechat-article-reader
description: "微信公众号文章提取：把 mp.weixin.qq.com 文章链接读成全文 Markdown，连文章里每张图片上的文字一起 OCR。用户发来公众号文章链接，要全文、要点、图片里的字（长图、截图、表格、海报）、作者和发布日期、文末「阅读原文」和二维码指向的链接时使用。不需要微信登录或 Cookie。通过 LinkDigest API 读取，需要 LINKDIGEST_API_KEY，按量计费：6 张图以内 1 积分（约 ¥0.14），注册送 10 积分。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/docs
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs"}}
---

# 微信公众号文章提取（全文 + 图片文字 OCR）

公众号文章的干货经常不在正文里，而在图里：长图、聊天截图、数据表、海报。普通的网页抓取只能拿到正文文字，图里的内容全丢。这个技能把文章链接交给 LinkDigest，返回：

- 全文正文（不是摘要），公众号名称、作者、发布日期；
- 文章里的每一张图（最多 60 张）：画面描述 + 图上的文字；
- 要点，每条要点附一句能在原文里逐字找到的引用；
- 文章指向的链接：文末「阅读原文」、正文里的网址、图片里的二维码（只列出，不打开；收款码和加群码会标明）；
- 一份「读了多少」的回执（`coverage`）：读了几张图、哪些没读到。

实测（2026-10-06，一篇 16 张图的公众号文章）：正文 4,683 字，16/16 张图读出，3 积分，约 110 秒。

## 触发条件

用户发来 `mp.weixin.qq.com/s/...` 链接，并且要：

- 「把这篇文章转成文字 / Markdown」「提取全文」「总结这篇公众号文章」；
- 「图片里写了什么」「把长图里的字打出来」「表格里的数据」；
- 「这篇文章文末的链接 / 二维码是什么」；
- 把文章存进知识库、做竞品或行业研究的素材。

不要用在：搜索公众号文章、读某个公众号的历史文章列表、读评论和阅读数、需要登录才能看的付费文章。这个技能一次只读一条你给的链接。

## 一次性准备

1. 打开 https://linkdigest.dev/app/keys ，用邮箱或 Google 登录，创建 API Key（`ld_live_` 开头）。新账户送 10 积分，不用绑卡。
2. `export LINKDIGEST_API_KEY=ld_live_...`

Key 只放在环境变量或 OpenClaw 配置（`skills.entries.linkdigest-wechat-article-reader.env`）里，不要贴进对话。

## 怎么调用

```bash
python3 {baseDir}/scripts/linkdigest.py "https://mp.weixin.qq.com/s/xxxxxxxx"
```

| 需要 | 加参数 |
| --- | --- |
| 结构化 JSON（逐图的 `images[]`、`links[]`、`coverage`） | `--format json` |
| 控制花费：最多花 N 积分，超出的图不读 | `--max-credits N` |
| 同时要英文（或其他语言）译文，原文保留 | `--translate-to en` |
| 接着取一个还没跑完的任务 | `--job-id <jobId>` |

脚本只用 Python 标准库，自动处理排队和轮询（长文章可能要 1–2 分钟）。最后一行 stderr 会写这次扣了几个积分、是否命中缓存。退出码：0 成功；3 Key 无效；4 积分不够（未扣费，stderr 里有支付宝付款链接）；5 链接读不了（未扣费）；7 等待超时（用 `--job-id` 接着取）。

没有 Python 时直接调 HTTP：

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/xxxxxxxx", "format": "markdown"}'
# 返回 202 时：curl -sS "https://linkdigest.dev/api/v1/digest/<jobId>?wait=20&format=markdown" -H "Authorization: Bearer $LINKDIGEST_API_KEY"
```

## 把结果交给用户

1. 用户要「全文」：给 `caption`（正文），不要改写；再按顺序给每张图的文字，标「图 1」「图 2」。
2. 用户要「总结」：用 `key_points`。每条要点后面的引用（`key_point_support`）是代码在原文里逐字核对过的，`verified=false` 的那条要提醒用户自己对照。
3. 正文和图上文字来自文章本身；图片描述和要点是模型写的，转述时分清楚。
4. 涉及数字、价格、人名时提醒用户对照原图，小字和手写字可能认错。
5. `coverage.not_captured` 不为空时，把没读到的部分原样告诉用户（比如「第 19–30 张图没读（预算）」）。
6. 告诉用户这次用了几个积分。

## 费用（按量，读不出不收费）

| 文章 | 积分 | 约合 |
| --- | --- | --- |
| 6 张图以内 | 1 | ¥0.14 |
| 7–12 张图 | 2 | ¥0.29 |
| 每多 6 张图 | +1 | +¥0.14 |
| 60 张图（单篇上限） | 10 | ¥1.44 |
| 加译文 | +1 | +¥0.14 |
| 任何人读过的同一篇（缓存） | 0 | 0 |

积分不够读完所有图时，不会报错：先读积分够的前几张（每个积分 6 张），并在结果里写明哪些没读。注册送 10 积分（一次）；加量包 ¥36 = 250 积分，支付宝可付，不过期；Dev 月付 $9 = 每月 500 积分。价格以 https://linkdigest.dev/zh/docs 为准。

## 做不到的

- 已删除、被屏蔽、需要登录或付费才能看的文章（返回 422，不扣费）。
- 文章里的视频和音频目前不转写，只读正文和图片。
- 不搜索文章、不读评论、阅读数和在看数。
- 每个账户每小时最多 60 次调用。

## 隐私

只把你给的链接发到 linkdigest.dev；不需要也不会读取你的微信账号。图片只在处理时临时下载，读完即删。文字结果按链接缓存，同一篇公开文章再读免费，也可能提供给请求同一链接的其他用户，所以不要提交内部或私密链接。`scripts/linkdigest.py` 只读环境变量 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不读写本地文件。详见 https://linkdigest.dev/privacy 。

LinkDigest 由独立开发者维护（GitHub `jcaiagent7143-ui`）。同一个 Key 还能读小红书、抖音、TikTok、YouTube、X 链接，见 `linkdigest-xhs-note-ocr`、`linkdigest-video-transcript`。反馈：support@linkdigest.dev
