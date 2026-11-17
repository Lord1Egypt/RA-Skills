---
name: linkfox-zhihuiya-abstract-data-translated
description: 智慧芽专利标题与摘要翻译工具。支持通过专利 ID 或公开号获取中、英、日等跨语言的专利翻译内容。
---

# 智慧芽专利标题与摘要翻译（Zhihuiya Abstract Data Translated）

本技能用于从智慧芽（PatSnap）专利数据库获取专利标题和摘要的翻译版本，支持中文、英文、日文翻译。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过**专利 ID**（`patentId`）或**公开号**（`patentNumber`）查询专利，返回其标题与摘要的翻译版本。
- 支持中、英、日三种目标翻译语言（`lang`：`cn`/`en`/`jp`）。
- 支持批量查询：多个专利 ID 或公开号用英文逗号分隔一次提交。
- 支持同族专利摘要回退：当原专利无摘要时，可启用 `replaceByRelated = 1` 用同族专利摘要替代。

### ❌ 边界与限制

- **必须提供标识符**：至少需要 `patentId` 或 `patentNumber` 之一，工具不支持按关键词检索专利。
- **翻译语言有限**：仅支持中文（`cn`）、英文（`en`）、日文（`jp`）。
- **仅返回标题与摘要**：不返回权利要求、说明书等专利全文。
- **同族替代为可选项**：仅当显式设置 `replaceByRelated = 1` 时才提供同族专利替代摘要。
- **不在范围内**：专利全文/权利要求获取；按关键词、分类号、申请人检索专利；专利法律状态、引证分析、专利全景报告；专利估值或侵权分析。

## 核心概念

智慧芽（PatSnap）是领先的专利情报平台。本工具查询其数据库，返回一条或多条专利的翻译标题与摘要。

**专利标识**：每条专利可通过 `patentId`（智慧芽内部 ID）或 `patentNumber`（公开号/公告号，如 `US20200012345A1`、`CN112345678A`）标识。若同时提供两者，优先使用 `patentId`。

**同族专利回退**：当原专利无可用摘要时，可启用替代选项，使用相关同族专利的摘要。

## 调用方式

- **API 端点**：`POST /zhihuiya/abstractDataTranslated`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_abstract_translated.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-abstract-data-translated-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号翻译单条专利摘要为英文**
```
查一下公开号 US20200012345A1 的英文摘要。
```
参数：`patentNumber = "US20200012345A1"`, `lang = "en"`

**2. 批量翻译多条专利为中文**
```
把 CN112345678A 和 US20200067890A1 的摘要翻译成中文。
```
参数：`patentNumber = "CN112345678A,US20200067890A1"`, `lang = "cn"`

**3. 按专利 ID 查询并启用同族回退**
```
查专利 ID 12345678 的日文摘要，如果摘要不可用就用同族专利替代。
```
参数：`patentId = "12345678"`, `lang = "jp"`, `replaceByRelated = 1`

**4. 按专利 ID 批量查询**
```
翻译这些专利 ID 的标题和摘要：111111、222222、333333。
```
参数：`patentId = "111111,222222,333333"`, `lang = "en"`

## 展示规则

1. **清晰呈现数据**：以结构化表格展示公开号、标题、摘要。
2. **标明语言**：在输出标题中注明翻译语言，便于用户确认结果语种。
3. **同族专利提示**：若结果中出现 `pnRelated`，明确告知用户该摘要取自同族专利，并展示替代公开号。
4. **长摘要处理**：摘要较长时完整展示，不截断，便于用户审阅完整内容。
5. **错误处理**：查询失败或无结果时，说明可能原因（如公开号无效、数据库中未找到该专利）并给出修正建议。
6. **不做主观评论**：仅原样呈现翻译文本，不对专利内容做解读或法律分析。

## 用户表达与场景速查

**适用** —— 专利摘要与标题翻译查询：

| 用户说 | 场景 |
|--------|------|
| "翻译这个专利的摘要" | 单条专利翻译 |
| "专利 XX 说了什么 / 是关于什么的" | 摘要查阅 |
| "把这个专利翻译成中文/日文" | 指定语言翻译 |
| "查一下公开号 XX 的摘要" | 按公开号查询 |
| "批量翻译这些专利" | 批量翻译 |
| "摘要缺失，试试同族专利" | 同族专利回退 |

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

# 智慧芽摘要翻译 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/abstractDataTranslated`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | patentId 和 patentNumber 至少填一个 | 智慧芽内部专利ID，多个用英文逗号隔开。最大长度 60,000 字符 |
| patentNumber | string | patentId 和 patentNumber 至少填一个 | 公开(公告)号，多个用英文逗号隔开。最大长度 60,000 字符 |
| replaceByRelated | integer | 否 | 摘要无法获取时是否用同族专利摘要替代：`1` 是，`0` 否。默认 `0` |
| lang | string | 否 | 翻译目标语言。可选值：`en`（英文，默认）、`cn`（中文）、`jp`（日语）。最大长度 1,000 字符 |

- `patentId` 和 `patentNumber` 至少需要提供一个。如果两个都存在，会优先使用 `patentId`

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 返回的专利记录数 |
| data | array | 专利列表 |
| data[].patentId | string | 智慧芽内部专利ID |
| data[].pn | string | 公开(公告)号 |
| data[].title | string | 标题翻译 |
| data[].abstractText | string | 摘要翻译 |
| data[].pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

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
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/abstractDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US20200012345A1", "lang": "en", "replaceByRelated": 0}'
```

### 批量查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/abstractDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN112345678A,US20200067890A1", "lang": "cn", "replaceByRelated": 1}'
```
