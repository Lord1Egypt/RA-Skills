---
name: datapilot
description: 面向所有问数与数据分析场景，基于 DataPilot 的 OpenAPI 执行从数据源接入到数据问答的完整流程。用于自然语言查数、SQL 查询校验、图表生成、报告导出下载、创建与管理数据分析 Agent、维护 Agent 知识库。
metadata:
  { "openclaw": { "requires": { "bins": ["node"], "env": ["DATAPILOT_API_URL", "DATAPILOT_API_KEY"] }, "primaryEnv": "DATAPILOT_API_KEY" } }
---

# DataAgent OpenAPI Assistant

## 何时使用

当用户要求任何"问数 / 查数 / 数据分析 / 报表"相关能力时使用本技能，包括但不限于：

- 基于数据源创建通用数据分析 Agent（面向任意业务域，不限行业）
- 自然语言问数、SQL 校验、图表展示、报告导出与下载
- 列出和检索当前全部 Agent（含描述）
- 维护 Agent 知识库（参考 SQL、业务知识、分析模板）

## 能力总览

| 能力 | CLI 命令 | 说明 |
|------|----------|------|
| 创建 DataAgent 实例 | `create-instance` | 一步完成 agent 创建，接入数据源 |
| 自然语言问数 | `ask` | SSE 对话，返回 SQL / 表格 / 图表 / 报告下载链接 |
| 列出全部 Agent | `list-agents` | 跨 namespace 汇总所有 agent 信息 |
| 查看知识库 | `knowledge-list` | 列出指定 agent 的知识条目（可按类型过滤） |
| 新增/更新知识 | `knowledge-upsert` | 新增或覆盖一条知识（reference_sql / business_knowledge / analysis_template） |
| 查看知识条目 | `knowledge-get` | 获取单条知识详情 |
| 删除知识条目 | `knowledge-delete` | 删除一条知识 |

## 核心流程

```
用户需求
  │
  ├─ 首次使用 ──► create-instance（接入数据源，创建 Agent）
  │                    │
  │                    ▼
  │              返回 namespaceId + agentId
  │
  ├─ 问数分析 ──► ask（传入 agentId + 自然语言问题）
  │                    │
  │                    ▼
  │              SSE 流式返回：SQL / 表格 / 图表 / 报告下载链接
  │
  ├─ 查看 Agent ► list-agents（列出所有可用 Agent）
  │
  └─ 知识管理 ──► knowledge-list / knowledge-upsert / knowledge-get / knowledge-delete
```

## 配置与鉴权

- **API 基础前缀**：`/api`
- **响应格式**：`{ code, message, data }`，`code === 0` 视为成功
- **鉴权**：Header `Authorization: Bearer <token>`
- **语言**：Header `X-Lang: zh`

## 调用方式

所有能力通过 Node 脚本 `dataagent_openapi_cli.mjs` 调用。

```bash
node dataagent_openapi_cli.mjs <command> [options]
```

### 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--base-url` | API 服务地址 | 环境变量 `DATAPILOT_API_URL` |
| `--token` 或 `--apiKey` | 鉴权令牌 | 环境变量 `DATAPILOT_API_KEY` |


## 命令详解

### 1. create-instance — 创建 DataAgent 实例

创建一个 agent 实例，提供问数，数据分析等能力。


**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | 是 | 实例名称（同时作为 namespace 和 agent 名） |
| `--description` | 否 | 实例描述（推荐模板：`[业务域] + [核心指标] + [时间粒度] + [场景]`） |
| `--datasource-file` | 二选一 | 数据源 JSON 配置文件路径 |
| `--datasource-json` | 二选一 | 数据源 JSON 字符串 |
| `--sqlite-file` | 条件 | SQLite 类型且无 uri 时，需提供 .db 文件路径上传 |

**数据源配置格式：**

| 类型 | 必填字段 |
|------|----------|
| `sqlite` | `{ type: "sqlite", uri }` — 或通过 `--sqlite-file` 上传后自动填充 |
| `mysql` | `{ type, host, port, username, password, database, schema? }` |
| `postgresql` | `{ type, host, port, username, password, database, schema? }` |
| `odps` | `{ type: "odps", access_id, access_key, project, endpoint, schema? }` |
| `oboracle` | `{ type: "oboracle", host, port, username, password, tenant, cluster?, database? }` |

**示例：**

```bash
node dataagent_openapi_cli.mjs create-instance \
  --name "sales_copilot" \
  --description "销售经营分析，覆盖GMV/转化率/复购，按日周月输出。" \
  --datasource-file ./datasource.json
```

**返回：**

```json
{
  "namespaceId": "ns_xxx",
  "agentId": "agent_xxx",
  "name": "sales_copilot",
  "description": "销售经营分析...",
  "tablesCount": 12,
  "datasourceType": "mysql"
}
```

---

### 2. ask — 自然语言问数

通过 SSE 对话接口进行问数，返回流式事件和下载链接。

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--namespace-id` | 是 | 目标 namespace ID |
| `--agent-id` | 是 | 目标 agent ID |
| `--input` | 是 | 自然语言问题 |
| `--session-id` | 否 | 会话 ID（多轮对话时传入） |
| `--role` | 否 | 角色标识 |

**示例：**

```bash
node dataagent_openapi_cli.mjs ask \
  --namespace-id ns_xxx \
  --agent-id agent_xxx \
  --input "按周分析最近90天GMV变化并生成周报"
```

**返回：**

```json
{
  "sessionId": "sess_xxx",
  "content": "最终回复文本（Markdown 格式，含表格、图表、报告等）",
  "downloadUrls": ["http://localhost:3000/api/sub-agents/.../download/files/..."],
  "status": "completed"
}
```

| 字段 | 说明 |
|------|------|
| `content` | 最终回复文本（由所有 text block 拼接而成） |
| `sql` | 执行过的 SQL 语句列表 |
| `downloadUrls` | 从回复中提取的可下载文件绝对 URL |
| `status` | `completed`（成功）或 `failed`（出错） |

---

### 3. list-agents — 列出全部 Agent

跨 namespace 汇总所有 agent 信息。

**参数：** 仅通用参数。

**示例：**

```bash
node dataagent_openapi_cli.mjs list-agents 
```

**返回：** 数组，每项包含 `agentId` / `name` / `description` / `namespaceId` / `namespaceName` / `datasourceType` / `updatedAt`。

---

### 4. knowledge-list — 查看知识库

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--namespace-id` | 是 | 目标 namespace ID |
| `--agent-id` | 是 | 目标 agent ID |
| `--knowledge-type` | 否 | 按类型过滤：`reference_sql` / `business_knowledge` / `analysis_template` |

**示例：**

```bash
node dataagent_openapi_cli.mjs knowledge-list \
  --namespace-id ns_xxx --agent-id agent_xxx
```

---

### 5. knowledge-upsert — 新增/更新知识

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--namespace-id` | 是 | 目标 namespace ID |
| `--agent-id` | 是 | 目标 agent ID |
| `--knowledge-type` | 是 | 类型：`reference_sql` / `business_knowledge` / `analysis_template` |
| `--name` | 是 | 知识条目名称（推荐：`业务域_主题_版本`） |
| `--content` | 是 | 知识内容（SQL / 术语定义 / 模板文本） |

**示例：**

```bash
node dataagent_openapi_cli.mjs knowledge-upsert \
  --namespace-id ns_xxx --agent-id agent_xxx \
  --knowledge-type reference_sql \
  --name weekly_gmv_v1 \
  --content "SELECT date_trunc('week', order_date) AS week, SUM(amount) AS gmv FROM orders GROUP BY 1"
```

---

### 6. knowledge-get — 查看知识条目

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--namespace-id` | 是 | 目标 namespace ID |
| `--agent-id` | 是 | 目标 agent ID |
| `--knowledge-type` | 是 | 知识类型 |
| `--name` | 是 | 知识条目名称 |

**示例：**

```bash
node dataagent_openapi_cli.mjs knowledge-get \
  --namespace-id ns_xxx --agent-id agent_xxx \
  --knowledge-type reference_sql --name weekly_gmv_v1
```

---

### 7. knowledge-delete — 删除知识条目

**参数：** 同 `knowledge-get`。

**示例：**

```bash
node dataagent_openapi_cli.mjs knowledge-delete \
  --namespace-id ns_xxx --agent-id agent_xxx \
  --knowledge-type reference_sql --name weekly_gmv_v1
```

---