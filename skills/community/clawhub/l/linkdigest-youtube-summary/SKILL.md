---
name: linkdigest-youtube-summary
description: "YouTube 视频总结和字幕提取，带时间戳，可直接译成中文。用户发来 YouTube 链接（youtube.com、youtu.be、Shorts），要中文总结、要点、逐字稿、字幕、画面上的文字，或者想不看视频先知道讲了什么时使用。没有字幕的视频也能读：由模型直接看视频，口播和画面文字一起出。不需要梯子抓字幕、不需要 yt-dlp、不需要 Cookie。通过 LinkDigest API 读取，需要 LINKDIGEST_API_KEY，按分钟计费，注册送 10 积分。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/docs
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs"}}
---

# YouTube 视频总结｜字幕提取（带时间戳，可译中文）

## 一句话

给一条 YouTube 链接，拿回带时间戳的逐字稿、画面上的文字和要点；加一个参数，同时得到中文译文。

```bash
python3 {baseDir}/scripts/linkdigest.py "https://www.youtube.com/watch?v=xxxxxxxxxxx" --translate-to zh-CN
```

## 为什么不直接用 yt-dlp 抓字幕

- 服务器和很多云主机的地址会被 YouTube 拦下（`Sign in to confirm you're not a bot`），本地能跑的脚本一上云就失效。
- 很多视频没有字幕，或者只有质量很差的自动字幕。
- 字幕里没有画面内容：幻灯片上的字、代码、图表标题都拿不到。

这个技能走的是另一条路：模型直接把视频看一遍，口播和画面上的文字一起读出来，所以没有字幕的视频也能用。代价是按视频时长收费，见下面的费用表；只想免费抓现成字幕、而且你本机能访问 YouTube 的话，用 yt-dlp 类技能更划算。

## 适合的场景

| 用户说 | 做法 |
| --- | --- |
| 「帮我总结这个 YouTube 视频」「这个视频讲了什么」 | 默认调用，用 `key_points` 回答 |
| 「要中文字幕 / 中文逐字稿」 | 加 `--translate-to zh-CN`，给 `translation` 里的逐字稿 |
| 「第几分钟讲到 X」 | 用带时间戳的 `transcript` 定位 |
| 「视频里那页 PPT 写了什么」 | 看 `ocr_text`（画面文字） |
| 「把这个英文教程整理成笔记」 | 要点 + 逐字稿，按时间顺序整理 |

不适合：搜索视频、读评论、读频道的视频列表、下载视频或音频、直播进行中的内容。

## 准备

1. https://linkdigest.dev/app/keys 登录并创建 API Key，新账户送 10 积分。
2. `export LINKDIGEST_API_KEY=ld_live_...`（或写进 OpenClaw 配置里本技能的 `env`）。

## 返回内容

- `title`、`author`（频道）；
- `transcript[]`：`{t, text}`，`t` 是秒；
- `ocr_text[]`：画面上出现过的文字；
- `key_points[]`：要点，每条附一句在逐字稿里逐字核对过的引用（`key_point_support`）；
- `translation`（加了 `--translate-to` 时）：标题、要点、逐字稿的译文，原文保留在旁边；
- `coverage`：读了多少秒、哪些没读到；
- `credits`、`cached`：这次扣了几个积分，是否命中缓存。

目前拿不到视频简介（description）里的文字和上传日期，回执里会写明；需要简介里的链接时请让用户直接贴出来。

## 参数

- `--format json`：要结构化数据时用；默认输出 Markdown。
- `--translate-to zh-CN`：加译文，+1 积分。
- `--max-credits N`：这条视频最多花 N 积分，超了就不读、不扣费。先用它问价很方便。
- `--job-id <jobId>`：长视频没等到结果时，用它接着取，不要重新提交。

退出码：0 成功；3 Key 无效；4 积分不够或视频超长（未扣费，会打印支付宝付款链接）；5 读不了；7 还在跑。

## 费用

1 积分约 ¥0.14（加量包 ¥36 = 250 积分，支付宝可付，不过期）。

| 视频时长 | 积分 | 约合 |
| --- | --- | --- |
| 1 分钟以内 | 2 | ¥0.29 |
| 5 分钟 | 6 | ¥0.86 |
| 10 分钟 | 11 | ¥1.58 |
| 30 分钟（Dev 月付账户上限） | 31 | ¥4.46 |
| 加中文译文 | +1 | +¥0.14 |
| 别人读过的同一条视频（缓存） | 0 | 0 |

算法：基础 1 积分 + 每开始的 1 分钟 1 积分。免费账户和加量包账户单条最长 10 分钟，Dev 月付（$9/月，500 积分）30 分钟，超过会直接拒绝且不扣费。YouTube 没有「省钱档」，`--depth transcript` 对 YouTube 不生效。

## 回答用户时

- 总结用 `key_points`，并给出对应时间点，方便用户跳转。
- 逐字稿是模型看视频得到的，专有名词和数字可能有误，重要信息提醒用户核对原视频。
- 很长的译文可能只覆盖逐字稿的前一部分，结果里会写明覆盖到哪里，照实告诉用户。
- 说明这次用了几个积分。

## 隐私与限制

只把链接发到 linkdigest.dev，不使用你的 Google 账号。不保存视频。文字结果按链接缓存。年龄限制、会员专享、私享和已删除的视频读不了。每小时最多 60 次调用。脚本只读 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不写文件。

同一个 Key 还能读小红书、抖音、TikTok、X 和公众号文章。文档：https://linkdigest.dev/zh/docs ，反馈：support@linkdigest.dev
