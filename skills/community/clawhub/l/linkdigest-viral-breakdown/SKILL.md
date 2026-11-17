---
name: linkdigest-viral-breakdown
description: "爆款拆解：把一条抖音、小红书、TikTok 或 YouTube 内容拆成开头钩子、带时间的结构节拍、标题公式、封面文字、行动号召和可复用模板。引用的原话逐字核对原文，对不上的删掉并写明删了几条；点赞收藏和话题标签取自平台数据，不由模型编写。用户要拆解爆款、分析对标账号、学习内容结构或准备仿写时使用。通过 LinkDigest API 读取，不需要平台账号或 Cookie。需要 LINKDIGEST_API_KEY；在读取费用上加 1 积分（约 ¥0.14），6 张图以内的图文笔记加拆解共 2 积分。"
version: 1.2.1
homepage: https://linkdigest.dev/zh/docs?ref=skill-linkdigest-viral-breakdown
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-linkdigest-viral-breakdown&next=/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-linkdigest-viral-breakdown"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-linkdigest-viral-breakdown&next=/app/keys"
    required_for: "the full output; without it the script gives one free summary a day"
---

# 爆款拆解（引用逐字核对原文）

> 脚本路径 `scripts/linkdigest.py` 相对于本技能目录。

给一条抖音、小红书、TikTok 或 YouTube 链接，先读出逐字稿、画面文字、图片文字和互动数据，再分析这条内容是怎么做出来的：开头怎么留人、每一步讲什么、标题怎么写、结尾怎么引导，最后给一个可以套用的模板。

和让模型「看完写个拆解」的区别在于：拆解里每一句标成原话的引用，都会和读出来的原文逐字比对，找不到的直接删掉，并在 `missing` 里写明删了几条。点赞、评论、收藏、话题标签直接取自平台数据，不让模型写。

## 实测例子

一条 15:42 的抖音剪辑教程（https://www.douyin.com/video/7515405363630443830 ），要求用英文写拆解（`translate_to: "en"`）：

- 得到 10 个带时间的结构节拍；
- 模型写出的引用里有 7 条在视频里找不到原话，被删掉，`missing` 里写着 `7 quote(s) removed: not found word for word in the post`；
- 留下的引用保持中文原话，例如（节选）：

```json
{"t": 24, "label": "Demonstration of Problem",
 "summary": "Shows a basic linear keyframe animation that looks boring and uniform, establishing the baseline problem.",
 "quote": "可以看到它的这个运动是不是比较的无聊，是一个比较匀速平稳的缩放"}
```

## 什么时候用

- 「拆解这条爆款」「分析一下这个视频为什么火」「这篇笔记的结构是什么」「帮我仿写这条」。
- 研究对标账号：一条一条拆，对比钩子、节拍和行动号召。
- 写脚本前找结构参考。

## 什么时候不用

- 只要文案或图片文字：用 `linkdigest-video-transcript` 或 `linkdigest-xhs-note-ocr`，少花 1 积分。
- 要账号整体诊断、流量预测或「保证爆」：这个技能只拆单条内容，不预测效果。
- 私密、已删除、需要登录才能看的内容读不了（返回 422，不扣费）。B站链接可以读（2026-10-24 起）。

## 准备（一次）

1. 打开 https://linkdigest.dev/signin?ref=skill-linkdigest-viral-breakdown&next=/app/keys ，用 Google 或邮箱登录（邮箱会收到一封登录链接），创建 API Key（`ld_live_` 开头）。新账户送 10 积分，只送一次，不用绑卡。
2. 设置环境变量：

```bash
export LINKDIGEST_API_KEY=ld_live_...
```

也可以写进 OpenClaw 配置（`~/.openclaw/openclaw.json`）里这个技能的 `env`：

```json5
{ skills: { entries: { "linkdigest-viral-breakdown": { env: { LINKDIGEST_API_KEY: "ld_live_..." } } } } }
```

Key 只放在环境变量或配置里，不要贴进对话、代码或提交记录。

## 用法

推荐用自带脚本（Python 3.8+ 标准库，已经处理好 202 排队和轮询）：

```bash
python3 scripts/linkdigest.py "<链接或整段分享文案>" --breakdown
python3 scripts/linkdigest.py "<链接>" --breakdown --format json
python3 scripts/linkdigest.py "<英文 TikTok 链接>" --breakdown --translate-to zh-CN   # 拆解用中文写，再 +1 积分
```

- 拆解默认用这条内容本身的语言写；加 `--translate-to` 就用指定语言写，并附整条内容的译文（再 +1 积分），引用仍是原文。
- 分享文案里有引号或换行时，从标准输入传：`printf '%s' "$SHARE_TEXT" | python3 scripts/linkdigest.py - --breakdown`
- 视频较长时会先返回 202，脚本自动轮询（默认最多等 900 秒，`--timeout` 可改）；超时就按提示用 `--job-id` 接着取，同一个 jobId 只扣一次费。
- `--max-credits 5`：这条超过 5 积分就不读、不扣费（返回 402）。
- 退出码：0 成功；2 参数错误或没设 Key；3 Key 无效（401）；4 积分不够或视频超长（402，未扣费）；5 链接读不了（422）；6 调用太频繁，或这个 Key 在 /app/keys 设的 30 天积分上限已用完（429，未扣费）；7 等待超时。

### 直接调 HTTP（没有 Python 时）

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://v.douyin.com/<短链>/", "format": "json", "breakdown": true}'
```

- `200`：结果 JSON，拆解在 `breakdown` 字段里。
- `202`：`{"pending":true,"jobId":"…","poll":"/api/v1/digest/…","retryAfter":15}`。用 jobId 取，不要重新提交：

```bash
curl -sS "https://linkdigest.dev/api/v1/digest/<jobId>?wait=20" \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY"
```

`wait=20` 让服务端最多等 20 秒再回复；仍是 `202` 就再取一次，直到 `200`。要 Markdown 时，提交用 `"format": "markdown"`，取结果加 `&format=markdown`（`202` 响应始终是 JSON）。`breakdown` 必须是布尔值 `true`，写成 `"yes"` 会返回 400。

可以直接运行的 bash/zsh 版本（提交 + 轮询，最多约 15 分钟）：

```bash
API=https://linkdigest.dev/api/v1/digest
AUTH="Authorization: Bearer $LINKDIGEST_API_KEY"
LINK='https://v.douyin.com/<短链>/'
res=$(curl -sS -w '\n%{http_code}' -X POST "$API" -H "$AUTH" \
  -H "Content-Type: application/json" -d "{\"url\": \"$LINK\", \"format\": \"json\", \"breakdown\": true}")
code=${res##*$'\n'}; body=${res%$'\n'*}
n=0
while [ "$code" = 202 ] && [ $n -lt 45 ]; do
  n=$((n+1))
  job=$(printf '%s' "$body" | sed -n 's/.*"jobId":"\([^"]*\)".*/\1/p')
  res=$(curl -sS -w '\n%{http_code}' "$API/$job?wait=20" -H "$AUTH")
  code=${res##*$'\n'}; body=${res%$'\n'*}
done
echo "HTTP $code" >&2
printf '%s\n' "$body"
```

## 返回字段

`breakdown` 里：

| 字段 | 内容 |
| --- | --- |
| `language` / `format` | 拆解用的语言；内容形式（如教程、口播） |
| `hook` | 开头怎么留人：`spoken` 说的话（原话）、`on_screen` 屏幕上的字（原话）、`visual` 画面、`why` 为什么有效 |
| `beats[]` | 最多 10 个结构节拍：视频是 `t`（秒，大致时间），图文是 `image`（第几张图）；`label` 标签、`summary` 摘要、`quote` 一句原话 |
| `title_formula` | 标题公式，例如「数字 + 结果 + 人群」 |
| `cover_text` / `cta` | 封面文字、行动号召（原话） |
| `audience` | 目标人群 |
| `tags` / `engagement` | 话题标签；点赞、评论、收藏、分享（`as_of` 是读取日期）。直接取自平台数据 |
| `template[]` | 可复用模板，最多 8 步，用 [产品]、[痛点] 这样的占位 |
| `remix_ideas[]` | 二创方向，最多 3 个 |
| `missing[]` | 这次拆解看不到或删掉的东西：没有语音、只读了一部分、删了几条对不上原文的引用等 |

同一个响应里还有完整的读取结果：`transcript`、`on_screen`、`images`、`caption`、`key_points`、`stats`、`credits`、`cached` 等（字段说明见另外两个技能）。`raw_markdown` 里拆解在原文之后，单独一节。

## 引用怎么核对

- 被核对的字段：`hook.spoken`、`hook.on_screen`、`beats[].quote`、`cover_text`、`cta`。
- 核对对象：这条内容读出来的文字，包括标题、正文、逐字稿、画面文字、图片文字和图片描述。比较时忽略空格、标点和大小写。
- 找不到的引用置空，`missing` 里加一条：中文拆解写「删除了 N 处无法在原文中逐字找到的引用」，英文拆解写 `N quote(s) removed: not found word for word in the post`。
- 局限：核对的是读出来的文字，不是音频本身。语音识别听错的字，引用里也会是同样的错字。`visual`、`why`、`summary`、`title_formula`、`template`、`remix_ideas` 是模型的分析，不是原话，不做核对。
- 视频节拍的 `t` 是大致时间，误差可能有几秒到几十秒，引用请以 `quote` 的文字为准。

## 把结果交给用户时

- 标成原话的内容（`hook.spoken`、`hook.on_screen`、`quote`、`cover_text`、`cta`）原样给出，带上时间或图号。不要自己补写「原话」，也不要改写后仍标成原话。
- 用户要仿写时，新写的内容明确标为新写的，和原文引用分开。
- 把 `missing` 告诉用户，尤其是删了几条引用、只读了一部分视频、没有语音这几种。
- 互动数据带上 `as_of` 日期，说明是读取当天的数。
- 模板是结构参考，不要承诺照做就能火。
- 告诉用户这次用了几个积分（`credits`）。

## 费用

拆解在读取费用上加 1 积分。按加量包 ¥36 = 250 积分折算，1 积分约 ¥0.144。

| 内容 | 积分 | 约合 |
| --- | --- | --- |
| 图文笔记（6 张图以内）+ 拆解 | 2 | ¥0.29 |
| 1 分钟以内的视频 + 拆解 | 3 | ¥0.43 |
| 3 分钟视频 + 拆解 | 5 | ¥0.72 |
| 10 分钟视频 + 拆解 | 12 | ¥1.73 |
| 再加译文 / 用其他语言写拆解（`--translate-to`） | +1 | +¥0.14 |
| 同一链接的拆解已被读过（缓存） | 0 | 0 |
| 读不出内容 | 0 | 0 |

图文每多 6 张图 +1 积分；视频每开始的 1 分钟 +1 积分。这条链接之前被读过、只是没拆解过时，原文走缓存，通常只收拆解的 1 积分，以返回的 `credits` 为准。

注册送 10 积分（每个账户一次，不按月补）。加量包 $5 = 250 积分，可用支付宝付款（按 ¥36 结算），不过期；或 Dev 月付 $9 = 每月 500 积分（银行卡）。价格以 https://linkdigest.dev/zh/docs?ref=skill-linkdigest-viral-breakdown 为准。

## 限制

- B站：可以读（2026-10-24 起）。B 站偶尔拒绝时返回 503，不扣费，稍后重试即可。
- 单条视频长度上限：免费账户和只买了加量包的账户 10 分钟，Dev 月付 30 分钟；超过返回 402（`media_too_long`），不扣费。免费账户和加量包账户可加 `--partial-ok` 只拆开头，`missing` 里会写明只读了一部分。
- 拆解只看这一条内容，看不到账号粉丝数、投流、发布时间段这些背景，`missing` 里通常会写出来。
- 互动数据是读取当天的快照；缓存里的结果保留第一次读取那天的数。
- 每个账户每小时最多 60 次 API 调用。

## 隐私

- 只把你给的链接发给 linkdigest.dev，不需要也不会读取你的平台账号或 Cookie。
- 视频、音频、图片只在处理时放在临时目录，返回前删除，不保存、不转发。
- 文字结果（包括拆解）按链接缓存（所以同一链接再读免费），可能提供给请求同一公开链接的其他用户。不要提交私密内容的链接。
- 读取和拆解会用到第三方模型服务，详见 https://linkdigest.dev/privacy 。
- `scripts/linkdigest.py` 只读环境变量 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不读写本地文件。

## 其他接入方式

- 远程 MCP（Streamable HTTP）：`https://linkdigest.dev/mcp`，请求头 `Authorization: Bearer <key>`，工具 `digest_url`，参数 `breakdown: true`。Claude Code：
  `claude mcp add --transport http linkdigest https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- 只支持本地（stdio）MCP 的客户端：`npx mcp-remote https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- Dify 插件市场：`jcaiagent7143-ui/linkdigest`
- OpenAPI：https://linkdigest.dev/openapi.json
- 开源客户端与接入示例：https://github.com/jcaiagent7143-ui/linkdigest-mcp
- 中文文档：https://linkdigest.dev/zh/docs?ref=skill-linkdigest-viral-breakdown

LinkDigest 由独立开发者 Jack（GitHub `jcaiagent7143-ui`）开发和维护。问题和反馈：support@linkdigest.dev
