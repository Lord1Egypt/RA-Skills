---
name: linkfox-zhihuiya-claim-data-translated
description: 智慧芽专利权利要求翻译工具。支持将专利的权利要求文本翻译并转换为中文、英文或日文版本。
---

# 智慧芽-专利权利要求翻译（Zhihuiya Patent Claims Translated）

本技能用于从智慧芽（PatSnap）专利数据库查询翻译后的专利权利要求，支持按专利 ID 或公开号检索，并返回中文、英文或日文版本的权利要求文本。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询专利的**翻译后权利要求文本**，支持中文（`cn`）、英文（`en`）、日文（`jp`）三种语言。
- 按内部专利 ID（`patentId`）或公开（公告）号（`patentNumber`）检索，单次最多 100 件专利。
- 当原专利权利要求不可获取时，可启用同族专利替代（`replaceByRelated=1`）返回相关同族专利的权利要求。

### ❌ 边界与限制

- **至少一个标识**：必须提供 `patentId` 或 `patentNumber` 之一，否则查询失败。
- **批量上限**：单次请求最多 100 件专利。
- **语言支持**：仅支持中文（`cn`）、英文（`en`）、日文（`jp`）；默认英文（`en`）。
- **同族替代**：仅当 `replaceByRelated=1` 且原专利权利要求不可获取时，才会返回同族专利的替代权利要求。
- **不在范围内**：专利检索/发现（按关键词找专利）；专利引用或法律状态分析；专利摘要或说明书获取；专利组合统计与分析。

## 核心概念

专利权利要求界定了专利授予的法律保护范围。本工具获取专利权利要求的**翻译文本**，支持中文（`cn`）、英文（`en`）、日文（`jp`）三种语言。可按内部专利 ID 或公开（公告）号检索专利。

**同族专利替代**：当某件专利的权利要求不可获取时，工具可选择用相关同族专利的权利要求替代，由 `replaceByRelated` 参数控制。

**数据字段**：

| 字段 | API 字段名 | 说明 | 示例 |
|------|-----------|------|------|
| 专利 ID | patentId | 内部专利标识 | 84a1b2c3-... |
| 公开号 | pn | 专利的公开（公告）号 | CN112345678A |
| 同族替代公开号 | pnRelated | 替代同族专利的公开号（仅在使用同族替代时出现） | US20210012345A1 |
| 权利要求 | claims | 翻译后的权利要求文本 | 1. A method for... |

**支持语言**：

| 代码 | 语言 |
|------|------|
| en | 英文（默认） |
| cn | 中文 |
| jp | 日文 |

用户未指定语言时，默认使用英文（`en`）。

## 调用方式

- **API 端点**：`POST /zhihuiya/claimDataTranslated`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_claim_translated.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-claim-data-translated-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单件专利的英文权利要求**
```
patentNumber: "CN112345678A"
lang: "en"
```

**2. 按公开号查询多件专利的中文权利要求**
```
patentNumber: "US20210012345A1,EP3456789B1"
lang: "cn"
```

**3. 查询日文权利要求并启用同族替代**
```
patentNumber: "JP2021123456A"
lang: "jp"
replaceByRelated: 1
```

**4. 按专利 ID 查询**
```
patentId: "84a1b2c3-d4e5-6f78-9abc-def012345678"
lang: "en"
```

## 展示规则

1. **清晰呈现权利要求**：以规范格式展示翻译后的权利要求文本。返回多件专利时，以公开号作为标题分隔每件专利的权利要求。
2. **同族替代提示**：响应中出现 `pnRelated` 时，明确告知用户权利要求取自相关同族专利，并展示替代公开号。
3. **语言说明**：说明返回权利要求所使用的语言，便于用户确认正在查看的翻译版本。
4. **大结果处理**：返回多件专利时，汇总数量并展示若干代表性条目，同时告知总数。
5. **错误处理**：查询失败时根据错误响应说明原因，并建议检查专利 ID 或公开号。

## 用户表达与场景速查

**适用** —— 与专利权利要求文本及翻译相关的查询：

| 用户说 | 场景 |
|--------|------|
| "查一下专利 XX 的权利要求" | 单件专利权利要求查询 |
| "把权利要求翻译成中文/日文" | 权利要求翻译 |
| "专利 XX 的权利要求是什么" | 权利要求内容获取 |
| "查这几件专利的权利要求：XX、YY" | 批量专利权利要求查询 |
| "权利要求查不到，试试同族专利" | 同族专利替代 |
| "专利 XX 的权利保护范围" | 权利要求文本获取 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 智慧芽-权利要求翻译 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/claimDataTranslated`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 否* | 专利ID，多个用英文逗号隔开，上限100条。当与 `patentNumber` 同时存在时优先使用专利ID。最大长度：60000字符 |
| patentNumber | string | 否* | 公开(公告)号，多个用英文逗号隔开，上限100条。最大长度：60000字符 |
| lang | string | 否 | 翻译语言，支持 `en`（英文，默认）、`cn`（中文）、`jp`（日语）。最大长度：1000字符 |
| replaceByRelated | integer | 否 | 权利要求无法获取时是否用同族专利替代：`1` 是，`0` 否（默认） |

> *`patentId` 和 `patentNumber` 两个参数必须至少提供一个。如果两个都存在，会优先使用 `patentId`。


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表（详见下方） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data[] 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开(公告)号 |
| pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |
| claims | string | 权利要求翻译文本 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `data` 等业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | - | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/claimDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN112345678A", "lang": "en", "replaceByRelated": 0}'
```

### 多专利查询并启用同族替代示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/claimDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US20210012345A1,EP3456789B1", "lang": "cn", "replaceByRelated": 1}'
```
