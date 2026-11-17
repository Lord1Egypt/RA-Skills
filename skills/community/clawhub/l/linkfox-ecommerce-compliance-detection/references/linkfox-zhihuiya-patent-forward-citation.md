---
name: linkfox-zhihuiya-patent-forward-citation
description: 智慧芽专利参考文献查询工具。支持查看特定专利在申请过程中引用的在先技术、专利及非专利文献。
---

# 智慧芽-专利参考文献查询（Zhihuiya Patent Forward Citation）

本技能用于从智慧芽专利数据库查询专利的前向引用详情，帮助用户了解特定专利在申请过程中引用了哪些专利与非专利文献。请求参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询特定专利的前向引用数据，返回该专利引用的专利文献（`citedPatents`）与非专利文献（`citedOthers`）。
- 支持通过专利 ID（`patentId`）或公开公告号（`patentNumber`）查询，两者同时提供时优先使用 `patentId`。
- 支持批量查询，单个参数最多 100 条，用英文逗号分隔。

### ❌ 边界与限制

- **参数必填**：`patentId` 与 `patentNumber` 至少提供一个，否则无法查询。
- **标识符优先级**：两者同时提供时优先使用 `patentId`，`patentNumber` 将被忽略。
- **数量上限**：单个参数最多 100 条，最大长度 60000 字符。
- **数据范围**：仅返回前向引用（该专利引用了哪些文献），不返回反向引用（谁引用了该专利）。
- **不在范围内**：反向/后向引用查询；专利有效性或法律状态；专利族分析；专利全文检索；专利分类或全景分析。

## 核心概念

**前向引用（Forward Citation）** 指某专利在申请文件中引用的专利与非专利文献，是专利分析的基础——了解一项专利引用了哪些在先技术，有助于评估其新颖性、保护范围与技术渊源。

- **专利引用**（`citedPatents`）：被查询专利所引用的其他专利。
- **非专利文献引用**（`citedOthers`）：被查询专利所引用的学术论文、技术报告等非专利文献。

## 调用方式

- **API 端点**：`POST /zhihuiya/patentForwardCitation`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_cited_references.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-patent-forward-citation-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开公告号查询前向引用**
> "查一下专利 US10000000B2 的前向引用。"
参数：`{"patentNumber": "US10000000B2"}`

**2. 批量查询多个专利的前向引用**
> "查专利 US10000000B2、US9876543B1 和 EP3456789A1 的全部引用。"
参数：`{"patentNumber": "US10000000B2,US9876543B1,EP3456789A1"}`

**3. 按专利 ID 查询前向引用**
> "检索专利 ID 12345678 的引用文献。"
参数：`{"patentId": "12345678"}`

**4. 同时提供两种标识符**
> "查专利 ID 12345678（公开号 US10000000B2）的引用。"
参数：`{"patentId": "12345678", "patentNumber": "US10000000B2"}`（优先使用 `patentId`）

## 展示规则

1. **清晰呈现数据**：以结构化表格展示引用结果，将专利引用与非专利文献引用分开列出。
2. **汇总数量**：始终说明被引用专利的总数与被引用非专利文献的总数。
3. **不捏造**：仅展示 API 返回的数据，不得推断或编造引用细节。
4. **错误处理**：查询失败时依据错误响应说明原因，并建议用户核实专利 ID 或公开号。
5. **批量结果**：查询多个专利时按专利分组组织结果，使每个专利的引用清晰归类。
6. **空结果**：若某专利无引用，明确告知用户，而非展示空表。

## 用户表达与场景速查

**适用** —— 专利引用查询：

| 用户说 | 场景 |
|--------|------|
| "XX 专利引用了哪些专利" | 前向引用查询 |
| "看看专利 XX 的引用文献" | 引用详情检索 |
| "XX 引用了哪些在先技术" | 在先技术引用查询 |
| "列出 XX 的引用文献" | 非专利文献引用查询 |
| "对专利 XX 做引用分析" | 专利+文献综合引用 |
| "专利 XX 引用了哪些文献" | 通用引用查询 |

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

# 智慧芽专利引用查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/patentForwardCitation`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个用英文逗号隔开，上限100条。最大长度60000字符。 |
| patentNumber | string | 条件必填 | 公开公告号（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个用英文逗号隔开，上限100条。最大长度60000字符。 |

- 每次请求至少需要提供 `patentId` 或 `patentNumber` 其中之一

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表，每个元素包含引用详情 |
| data[].patentId | string | 查询专利的专利ID |
| data[].pn | string | 查询专利的公开（公告）号 |
| data[].citedPatents | array | 引用专利列表 |
| data[].citedOthers | array | 引用非专利文献列表 |
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

### 通过公开公告号查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentForwardCitation \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10000000B2"}'
```

### 通过专利ID查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentForwardCitation \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "12345678"}'
```

### 通过公开公告号批量查询多条专利

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentForwardCitation \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10000000B2,US9876543B1,EP3456789A1"}'
```
