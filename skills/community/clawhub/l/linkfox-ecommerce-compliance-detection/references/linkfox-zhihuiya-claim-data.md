---
name: linkfox-zhihuiya-claim-data
description: 智慧芽专利权利要求获取工具。支持查询专利的独立与从属权利要求文本、数量及范围分析。
---

# 智慧芽-专利权利要求获取（Zhihuiya Patent Claims Data）

本技能用于从智慧芽（PatSnap）专利数据库获取专利权利要求数据，帮助 IP 专业人士、专利分析师和研发团队快速查阅任意专利的权利要求部分。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过专利 ID 或公开号查询一件或多件专利的完整权利要求文本（独立权利要求与从属权利要求）。
- 返回权利要求数量，支持权利要求树、范围分析等场景。
- 支持同族专利替代：当目标专利权利要求缺失时，可选返回同族专利的权利要求。

### ❌ 边界与限制

- **至少提供一个标识**：`patentId` 与 `patentNumber` 必须至少提供其一，否则报错。
- **批量上限**：单次请求最多查询 100 件专利。
- **权利要求可用性**：并非所有专利都有权利要求数据，可用 `replaceByRelated` = `1` 尝试同族替代。
- **claim 对象结构**：`claims` 数组中各 claim 对象的结构可能因专利局和数据源不同而异。
- **不在范围内**：专利检索与发现（按关键词/主题找专利）；专利法律状态或审查历史；专利引文/引用分析；权利要求以外的专利全文（摘要、说明书、附图）；自由实施或侵权意见（法律建议）。

## 调用方式

- **API 端点**：`POST /zhihuiya/claimData`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_claim_data.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-claim-data-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 核心概念

专利权利要求界定了专利授予的法律保护范围，是侵权分析、自由实施评估和现有技术对比中最重要的部分。本工具通过专利 ID 或公开号获取一件或多件专利的完整权利要求集。

**同族替代**：当某专利权利要求在数据库中不可用时，可选择返回同族（family member）专利的权利要求作为替代，由 `replaceByRelated` 参数控制。

## 使用示例

**1. 按公开号查询单条专利**
```json
{"patentNumber": "CN115000000A"}
```

**2. 按公开号查询多条专利**
```json
{"patentNumber": "CN115000000A,US20230001234A1,EP4000000A1"}
```

**3. 按专利 ID 查询单条专利**
```json
{"patentId": "98a1b2c3-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
```

**4. 启用同族替代**
```json
{"patentNumber": "CN115000000A", "replaceByRelated": "1"}
```

**5. 批量查询并启用同族替代**
```json
{"patentNumber": "CN115000000A,JP2023100000A", "replaceByRelated": "1"}
```

## 展示规则

1. **清晰呈现权利要求**：以编号列表展示权利要求，保留原始权利要求编号；尽量用缩进或格式区分独立权利要求与从属权利要求。
2. **突出权利要求数量**：对每件专利始终说明返回的权利要求总数。
3. **同族替代提示**：若结果中存在 `pnRelated`，明确告知用户所展示权利要求来自同族专利，并提供该同族专利的公开号。
4. **批量结果**：查询多件专利时，按专利分组展示，用清晰的标题标注公开号。
5. **错误处理**：查询失败时根据响应说明原因，建议用户核实专利号格式或尝试启用同族替代。
6. **不做主观分析**：呈现原始权利要求文本，除非用户明确要求分析，否则不做法律解读。

## 用户表达与场景速查

**适用** —— 专利权利要求获取与分析：

| 用户说 | 场景 |
|--------|------|
| "看一下专利 XX 的权利要求" | 单条专利权利要求查询 |
| "获取这些专利的权利要求文本" | 批量权利要求获取 |
| "专利 XX 有多少条权利要求" | 权利要求数量查询 |
| "XX 的独立权利要求是什么" | 权利要求获取 + 展示 |
| "对比专利 A 和专利 B 的权利要求" | 多专利权利要求获取 |
| "权利要求取不到，试试同族专利" | 同族替代查询 |
| "专利权利要求范围"、"权利要求语言" | 权利要求获取 |

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

# 智慧芽-权利要求查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/claimData`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 否* | 智慧芽内部专利ID，多个用英文逗号隔开，上限100条，最大长度60000字符 |
| patentNumber | string | 否* | 公开公告号，多个用英文逗号隔开，上限100条，最大长度60000字符 |
| replaceByRelated | string | 否 | 当前专利权利要求无法获取时是否用同族专利的权利要求替代：`1` 是，`0` 否，最大长度1000字符 |

\* `patentId` 和 `patentNumber` 两个参数必须至少提供一个。如果两个都存在，会优先使用 `patentId`。


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表（详见下方） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data[] 元素结构

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开（公告）号 |
| pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |
| claims | array | 权利要求数组，包含权利要求文本及元数据 |
| claimCount | integer | 权利要求数量 |

## curl 示例

```bash
# 通过公开号查询单条专利的权利要求
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/claimData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115000000A"}'
```

```bash
# 查询多条专利的权利要求，并启用同族专利替代
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/claimData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115000000A,US20230001234A1", "replaceByRelated": "1"}'
```

```bash
# 通过专利ID查询权利要求
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/claimData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "98a1b2c3-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}'
```

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
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
