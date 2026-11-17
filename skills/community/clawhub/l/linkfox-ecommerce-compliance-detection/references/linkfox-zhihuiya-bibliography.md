---
name: linkfox-zhihuiya-bibliography
description: 智慧芽专利详细著录信息查询工具。支持查询申请人、发明人、分类号、引用关系及优先权等完整元数据。
---

# 智慧芽-专利详细著录信息查询（Zhihuiya Patent Bibliography）

本技能用于通过专利ID或公开号查询智慧芽专利数据库中的专利著录（书目）信息，帮助用户获取特定专利的完整元数据。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过**专利ID**或**公开号**查询专利著录信息，单次请求最多 100 条。
- 返回字段覆盖：标题、摘要、专利类型、申请人、当前专利权人、发明人、代理人/代理机构、审查员、优先权声明、申请/公开引用数据、IPC/CPC/UPC/LOC/FI/F-term/GBC 分类号、引用专利与非专利文献、分案/继续申请、PCT 数据、预估到期日等。

### ❌ 边界与限制

- **输入要求**：`patentId` 与 `patentNumber` 至少提供一个；二者同时存在时优先使用 `patentId`。
- **数量上限**：单次请求最多 100 条，参数最大长度 60,000 字符。
- **不在范围内**：按关键词/语义的全文本专利检索、专利全景分析报告、专利估值或法律状态跟踪、FTO/侵权分析、专利族树探索（除非给定具体公开号）。当用户说"查找关于 X 的专利"或"在 Y 领域检索专利"时属于专利检索任务，不适用本技能。
- **数据时效**：著录数据来自智慧芽专利数据库，依赖其更新周期。

## 核心概念

专利著录数据（书目信息）是与专利文档关联的结构化元数据，包含标题、申请人、发明人、分类号、优先权声明、引用文献、摘要等。本工具支持按 **专利ID** 或 **公开号** 查询，单次最多返回 100 条专利的完整著录记录。

**专利类型**（`patentType` 字段）：
- `APPLICATION` —— 发明申请（已公开未授权）
- `PATENT` —— 授权发明专利
- `UTILITY` —— 实用新型
- `DESIGN` —— 外观设计

## 调用方式

- **API 端点**：`POST /zhihuiya/bibliography`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_bibliography.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-bibliography-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单条专利**
```
用户："查一下 US10123456B2 的著录信息"
动作：patentNumber = "US10123456B2"
```

**2. 按公开号批量查询**
```
用户："获取 CN112345678A、EP3456789B1、US20210012345A1 的著录数据"
动作：patentNumber = "CN112345678A,EP3456789B1,US20210012345A1"
```

**3. 按专利ID查询**
```
用户："查询专利ID 8fa3b2c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx 的著录信息"
动作：patentId = "8fa3b2c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**4. 批量查询发明人与专利权人**
```
用户："我有 20 个公开号，查一下它们的发明人和专利权人"
动作：patentNumber = "<逗号分隔的列表>"
随后从结果中抽取并展示发明人与专利权人。
```

## 展示规则

1. **清晰呈现数据**：以结构化表格或组织良好的分区展示每条专利，重点突出常用字段：标题、申请人/专利权人、发明人、申请/公开日期、分类号、摘要。
2. **遵循查询范围**：只展示用户询问的字段。若用户只要"发明人"，除非用户要求否则不要倾倒全部著录信息。
3. **专利类型标签**：将 `patentType` 代码翻译为可读标签（APPLICATION = 发明申请，PATENT = 授权发明，UTILITY = 实用新型，DESIGN = 外观设计）。
4. **多专利结果**：结果含多条专利时先用汇总表，再按用户需要展开单条详情。
5. **错误处理**：查询返回错误或空结果时清晰说明，并建议用户核对专利ID或公开号。
6. **不做主观分析**：只呈现事实性著录数据，不做推测性的法律或商业解读。

## 用户表达与场景速查

**适用** —— 专利著录/元数据查询：

| 用户说 | 场景 |
|--------|------|
| "查一下 XX 专利的信息" | 单条专利著录 |
| "XX 专利的发明人是谁" | 发明人查询 |
| "XX 专利是谁的"、"当前专利权人" | 专利权人/申请人查询 |
| "XX 专利的 IPC/CPC 分类是什么" | 分类号查询 |
| "看一下 XX 专利的摘要" | 摘要获取 |
| "XX 专利引用了哪些专利" | 引用分析 |
| "XX 专利什么时候到期" | 到期日查询 |
| "查这几个专利的著录信息：A、B、C" | 批量查询 |
| "专利详情"、"专利元数据" | 通用著录查询 |

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

# 智慧芽-著录项目 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/bibliography`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 否* | 专利ID（专利id和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利id），多个用英文逗号隔开，上限100条，最大长度60,000字符 |
| patentNumber | string | 否* | 公开公告号（专利id和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利id），多个用英文逗号隔开，上限100条，最大长度60,000字符 |

> \* `patentId` 和 `patentNumber` 至少需要提供一个。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 著录项目数据列表（详见下方数据字段） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 数据字段（`data` 数组中的每个对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开公告号 |
| inventionTitle | array | 专利标题语言和名称 |
| abstracts | array | 专利摘要 |
| patentType | string | 专利类型，其中APPLICATION：发明申请，PATENT：授权发明，UTILITY：实用新型，DESIGN：外观设计 |
| applicants | array | 原始申请人 |
| assignees | array | 当前申请(专利权)人 |
| inventors | array | 发明人 |
| agents | array | 专利申请人 |
| agency | array | 申请代理机构 |
| examiners | array | 审查员信息 |
| priorityClaims | array | 优先权声明 |
| applicationReference | object | 申请文件引用数据 |
| publicationReference | object | 公开文件引用数据 |
| datesOfPublicAvailability | object | 公开可用日期 |
| classificationIpcr | object | IPC分类号 |
| classificationCpc | object | CPC分类号 |
| classificationUpc | object | 美国专利分类号 |
| classificationLoc | array | LOC分类号 |
| classificationFi | array | FI分类号 |
| classificationFterm | array | F_term分类号 |
| classificationGbc | object | GBC分类号 |
| referenceCitedPatents | array | 引用专利文献 |
| referenceCitedOthers | array | 引用非专利文献 |
| relatedDocuments | array | 分案继续申请信息 |
| pctOrRegionalFilingData | object | PCT或区域阶段申请数据 |
| pctOrRegionalPublishingData | object | PCT或区域阶段公开数据 |
| exdt | integer | 智慧芽专利预估到期日 |

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

## curl 示例

**通过公开公告号查询（单条专利）：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/bibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2"}'
```

**通过专利ID查询：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/bibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "some-patent-id-here"}'
```

**通过公开公告号查询多条专利：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/bibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2,CN112345678A,EP3456789B1"}'
```
