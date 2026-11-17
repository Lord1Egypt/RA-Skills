---
name: linkdigest-script-rewrite
description: "对标视频脚本仿写：给一条抖音、小红书或 TikTok 爆款视频链接，先提取它的口播稿（逐字稿）和结构（开头钩子、分段节拍、标题公式、结尾引导），再按同样的结构写出你自己主题的口播脚本。用户说「仿写这条视频」「照这个结构写个脚本」「扒一下这条视频的文案再改写」「口播稿改写」时使用。原视频内容通过 LinkDigest API 读取，引用逐字核对原文，需要 LINKDIGEST_API_KEY；仿写由你当前的模型完成，不另收费。"
version: 1.2.1
homepage: https://linkdigest.dev/zh/docs?ref=skill-linkdigest-script-rewrite
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-linkdigest-script-rewrite&next=/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-linkdigest-script-rewrite"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-linkdigest-script-rewrite&next=/app/keys"
    required_for: "the full output; without it the script gives one free summary a day"
---

# 对标视频脚本仿写（口播稿提取 → 结构拆解 → 写你的版本）

> 脚本路径 `scripts/linkdigest.py` 相对于本技能目录。

这是一个三步流程的技能。和只做拆解的 `linkdigest-viral-breakdown` 不同，这里的目标是交付一份可以直接拍的新脚本。

## 流程

### 第 1 步：问清楚两件事

动手之前向用户确认（已经说过的不用再问）：

- 对标视频的链接（抖音、小红书视频笔记或 TikTok）；
- 用户自己的主题、产品或人设，以及想要的时长（比如「60 秒左右」）。

### 第 2 步：取回原视频的口播稿和结构

```bash
python3 scripts/linkdigest.py "<对标视频链接或整段分享文案>" --breakdown --format json
```

读这些字段：

| 字段 | 用来做什么 |
| --- | --- |
| `transcript[]` | 原口播稿，带时间（秒） |
| `on_screen[]` / `ocr_text[]` | 画面上的字幕和大字 |
| `breakdown.hook` | 开头钩子：原话 `spoken`、画面字 `on_screen`、为什么有效 `why` |
| `breakdown.beats[]` | 分段节拍：每段的时间 `t`、作用 `label`、内容 `summary`、原话 `quote` |
| `breakdown.title_formula` / `cover_text` | 标题公式、封面字 |
| `breakdown.cta` | 结尾引导（关注、评论、私信） |
| `breakdown.template[]` | 抽象出来的可复用模板 |
| `breakdown.missing[]` | 拆解时没看到的部分，仿写时别假设 |
| `stats` | 点赞、收藏、评论、分享（读取当天的数） |

`quote` 都是代码在原文里逐字核对过的；没通过核对的引用会被删掉，不会编。

视频超过 10 分钟（免费和加量包账户的完整档上限）时，加 `--depth transcript`：全程逐字稿，每 2 分钟 1 积分，可读到 60 分钟。

### 第 3 步：写用户自己的脚本

用你当前的模型来写，规则：

1. **照结构，不照句子。** 保留节拍顺序、每段的作用和大致时长占比；每一句都换成用户主题的内容。不要搬运原视频的原话。
2. **钩子用同一种手法**（提问、反常识、数字、冲突……以 `hook.why` 为准），内容换成用户的。
3. **按时长控制字数**：中文口播大约每秒 4 个字，60 秒约 240 字。
4. **事实只用用户给的。** 用户没提供的数据、案例、功效不要编；需要时留「【这里填你的数据】」。
5. 输出格式：

```
标题（按原标题公式写 3 个备选）
封面字
【0–3 秒 钩子】口播 / 画面字
【3–15 秒 ……】口播 / 画面提示
……
【结尾引导】
```

6. 最后附一张对照表：原视频每个节拍 → 新脚本对应段落，让用户看得出结构是怎么对应的。

## 交付时说明

- 哪些来自原视频（口播稿、画面字、互动数据），哪些是模型的分析（拆解），哪些是新写的（脚本）。
- `breakdown.missing` 里有内容时告诉用户，比如「没看到评论区，无法判断评论引导是否有效」。
- 这次读取用了几个积分。同一条对标视频再读是缓存，0 积分，可以放心反复仿写不同主题。
- 提醒用户：借鉴结构可以，照搬原文案可能构成抄袭，也容易被平台判重。

## 准备

1. https://linkdigest.dev/signin?ref=skill-linkdigest-script-rewrite&next=/app/keys 创建 API Key（新账户送 10 积分，不用绑卡）。
2. `export LINKDIGEST_API_KEY=ld_live_...`

## 费用

只有「读原视频」这一步收费：

| 对标视频 | 积分（含拆解 +1） | 约合 |
| --- | --- | --- |
| 1 分钟以内 | 3 | ¥0.43 |
| 3 分钟 | 5 | ¥0.72 |
| 5 分钟 | 7 | ¥1.01 |
| 读过的同一条（缓存，只补拆解） | 0–1 | ¥0–0.14 |
| 读不出内容 | 0 | 0 |

基础 1 积分 + 每开始的 1 分钟 1 积分 + 拆解 1 积分。加量包 ¥36 = 250 积分，支付宝可付。价格以 https://linkdigest.dev/zh/docs?ref=skill-linkdigest-script-rewrite 为准。

## 限制

- 一次一条链接；不搜索爆款、不看账号主页、不读评论。
- 图文笔记也能读（拆解按图片顺序），但这个技能主要为视频口播设计。
- 私密、已删除、需要登录的内容读不了（不扣费）。不支持快手、视频号。
- 互动数据是读取当天的快照。

## 隐私

只把对标视频的链接发到 linkdigest.dev；用户自己的主题和产品信息留在你的对话里，不会发出去。视频只在处理时临时下载，读完即删。脚本只读 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不写文件。

反馈：support@linkdigest.dev ｜ 文档：https://linkdigest.dev/zh/docs?ref=skill-linkdigest-script-rewrite
