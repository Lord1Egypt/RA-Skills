---
name: kuaishouzhushou
description: "用于快手数据分析、快手视频详情、快手作品数据、互动指标、内容调研和快手内容分析。覆盖 Kuaishou / Kwai，来自GuaiKei社媒数据助手。提供快手关键词搜索、快手博主作品获取、快手视频评论获取等功能。支持三大能力：(1) 关键词搜索视频，可按点赞数、发布时间、视频时长筛选排序；(2) 达人作品抓取，按主页链接获取公开作品列表；(3) 视频评论分析，按视频链接获取评论内容与互动数据。"
license: MIT
version: 1.1.1
metadata:
  openclaw:
    emoji: "📷"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins: ["node"]
    env: ["GUAIKEI_API_TOKEN"]
  env_desc:
    GUAIKEI_API_TOKEN: "快手数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通。"
  keywords:
    - "快手"
    - "Kuaishou"
    - "快手搜索"
    - "快手评论"
    - "快手博主"
    - "爆款选题"
    - "竞品分析"
    - "评论舆情"
  category:
    - "Integrations"
    - "Research"
    - "数据分析"
    - "内容创作"
    - "商业运营"
  tags:
    - "快手"
    - "Kuaishou"
    - "短视频"
    - "关键词搜索"
    - "视频评论"
    - "博主作品"
    - "竞品分析"
    - "选题调研"
    - "舆情分析"
    - "爆款挖掘"
    - "趋势洞察"
    - "内容选题"
    - "快手运营"
    - "快手内容创作"
    - "快手营销"
    - "快手互动数据统计"
    - "博主作品监控"
    - "视频查询"
  schemas:
    - name: "输出信封"
      file: "assets/output_envelope.schema.json"
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
  examples:
    - "帮我搜快手里「具身智能」的高赞视频 → node scripts/kuaishou/search-cli.js --keyword \"具身智能\" --sort 2 --limit 20"
    - "最近一周最新的快手 AI 教程，要 20 条 → node scripts/kuaishou/search-cli.js --keyword \"AI 教程\" --sort 1 --time 7 --limit 20"
    - "这条快手视频评论区在说什么 → node scripts/kuaishou/comment-cli.js --url \"https://www.kuaishou.com/short-video/3xabc\" --limit 40"
    - "这个快手博主最近 20 条作品 → node scripts/kuaishou/post-cli.js --url \"https://www.kuaishou.com/profile/3xabc\" --sort 0 --limit 20"
    - "这个快手博主多少粉丝 → node scripts/kuaishou/post-cli.js --url 123456 --limit 0"
---

# 📊 快手运营助手

> ✨ **一句话价值**：面向快手公开数据的检索与洞察技能，用于关键词搜索视频、抓取博主作品、拉取视频评论，并返回结构化数据供后续分析、汇总或生成报告，帮助你实现快手账号的快速增长与精准营销。

给一个关键词或一条链接，拿回快手公开视频、评论和博主数据。不登录，不发布。结果是一份 JSON。

| 你要做的事 | 用哪个命令 | 你拿到什么 |
| --- | --- | --- |
| 找选题、看高赞 | `search-cli.js` | 视频数组。点赞、播放、评论是数字 |
| 看评论区 | `comment-cli.js` | 评论数组 |
| 看博主作品 | `post-cli.js --limit 大于 0` | `results.post` 作品数组，以及可能有的 `results.user` |
| 看粉丝、获赞 | `post-cli.js --limit 0` | `results.user`。`fan` 粉丝，`like` 点赞，`follow` 关注 |

作品里的互动数是字符串，搜索和评论里的互动数是数字。比较之前先看 schema。空字符串和数字 0 可能不返回。

## 0. 每次按这个顺序执行

1. 确认环境变量 `GUAIKEI_API_TOKEN` 已配置。没有配置时直接告诉用户去 [快手运营助手](https://www.guaikei.com) 开通，不要先跑一遍试探。
2. 在本技能根目录执行 `node scripts/kuaishou/<命令>.js`。
3. stderr 出现「处理中」表示任务还在跑。等进程自己退出，再读 stdout 的最后一份 JSON。不要把 stderr 或整份 JSON 念给用户。
4. 按「4. 读结果」的退出码表决定：改参数再试、告诉用户，或停止。

查询最多 20 次。间隔从 2 秒起按 2、4、8、16、32 秒增加，之后每次 60 秒，只算等待大约 15 分钟。每次请求本身还有最多 20 秒超时。宿主如果更早结束进程，按超时处理，不要立刻用同一组参数连打。

同一组参数再次执行时，搜索、作品和评论大约 20 分钟内会复用已有任务。等到 `TIMEOUT` 后再立刻重跑，通常仍落在这个窗口里。

- 没有关键词或链接就先问，不要编造
- 搜索不传 `--limit` 是 10 条。用户说「全部」再加大，不要自行抓 10000 条。用户未说明套餐时优先默认 10；需要更多时先说明可能受套餐限制
- `status=empty` 且退出码 0 是「没有结果」，不是命令失败
- 这个技能没有视频详情命令。视频链接只能拉评论

**套餐双上限（重要）**：技能侧硬上限为 10000（按量 Token）。**包月 Token** 超限会返回 `PLAN_LIMIT`（后端 errcode 14），不要当网络错误重试：搜索最多 **30**，作品最多 **50**，评论最多 **60**。具体以官网与本次 `message` 为准。

## 1. 什么时候调用

满足任一条件即调用：用户提到快手或 Kuaishou，并要求搜索、看评论、看博主作品或做选题、竞品、舆情。

不要调用：只让写文案；平台是抖音、小红书、B 站、微博、公众号；要求登录、发布、点赞或私密数据；没有关键词也没有可识别链接。

## 2. 路由

按这个顺序判断，命中即停：

1. 要评论、留言、舆情，且对象是一条视频 → `comment-cli.js`
2. 要作品、主页、账号、博主、粉丝 → `post-cli.js`
3. 有关键词，且没有上面两类信号 → `search-cli.js`
4. 以上都不明确 → 先追问

链接和 id：

- `kuaishou.com/profile/{id}` 只能给 `post-cli.js`
- 纯数字 `user_id` 只能给 `post-cli.js`。搜索结果里用 `user.user_id`，或直接用 `user.url`
- `kuaishou.com/short-video/{id}`、`v.kuaishou.com/*`、裸的 `3x...` 只能给 `comment-cli.js`。搜索结果里用视频 `id` 或 `url`
- `user.id` 和作品结果里的 `kwaiId` 是快手号，不要交给作品命令
- 只拿到一个裸 `3x`、又没说明是视频还是从主页路径里拆出来的，先问。不要两个命令都试
- `http://` 会改成 `https://`。不带 `www` 的 `kuaishou.com` 会补成 `www`。协议和主机名不区分大小写，id 保持原样

| 用户说 | 应该传 |
| --- | --- |
| 爆款、高赞、什么火 | `search-cli.js --sort 2` |
| 最新、刚发的 | `search-cli.js --sort 1` |
| 近一天 | `--time 1` |
| 近一周、这周 | `--time 7` |
| 近一月 | `--time 30` |
| 1 分钟以内 | `--duration 1` |
| 博主最近发了什么 | `post-cli.js --sort 0 --limit N`。没说条数就问 |
| 这个博主什么最火 | `post-cli.js --sort 1` |
| 多少粉丝 | `post-cli.js --limit 0` |
| 评论区 | `comment-cli.js`。没说条数用默认 10 |

搜索的 `--sort 1` 是最新。作品的 `--sort 1` 是最热，`--sort 0` 才是最新。不传作品 `--sort` 时默认最热。

`--time 2` 不是一周。一周是 `--time 7`。非法值会直接失败。

## 3. 参数

枚举和数量不在允许范围内时，命令直接失败（退出码 2，`INVALID_ARGS`），不会改成默认值再请求。三个命令都支持 `--help` / `-h`：帮助打在 stderr，退出码 0，stdout 为空，这是正常现象。短参数大小写都可以。含空格的关键词用双引号包成一个参数。关键词以 `-` 开头时写成 `--keyword=-AI`，或 `node scripts/kuaishou/search-cli.js -- -AI`。完整字段见 `assets/*_cli_req.schema.json` 与 [references/options.md](references/options.md)。

### 3.1 关键词搜索

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--keyword` `-k` | 是 | 1–50 个字符，不能是链接，不含 `< > " '` | — |
| `--sort` `-s` | 否 | `0` 综合 / `1` 最新 / `2` 最多点赞 | `0` |
| `--time` `-t` | 否 | `0` 不限 / `1` 近 1 日 / `7` 近 7 日 / `30` 近 1 月 | `0` |
| `--duration` `-d` | 否 | `0` 不限 / `1` 1 分钟内 / `2` 1–5 分钟 / `3` 超过 5 分钟 | `0` |
| `--limit` `-l` | 否 | 整数 1–10000（**包月 Token 实际最多 30**） | `10` |

### 3.2 博主作品

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 主页链接或纯数字 `user_id`，最长 255 | — |
| `--sort` `-s` | 否 | `0` 最新 / `1` 最热 | `1` |
| `--limit` `-l` | 否 | 整数 0–10000（**包月最多 50**；`0` 只要博主信息） | `10` |

### 3.3 视频评论

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 视频链接、短链或 `3x` 视频 id，最长 255 | — |
| `--limit` `-l` | 否 | 整数 1–10000（**包月最多 60**） | `10` |

## 4. 读结果

成功、空结果、失败都是同一份信封。只读 stdout 的最后一份 JSON。`--help` 时 stdout 为空，帮助在 stderr，不要把它当成命令崩溃。字段以 `assets/output_envelope.schema.json` 和 `assets/*_cli_resp.schema.json` 为准。

```json
{
  "status": "success",
  "error_code": "OK",
  "message": "搜索任务完成",
  "timestamp": "2026/10/26 16:20:00",
  "request": { "command": "search", "keyword": "具身智能", "sort": 2, "time": 0, "duration": 0, "limit": 20 },
  "metadata": { "skill_version": "1.1.1", "runtime_version": "22.22.2", "execution_time": 8421 },
  "results": [{ "id": "3xabc", "caption": "..." }]
}
```

空结果仍是退出码 0：`status` 为 `empty`，`error_code` 为 `NO_MATCH`，`results` 为 `null`。失败时 `status` 为 `error`，`results` 为 `null`，`message` 是给人读的原因。

- 搜索、评论成功时 `results` 是数组
- 作品成功时 `results` 是对象。`post` 是作品数组，`user` 是博主。`limit` 为 0 时看 `user`
- 作品视频上的点赞、播放、评论是字符串。搜索和评论里的对应字段是数字
- 搜索作者有三套标识：视频 `id` 给评论，`user.user_id` 或 `user.url` 给作品，`user.id` 是快手号

| 退出码 | error_code | 怎么处理 |
| --- | --- | --- |
| 0 | `OK` / `NO_MATCH` | 没有结果就告诉用户没有匹配内容，不要当成失败重试 |
| 2 | `INVALID_ARGS` / `INVALID_KEYWORD` | 按上一节改参数后再试一次。关键词缺失或是链接时先问用户 |
| 1 | `INVALID_URL` | 按路由换命令，或向用户确认这是视频还是主页 |
| 3 | `AUTH_REQUIRED` / `AUTH_ERROR` | 停止重试，让用户配置 `GUAIKEI_API_TOKEN` |
| 1 | `PLAN_LIMIT` | 套餐单次条数超限（常见于包月 Token）。**禁止同参重试**。转述 `message`；可建议降低 `--limit`（搜索≤30，作品≤50，评论≤60）或到官网升级按量；**须用户同意后再跑**。禁止擅自加大 limit |
| 1 | `TIMEOUT` | 任务仍在处理。大约 20 分钟内用同一组参数重跑会复用已有任务。宿主提前结束进程时不要立刻连打 |
| 1 | `NETWORK_ERROR` / `HTTP_5xx` / `HTTP_429` | 命令内部已经重试过。退出后再失败就告诉用户稍后再试，不要立刻连打 |
| 1 | 十进制数字，例如 `"12"` | 把 `message` 原样转告。不要把 `"1"` 当成业务失败，那是处理中，命令会自己等 |
| 1 | `API_ERROR` / `UNKNOWN` | 转告 `message`，建议联系官网 |

`error_code` 是字符串。查询还在处理、次数用尽时是 `TIMEOUT`，不是空结果。

## 5. 合规

只处理快手公开数据。调用时会把关键词或链接发到 `www.guaikei.com`。不上传本地文件，不登录，不发布。

成功结果默认不写文件。需要留底时设置 `KS_GUAIKEI_ENABLE_LOG=1`，文件写到系统临时目录的 `kuaishou-guaikei/logs/`。POSIX 上权限是仅当前用户可读写；Windows 不使用这组权限位，靠临时目录本身的用户隔离。

开通 token 或人工支持：[快手运营助手官网](https://www.guaikei.com)。
