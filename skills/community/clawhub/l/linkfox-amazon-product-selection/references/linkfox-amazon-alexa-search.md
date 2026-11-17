---
name: linkfox-amazon-alexa-search
description: 模拟亚马逊前台 Alexa 购物助手，通过自然语言多轮问答获取导购建议、推荐商品分组及相关 ASIN 列表。
---

# 亚马逊 Alexa 购物助手（Amazon Alexa Shopping Assistant）

本技能驱动亚马逊前台 Alexa 购物助手：用自然语言提问，获取导购回答、推荐商品分组（含 ASIN 与链接）以及可继续追问的问题。每次调用仅支持 1 条 prompt；多轮对话需由 agent 总结上文并拼接新问题发起新请求。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过亚马逊前台 Alexa 购物助手发起自然语言问答，获取导购回答与推荐商品分组（含 ASIN、标题、价格、评分、链接）。
- 返回可继续追问的问题列表，支持 agent 总结上文后拼接新问题进行多轮对话。
- 可用 `url` 锚定具体亚马逊页面（分类页 / 搜索结果页 / 商品详情页）作为对话上下文。
- 支持 `markdown`（可读报告）与 `json`（结构化数据）两种输出格式。

### ❌ 边界与限制

- **每次仅 1 条 prompt**：`prompts` 数组只接受 1 个元素，不可一次传入多个问题。
- **无跨调用记忆**：每次调用是全新的 Alexa 会话，追问须由 agent 总结上文 + 新问题作为 `prompts[0]` 重新发起。
- **Alexa 驱动、非确定性**：相同 prompt 在不同时间/流量下可能返回不同答案。
- **站点覆盖**：主要锚定 amazon.com 前台 Alexa 体验；非美国站点的可用性取决于 Alexa 上线情况。
- **不传首页 URL**：`url` 仅在用户提供具体页面时传入；`https://www.amazon.com/` 这类首页 URL 不要传。
- **不在范围内**：关键词 SERP 全量结果与排名（用前台搜索模拟技能）；历史搜索词分析或搜索量趋势（用 ABA 数据浏览器）；已知 ASIN 的商品详情/A+/五点（用亚马逊商品详情技能）；评论情感分析（用亚马逊评论技能）；以图搜款（用图片搜索技能）；对扁平商品列表的聚合统计。

## 核心概念

1. **单轮单问题**：`prompts` 是数组但只支持 **1 个元素**，每次调用发送 1 个问题并返回 1 个回答，不要传入多个元素。
2. **跨调用无上下文**：每次调用都是全新 Alexa 会话。追问时 agent 须总结上一轮回答（关键推荐、ASIN、相关上下文），与新问题拼接后作为 `prompts[0]` 发起新请求。
3. **可选页面上下文 `url`**：仅在需要把对话锚定到**具体**亚马逊页面（分类页、搜索结果页、商品详情页）时传入。不要传 `https://www.amazon.com/` 这类首页 URL——它不提供有用上下文。无具体页面时省略 `url`。
4. **两种输出格式**：
   - `markdown`（默认）：一份可读 Markdown 报告，包含问题、Alexa 回答、推荐商品分组、可继续追问的问题。
   - `json`：`data` 下的结构化数组，每项含 `prompt`、`content`、`products`（分组推荐）、`followUpQuestions`、`screenshot`。

`resultsNum` 为 Alexa 实际答复的对话轮次；为 `0` 表示 Alexa 未对该输入产生可用回答。

## 调用方式

- **API 端点**：`POST /amazon/alexaSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_alexa_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-alexa-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 单轮购物提问**
```json
{
  "prompts": ["best wireless earbuds for running on Amazon US under $100"]
}
```

**2. 追问（agent 总结上文后重新提问）**

首次调用：
```json
{
  "prompts": ["best electric kettle on Amazon US"]
}
```

第二次调用（agent 总结上一轮回答并拼接追问）：
```json
{
  "prompts": ["Previously Alexa recommended: 1) Cosori Electric Kettle (B07T1KY5TZ, $35.99, 4.7★), 2) Mueller Ultra Kettle (B09KC7D3HR, $29.97, 4.5★). Now compare these two on noise level and boil time."]
}
```

**3. 锚定到分类页的问题**
```json
{
  "prompts": ["What are the most popular picks on this page?"],
  "url": "https://www.amazon.com/s?k=electric+kettle"
}
```

**4. 结构化输出便于下游提取**
```json
{
  "prompts": ["best gift ideas for a 10-year-old who likes science"],
  "format": "json"
}
```

## 展示规则

1. **直接渲染 Markdown**：`format=markdown` 时 `stdout` 已按轮次标题、商品卡片、追问问题结构化，保留该结构呈现。
2. **突出推荐 ASIN**：展示 `title`、`price`、`score`/`ratingsCount` 与商品 URL，便于用户点击直达。
3. **展示追问问题**：Alexa 返回的 `followUpQuestions` 是可用的继续提问选项；用户选中其一后，总结当前回答并以该问题作为 `prompts[0]` 发起新调用。
4. **不要重定向到数据分析沙箱**：回答正文是对话式的，推荐商品是嵌套分组而非适合 SQL 聚合的扁平表。
5. **标注空结果**：`resultsNum` 为 `0` 或 `data` 为空时，告知用户 Alexa 未产生可用回答，建议改写问题或用 `url` 锚定页面。
6. **说明时效**：结果反映调用时 Alexa 的实时回答；用户问及时效时说明这一点。
7. **处理业务错误**：`code`/`errcode` 非 `200` 时，呈现 `msg`/`errmsg` 并建议用更简单的问题重试。

## 用户表达与场景速查

**适用** —— 亚马逊自然语言对话式购物：

| 用户说 | 场景 |
|--------|------|
| "用 Alexa 帮我推荐...", "亚马逊 Alexa 问下..." | 直接 Alexa 问答 |
| "在亚马逊上聊聊给我推荐 ...", "对话式选品" | 对话式发现 |
| "顺便再追问一下 / 接着问 ..." | 追问（agent 总结上文后在新调用中重新提问） |
| "在这个页面 / 这个分类下推荐...", "基于这个页面再问一下" | 页面锚定对话（用 `url`） |
| "best XX for YY under $Z on Amazon" | 目标 + 约束 + 预算问答 |
| "对比 Alexa 给的前两个推荐" | 在 Alexa 回答内对比 |
| "Alexa 还能继续问什么 / 给我一些追问思路" | 呈现追问问题 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# 亚马逊 Alexa 购物助手 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/alexaSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompts | string[] | 是 | 对话提示词数组，仅支持 **1 条**。每次调用只能传入 1 个问题。如需追问，agent 须自行总结上一轮回答的关键信息（推荐商品、ASIN、关键结论等），拼接新问题后作为新的 `prompts[0]` 发起新请求。每次调用是独立的新会话，不保留跨次调用的历史上下文 |
| format | string | 否 | 响应格式，`markdown`（默认）返回可读报告；`json` 返回结构化数据数组 |
| url | string | 否 | 联动页面 URL，用于补充 Alexa 当前答复的页面上下文。仅在用户提供了**具体页面**（分类页 / 搜索结果页 / 商品详情页等）时才传入；亚马逊首页（如 `https://www.amazon.com/`）**无需传**该参数 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| stdout | string | Markdown 格式问答报告，包含每一轮的用户问题、Alexa 回答、推荐商品、可继续追问的问题；仅 `format=markdown` 时返回 |
| data | array | 结构化对话结果数组；仅 `format=json` 时返回 |
| resultsNum | integer | Alexa 实际答复的对话轮次数量；为 0 表示未产生有效回答 |
| code | string | 业务状态码，成功为 `"200"`（同 `errcode` 数值版） |
| errcode | integer | 业务状态码（HTTP 层一般为 200，业务成功与否以此字段为准） |
| msg / errmsg | string | 响应消息，成功为 `ok` |
| costTime | integer | 接口耗时，单位毫秒 |
| costToken | integer | 本次调用消耗 Token 数；上游成功才计费 |
| taskId | string | 上游返回的本次任务标识 |
| type | string | 渲染样式：`stdoutWorkbenches`（markdown）或 `json` |

### `data[*]` 结构（`format=json`）

| 字段 | 类型 | 说明 |
|------|------|------|
| prompt | string | 当前轮次发送给 Alexa 的提示词 |
| content | string | Alexa 本轮回答的文本内容 |
| screenshot | string | 本轮对话截图链接 |
| followUpQuestions | string[] | Alexa 推荐继续追问的问题列表 |
| products | array | 推荐商品分组列表，每个分组包含 `title` 和 `items` |
| products[].title | string | 推荐分组标题 |
| products[].items[].asin | string | 商品 ASIN |
| products[].items[].title | string | 商品标题 |
| products[].items[].url | string | 商品详情页 URL |
| products[].items[].cover | string | 商品封面图 URL |
| products[].items[].price | string | 现价（带币种） |
| products[].items[].originalPrice | string | 原价或划线价 |
| products[].items[].score | string | 评分 |
| products[].items[].ratingsCount | string | 评价数量 |
| products[].items[].describe | string | 商品简介 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 `errcode` / `code` 字段区分（`200` 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `stdout` 或 `data` 字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 计费/积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 其他非 200 值 | 业务异常 | 参考 `errmsg` / `msg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

**Markdown 格式（默认）：**

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/alexaSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "prompts": ["best wireless earbuds for running"]
      }'
```

**JSON 格式：**

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/alexaSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "prompts": ["best electric kettle on Amazon US"],
        "format": "json"
      }'
```

成功响应（节选）：

```json
{
  "msg": "ok",
  "errcode": 200,
  "code": "200",
  "stdout": "# 亚马逊 Alexa 购物助手\n\n## 问题 1：best wireless earbuds for running\n\n### Alexa 回答\n- ...\n\n### 推荐商品\n- ...\n\n### 可继续追问的问题\n- ...\n",
  "resultsNum": 1,
  "costTime": 12000,
  "costToken": 1500,
  "type": "stdoutWorkbenches",
  "taskId": "1779367311421-d728ce53704fc86e"
}
```
