---
name: linkfox-zhihuiya-simple-bibliography
description: 智慧芽专利核心著录数据查询工具。支持快速检索专利的公开详情、摘要、发明人、申请人及 IPC/CPC 分类号。
---

# 智慧芽专利核心著录查询（Zhihuiya Simple Bibliography）

本技能用于从智慧芽专利数据库查询专利简要著录（书目）数据，通过专利 ID 或公开号检索结构化元数据。完整参数、响应字段与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过 `patentId`（智慧芽内部专利 ID）或 `patentNumber`（公开公告号）查询专利核心著录数据。
- 返回标题、摘要、申请人、发明人、专利权人、IPC/CPC 分类号、申请日、公开日、优先权、引用文献等结构化字段。
- 支持单条与批量查询，单次最多 100 个标识符。

### ❌ 边界与限制

- **必须提供标识符**：`patentId` 与 `patentNumber` 至少传一个，否则报错。
- **patentId 优先**：两者同时传入时，仅使用 `patentId`，忽略 `patentNumber`。
- **批量上限**：单次请求最多 100 个专利 ID 或公开号。
- **数据范围**：仅返回简要著录数据，不返回全文权利要求、详细说明书、法律状态或专利族信息。
- **不在范围内**：按关键词或语义检索专利（本工具需提供具体专利标识符）；专利价值评估、自由实施分析、侵权分析。

## 核心概念

智慧芽简单著录项工具根据一个或多个专利 ID 或公开号，返回专利首页著录信息，包括标题、摘要、申请人、发明人、专利权人、分类号、申请日、公开日、优先权及引用文献等。

**查询方式**：可通过 `patentId`（智慧芽内部专利 ID）或 `patentNumber`（公开公告号）查询；两者同时提供时以 `patentId` 为准。多个值用英文逗号分隔，单次最多 100 个。

## 调用方式

- **API 端点**：`POST /zhihuiya/simpleBibliography`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_simple_bibliography.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-simple-bibliography-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单个专利**
```
用户："查一下专利 US11234567B2 的著录信息。"
动作：patentNumber = "US11234567B2"
```

**2. 按公开号批量查询**
```
用户："获取 CN115000000A、EP4000000A1、JP2023100000A 的基本信息。"
动作：patentNumber = "CN115000000A,EP4000000A1,JP2023100000A"
```

**3. 按智慧芽专利 ID 查询**
```
用户："检索专利 ID abc123 和 def456 的著录数据。"
动作：patentId = "abc123,def456"
```

**4. 获取发明人与申请人信息**
```
用户："专利 US20230001234A1 的发明人和申请人是谁？"
动作：patentNumber = "US20230001234A1"，从响应中提取 inventors 与 applicants 字段。
```

**5. 查询分类号**
```
用户："专利 EP3999999B1 有哪些 IPC 和 CPC 分类号？"
动作：patentNumber = "EP3999999B1"，展示 ipcMain、ipcFurther、cpcMain、cpcFurther 字段。
```

**6. 获取摘要与引用文献**
```
用户："看一下 CN114000000B 的摘要和引用的专利。"
动作：patentNumber = "CN114000000B"，展示 abstractContent 与 citedPatents。
```

## 展示规则

1. **清晰呈现**：单条专利用键值对布局；多条专利用表格展示最相关列。
2. **精简展示**：字段较多时优先展示标题、公开号、申请人、发明人、申请日、公开日、IPC/CPC 主分类号、摘要；其余字段按用户需要再展示。
3. **列表字段**：数组字段（发明人、申请人、专利权人、分类号、引用文献）按长度用逗号分隔或项目符号呈现。
4. **空字段**：null 或空字段直接省略，不展示空白条目。
5. **错误处理**：查询失败时根据错误信息说明原因，并建议用户核对专利号或 ID 格式。
6. **批量提示**：一次查询较多专利时，提醒单次最多 100 个。

## 用户表达与场景速查

**适用** —— 专利著录数据检索：

| 用户说 | 场景 |
|--------|------|
| "查一下专利 XX"、"获取专利 XX 的信息" | 单条专利著录查询 |
| "专利 XX 的发明人是谁"、"申请人是谁" | 发明人/申请人检索 |
| "专利 XX 的 IPC 分类号"、"XX 的分类号" | 分类号查询 |
| "看一下专利 XX 的摘要" | 摘要获取 |
| "专利 XX 什么时候申请的"、"公开日期" | 日期信息查询 |
| "专利 XX 引用了哪些专利" | 引用文献查询 |
| "查这些专利的著录数据：A、B、C" | 批量著录查询 |
| "专利基本信息"、"专利首页数据" | 通用著录检索 |

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

# 智慧芽简单著录项 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/simpleBibliography`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个专利ID之间用英文逗号 `,` 隔开，最大支持100个 |
| patentNumber | string | 条件必填 | 公开公告号（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个公开公告号之间用英文逗号 `,` 隔开，最大支持100个 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| allRecordsCount | integer | 总记录数 |
| data | array | 著录项列表（详见下方数据字段说明） |
| columns | array | 渲染的列定义 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 数据字段（`data` 数组中每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| title | string | 专利标题 |
| abstractContent | string | 专利摘要 |
| publicationNumber | string | 公开号 |
| pn | string | 公开公告号 |
| country | string | 国家代码 |
| publicationCountry | string | 公开国家 |
| publicationDate | string | 公开日期 |
| publicationKind | string | 公开类型代码 |
| patentType | string | 专利类型（发明、实用新型、外观设计等） |
| kind | string | 专利类型代码 |
| applicationNo | string | 申请号 |
| applicationDate | string | 申请日期 |
| applicants | array | 申请人列表 |
| inventors | array | 发明人列表 |
| assignees | array | 专利权人列表 |
| assigneeAddresses | array | 专利权人地址列表 |
| ipcMain | string | IPC主分类号 |
| ipcFurther | array | IPC副分类号列表 |
| cpcMain | string | CPC主分类号 |
| cpcFurther | array | CPC副分类号列表 |
| loc | array | LOC分类号列表 |
| gbc | array | GBC分类号列表 |
| priorityClaims | array | 优先权声明列表 |
| pctApplicationNo | string | PCT申请号 |
| pctFilingDate | string | PCT申请日期 |
| pctEntryDate | string | PCT进入日期 |
| citedPatents | array | 引用专利列表 |
| citedNonPatents | array | 引用非专利文献列表 |

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

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/simpleBibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US11234567B2"}'
```

### 批量查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/simpleBibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US11234567B2,CN115000000A,EP4000000A1"}'
```

### 通过专利ID查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/simpleBibliography \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "abc123,def456"}'
```
