---
name: linkdigest-xhs-note-ocr
description: "小红书图文笔记提取，连图片里的字一起 OCR。用户发来小红书笔记链接或分享文案（xiaohongshu.com、xhslink.com），要提取笔记正文、图片上的文字、每张图的描述、要点、点赞收藏数或话题标签时使用。图文笔记的正文常写在图片里，直接抓网页拿不到。通过 LinkDigest API 读取，不需要小红书账号或 Cookie。需要 LINKDIGEST_API_KEY，按量计费：6 张图以内 1 积分（约 ¥0.14），注册送 10 积分。"
version: 1.2.2
homepage: https://linkdigest.dev/zh/docs?ref=skill-linkdigest-xhs-note-ocr
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-linkdigest-xhs-note-ocr&next=/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-linkdigest-xhs-note-ocr"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-linkdigest-xhs-note-ocr&next=/app/keys"
    required_for: "the full output; without it the script gives one free summary a day"
---

# 小红书图文笔记提取（含图片文字 OCR）

> 脚本路径 `scripts/linkdigest.py` 相对于本技能目录。

小红书图文笔记的正文经常写在图片里：标题一句话，干货全在图上。直接抓网页只能拿到标题、几行正文和反复出现的「打开App查看更多」。这个技能把笔记链接交给 LinkDigest，返回正文、每张图的描述和图上的文字（OCR）、要点、点赞收藏数和话题标签，按图片顺序排好。

实测同一条图文笔记（公开结果页：https://linkdigest.dev/d/5d0e7837ec2742ea4ae07806d979f0ce ）：

- 直接 curl 网页，去掉脚本和样式后只剩 860 个可见字符；
- yt-dlp 报 `No video formats found`（它只认视频笔记）；
- LinkDigest 返回的 Markdown 是 35,059 个字符，约为前者的 41 倍。

## 什么时候用

- 用户发来小红书笔记链接或整段分享文案，要「提取文案」「图片上的字」「把这篇笔记转成文字」「整理成文档」。
- 做选题或竞品调研，需要笔记的完整内容和互动数据。
- 笔记是视频时，同一个接口也能读，逐字稿的说明见 `linkdigest-video-transcript` 技能。

## 什么时候不用

- 要搜索笔记、看评论、发布或点赞：这个技能只读单条笔记，不搜索、不登录、不发帖。
- 私密、已删除或需要登录才能看的笔记：读不了（返回 422，不扣费）。
- B站链接：可以读（2026-10-24 起）。

## 准备（一次）

1. 打开 https://linkdigest.dev/signin?ref=skill-linkdigest-xhs-note-ocr&next=/app/keys ，用 Google 或邮箱登录（邮箱会收到一封登录链接），创建 API Key（`ld_live_` 开头）。新账户送 10 积分，只送一次，不用绑卡。
2. 设置环境变量：

```bash
export LINKDIGEST_API_KEY=ld_live_...
```

也可以写进 OpenClaw 配置（`~/.openclaw/openclaw.json`）里这个技能的 `env`：

```json5
{ skills: { entries: { "linkdigest-xhs-note-ocr": { env: { LINKDIGEST_API_KEY: "ld_live_..." } } } } }
```

Key 只放在环境变量或配置里，不要贴进对话、代码或提交记录。

## 用法

推荐用自带脚本。它只用 Python 3.8+ 标准库，已经处理好 202 排队和轮询：

```bash
python3 scripts/linkdigest.py "<笔记链接或整段分享文案>"
```

- 默认输出 Markdown，适合直接读；要结构化数据加 `--format json`（脚本会省略和其他字段重复的 `raw_markdown`）。
- 分享文案里有引号或换行时，从标准输入传：`printf '%s' "$SHARE_TEXT" | python3 scripts/linkdigest.py -`
- 用 App 里「分享 → 复制链接」得到的链接，保留链接上的参数（如 `xsec_token`）；整段分享文案也可以，服务端会从里面取出链接。
- 想控制花费：`--max-credits 2`，这条笔记超过 2 积分就不读、不扣费（返回 402）。
- 本次扣了几个积分、是否命中缓存，打印在 stderr 的最后一行。
- 退出码：0 成功；2 参数错误或没设 Key；3 Key 无效（401）；4 积分不够（402，未扣费，stderr 里有付款链接）；5 链接读不了（422）；6 调用太频繁，或这个 Key 在 /app/keys 设的 30 天积分上限已用完（429，未扣费）；7 等待超时（任务还在跑，按提示用 `--job-id` 接着取）。

### 直接调 HTTP（没有 Python 时）

提交：

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.xiaohongshu.com/explore/<笔记ID>?xsec_token=<...>", "format": "json"}'
```

- `200`：结果 JSON，字段见下文。
- `202`：还在处理，返回 `{"pending":true,"jobId":"…","poll":"/api/v1/digest/…","retryAfter":15}`。用 jobId 取结果，不要重新提交：

```bash
curl -sS "https://linkdigest.dev/api/v1/digest/<jobId>?wait=20" \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY"
```

`wait=20` 让服务端最多等 20 秒再回复；仍是 `202` 就再取一次，直到 `200`。要 Markdown 时，提交用 `"format": "markdown"`，取结果加 `&format=markdown`（`202` 响应始终是 JSON）。用 curl 传分享文案时，注意把里面的引号和换行按 JSON 转义。

可以直接运行的 bash/zsh 版本（提交 + 轮询，最多约 15 分钟）：

```bash
API=https://linkdigest.dev/api/v1/digest
AUTH="Authorization: Bearer $LINKDIGEST_API_KEY"
LINK='https://www.xiaohongshu.com/explore/<笔记ID>?xsec_token=<...>'
res=$(curl -sS -w '\n%{http_code}' -X POST "$API" -H "$AUTH" \
  -H "Content-Type: application/json" -d "{\"url\": \"$LINK\", \"format\": \"json\"}")
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

## 返回字段（图文笔记）

| 字段 | 内容 |
| --- | --- |
| `title` / `author` / `posted_at` | 标题、作者、发布日期 |
| `caption` | 笔记正文（文字部分） |
| `images[]` | 按图片顺序，每张一个 `{description, ocr}`：`description` 是模型写的画面描述，`ocr` 是图上的文字 |
| `ocr_text[]` | 所有图片里读出的文字片段汇总成一个列表（同样的字只出现一次）；要按图对应，用 `images[].ocr` |
| `key_points[]` | 要点，用原文语言 |
| `stats` | `likes` 点赞、`comments` 评论、`collects` 收藏、`shares` 分享；是读取当天平台给的数，`as_of` 是日期，拿不到的是 `null` |
| `tags[]` | 话题标签 |
| `raw_markdown` | 整条内容的 Markdown：`## Caption`、`## Key points`、`## Images`（每张图是「**Image N.** 描述」，下面引用块里是图上文字） |
| `credits` / `cached` | 本次扣了几个积分；读过的链接 `cached=true`，0 积分 |
| `degraded[]` | 处理中没做完的部分的说明，正常为空 |

## 把结果交给用户时

- 用户要「文案」「图片上的字」：先给 `caption`，再按顺序给每张图的 `ocr`，标明「图 1」「图 2」。原样给出，不改写、不总结，除非用户要求。
- `caption`、`ocr`、`stats`、`tags` 来自笔记本身；`images[].description` 和 `key_points` 是模型写的。转述时分清楚。
- 花体字、手写字、很小的字可能认错。涉及价格、数字、品牌名时，提醒用户对照原图。
- 告诉用户这次用了几个积分（`credits`，缓存命中是 0）。

## 费用

按加量包 ¥36 = 250 积分折算，1 积分约 ¥0.144。

| 内容 | 积分 | 约合 |
| --- | --- | --- |
| 图文笔记，6 张图以内 | 1 | ¥0.14 |
| 7–12 张图 | 2 | ¥0.29 |
| 13–18 张图 | 3 | ¥0.43 |
| 加爆款拆解（`--breakdown`） | +1 | +¥0.14 |
| 加译文（`--translate-to en` 等） | +1 | +¥0.14 |
| 任何人读过的链接（缓存） | 0 | 0 |
| 读不出内容 | 0 | 0 |

注册送 10 积分（每个账户一次，不按月补）。加量包 $5 = 250 积分，可用支付宝付款（按 ¥36 结算），不过期；或 Dev 月付 $9 = 每月 500 积分（银行卡）。价格以 https://linkdigest.dev/zh/docs?ref=skill-linkdigest-xhs-note-ocr 为准。

## 限制

- B站：可以读（2026-10-24 起）。B 站偶尔拒绝时返回 503，不扣费，稍后重试即可。
- 私密、已删除、需要登录才能看的笔记读不了。
- 视频笔记另按时长计费（每开始的 1 分钟 +1 积分）；免费账户和加量包账户单条视频最长 10 分钟，Dev 月付 30 分钟，超过返回 402 且不扣费。详见 `linkdigest-video-transcript`。
- 互动数据是读取当天的快照，不是实时数据；缓存里的结果保留第一次读取那天的数。
- 每个账户每小时最多 60 次 API 调用。
- 不搜索、不读评论、不登录、不发帖、不点赞。

## 隐私

- 只把你给的链接发给 linkdigest.dev，不需要也不会读取你的小红书账号或 Cookie。
- 图片、视频、音频只在处理时放在临时目录，返回前删除，不保存、不转发。
- 文字结果按链接缓存（所以同一链接再读免费），可能提供给请求同一公开链接的其他用户。不要提交私密内容的链接。
- 读取时会用到第三方模型服务，详见 https://linkdigest.dev/privacy 。
- `scripts/linkdigest.py` 只读环境变量 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不读写本地文件。

## 其他接入方式

- 远程 MCP（Streamable HTTP）：`https://linkdigest.dev/mcp`，请求头 `Authorization: Bearer <key>`，工具 `digest_url`。Claude Code：
  `claude mcp add --transport http linkdigest https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- 只支持本地（stdio）MCP 的客户端：`npx mcp-remote https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- Dify 插件市场：`jcaiagent7143-ui/linkdigest`
- OpenAPI：https://linkdigest.dev/openapi.json
- 开源客户端与接入示例：https://github.com/jcaiagent7143-ui/linkdigest-mcp
- 中文文档：https://linkdigest.dev/zh/docs?ref=skill-linkdigest-xhs-note-ocr

LinkDigest 由独立开发者 Jack（GitHub `jcaiagent7143-ui`）开发和维护。问题和反馈：support@linkdigest.dev
