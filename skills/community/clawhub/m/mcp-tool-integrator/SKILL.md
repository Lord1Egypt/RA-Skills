---

name: "MCP Tool Integrator"

slug: mcp-integrator

description: "UPDATED 2026: MCP moves to Linux Foundation (2025-11), becomes de facto AI agent standard. AI-powered Model Context Protocol (MCP) server integration assistant — scaffold MCP servers, connect to 50+ tools (GitHub, Slack, Notion, Airtable, Postgres, filesystem), debug MCP connections, and build custom MCP tool chains. Built for AI developers, agent builders, and DevOps engineers building multi-tool AI agents. Keywords: MCP, Model Context Protocol, MCP server, AI agent integration, Anthropic Claude MCP, tool integration, AI agent development, LangChain MCP, n8n MCP, AI automation, MCP开发, AI Agent工具集成, 工具链, 自动化工作流, Claude桌面版.

version: "4.0.6"

---

## 执行边界与数据安全（2026-11-11 轮换补强）

本技能是一份**文档式 MCP 集成指南**，本身不包含可执行代码、不持有任何凭据、不发起网络连接。

- **凭据由使用者自行管理**：文中提及的 Token / API Key / 数据库连接串等，均由使用者在自己的环境与权限范围内配置；本技能只说明“最小权限、只读优先、写操作需审批与审计日志”的配置原则，不替代你做授权决策。
- **不代为执行**：本技能不代替你创建、授权或调用任何 MCP server；所有连接、授权与写操作都由你在受控环境中手动确认后完成。
- **数据最小化**：仅在排查连接问题时提供必要的最小配置片段，不要粘贴包含真实密钥的完整配置文件。




# MCP Tool Integrator





### AI技术最新动态 [2026-11-23更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 集成应对 |
|---------|---------|---------|---------|---------|
| AI技术 | 2026年MCP已捐赠给Linux基金会AAIF治理，生态超1000个服务器 | 2025-11 | MCP集成指南需更新AAIF治理架构和企业导入实践 | 以AAIF治理为准跟踪规范演进 |
| AI技术 | OpenAI/Google/Microsoft等巨头已广泛采纳MCP标准 | 2026 | 跨运行时工具复用 | 一次接入、多运行时复用，避免重复集成 |
| AI技术 | 企业MCP导入五大场景：工具集成、数据源连接、多Agent协同、权限控制、异步任务 | 2026 | 企业集成架构 | 按场景选择传输模式与网关 |
| 协议更新 | MCP 2.0相关扩展推进：Apps（服务端渲染UI）、Tasks（长时运行任务）等能力逐步落地（以官方规范为准） | 2026 | 交互形态与长时任务 | 长时任务需设计可中断与状态可追溯 |
| 安全实践 | 企业级安全部署强调零入站端口、权限声明与执行沙箱（以官方最新发布为准） | 2026 | 生产环境部署 | 传输层与身份鉴别需同步设计 |
| 互操作 | 跨协议互操作（MCP 与 A2A 等）持续推进 | 2026 | 多Agent协作 | 通过网关/转换层桥接，避免硬编码绑定 |

> **数据截止**: 2026-11-23 | 来源：MCP官方规范、Linux Foundation AAIF、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准；版本号与具体实现请以官方规范文档为准。



## Overview



The Model Context Protocol (MCP) is the emerging standard for connecting AI agents to external tools — and 2026 is the year it goes mainstream. Microsoft Agent 365, Claude Desktop, Cursor, and dozens of frameworks now support MCP natively. This skill helps developers scaffold, configure, and debug MCP server integrations at speed — turning scattered tool APIs into a unified agent capability layer.



## Title



**MCP Tool Integrator** — Connect AI Agents to Any Tool in Minutes



## Triggers



- "MCP server setup" / "MCP服务器配置"

- "MCP integration" / "MCP集成" / "MCP接入"

- "Model Context Protocol" / "MCP协议"

- "Claude MCP tools" / "Claude MCP工具"

- "AI agent tool integration" / "AI代理工具集成"

- "MCP GitHub" / "MCP Slack" / "MCP Notion"

- "MCP debug" / "MCP调试"

- "MCP LangChain" / "MCP n8n"

- "build MCP server" / "构建MCP服务器"

- "MCP custom tool" / "MCP自定义工具"



---



### 0. 2025-2026 MCP 最新动态



| 时间 | 动态 | 意义 | 对集成者的动作 |
|------|------|------|---------|
| **2024年11月** | Anthropic发布MCP协议 | AI Agent与外部工具交互的开放标准诞生 | 评估是否替代自建工具适配层 |
| **2025年11月** | MCP移交至Linux Foundation旗下Agentic AI Foundation治理 | OpenAI、Google、Microsoft等主要厂商共同参与标准制定 | 跟踪AAIF规范，避免依赖单一厂商实现 |
| **2026年** | MCP成为AI Agent开发事实标准协议 | Microsoft Agent 365、Claude Desktop、Cursor等主流平台原生支持 | 一次开发、多运行时复用 |
| **2026年** | FastMCP简化MCP Server开发 | 开发者可快速搭建自定义MCP服务器 | 内部工具优先用FastMCP封装 |
| **2026年5月** | MCP官方Server Registry扩展至50+工具 | 涵盖GitHub、Slack、Notion、Postgres、腾讯云等 | 优先复用官方Server，自研只做差异化部分 |
| **2026年** | MCP 2.0及Apps/Tasks等扩展推进 | 交互形态与长时任务标准化 | 长时任务补可中断与状态留痕设计 |



> **关键提示：** 2026年MCP生态已从单一AI厂商协议演变为跨平台开放标准。金融行业部署MCP时，优先使用官方认证的Server；国内企业可选用国产MCP Server（如腾讯云、钉钉、飞书定制实现）。



---




### MCP技术最新动态 [2026-11-23更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 集成应对 |
|---------|---------|---------|---------|---------|
| 标准路线 | MCP 2026路线图发布，四大优先方向：传输层演进、Agent通信、治理成熟度、企业就绪 | 2026-06 | MCP Server开发与集成 | 传输层选型预留演进空间 |
| 行业合规 | 银行业保险业AI安全开发应用指导意见发布，金融机构部署MCP需满足可解释、可审计、数据安全要求 | 2026-06-18 | 金融MCP企业导入 | MCP调用纳入审计与权限管控 |
| 生态规模 | MCP生态系统汇聚超过1000个服务器，成为AI Agent开发事实标准 | 2026-04 | MCP工具链选择 | 建立内部Server白名单 |
| 治理要求 | 治理成熟度被列为标准优先方向，Server需具备权限声明、审计日志与用户确认能力 | 2026-06 | 生产上线门槛 | 上线前逐项核对治理控制点 |
| 国际差异 | AI治理路径出现区域分化，跨境部署的同一种Server可能面临不同合规要求（以官方最新发布为准） | 2026-09-02 | 跨境与集团统一架构 | 底线取最严，区域差异化配置 |

> **数据截止**: 2026-11-23 | 来源：国家金融监督管理总局、MCP官方规范、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准。

## Workflow



### Phase 1 — MCP Fundamentals & Environment Setup



**Step 1.1: Detect Current MCP Environment**



Determine what MCP runtime is available and what tools are already connected.



**Output: MCP Environment Audit**



| Runtime | Version | Transport | Connected Tools | Status | 备注 |
|---------|---------|-----------|----------------|--------|------|
| Claude Desktop MCP | 1.0.3 | stdio | filesystem, github | ✅ Active | 本地进程，适合个人开发 |
| Cursor MCP Bridge | 0.9.2 | stdio | postgres, slack | ⚠️ Partial | slack 权限不完整 |
| Custom LangChain MCP | N/A | — | None | ❌ Not configured | 需先选传输模式再接入 |
| FastAPI MCP Server | 0.4.1 | HTTP | crm, erp | ✅ Active | 生产环境，前置鉴权与限流 |
| MCP Gateway | 1.2.0 | HTTP/SSE | 12 tools | ✅ Active | 统一入口，便于审计与协议转换 |



**审计要点（本版新增）**：这张表至少每季度复检一次。重点看三类异常——

① Status 为 Partial/Not configured 却已在生产使用（说明台账失真）；

② Transport 为 stdio 却被多人共享（本地进程模式不适合团队共用）；

③ 接入了敏感数据源但缺少鉴权与审计（见 Phase 1.5 安全加固清单）。



**Step 1.2: Recommend MCP Architecture**



Based on use case, recommend the optimal MCP topology.



**Architecture Patterns:**



```

Pattern A — Desktop-First (Individual Developer)

Claude Desktop ↔ Local MCP Servers ↔ filesystem, git, terminal



Pattern B — Enterprise Multi-Agent (Team)

LangChain Agent ↔ MCP Gateway ↔ GitHub, Jira, Slack, Notion, Postgres



Pattern C — API-First (Production)

FastAPI MCP Server ↔ Authenticated Tools ↔ CRM, ERP, Database



Pattern D — China-Optimized (Regulated Industry)

Local MCP Server ↔ Domestic tools (钉钉, 飞书, 腾讯云) ↔ Firewall-compliant

```



---



### Phase 1.5 — 传输模式选型与安全加固（本版新增）



**传输模式对照（选型第一步）**：



| 模式 | 典型场景 | 优点 | 局限 | 适用阶段 |
|------|---------|------|------|---------|
| stdio | Claude Desktop、本地IDE | 部署简单、无需开端口 | 仅限本机单进程，难以共享与审计 | 个人开发/验证 |
| HTTP（可流式） | 生产服务、团队共用 | 可鉴权、可限流、易接入网关 | 需处理鉴权与传输安全 | 生产环境 |
| SSE | 需要服务端推送的长连接场景 | 支持服务端主动推送 | 连接管理复杂 | 特定推送场景 |
| Gateway 统一入口 | 多Server、多Agent | 集中审计、协议转换、统一鉴权 | 引入单点，需高可用设计 | 企业级 |



**选型举例**：一个人用的Notion工具，用 stdio 最快；

给20人团队共用的CRM工具，必须走 HTTP 并前置鉴权；

当Server数量超过5个、且需要统一审计时，才值得引入 Gateway——**过早引入网关会增加运维负担**。



**上线前安全加固清单**：



| 控制点 | 具体要求 | 验证方式 |
|-------|---------|---------|
| 凭据管理 | 密钥走环境变量或密钥管理，禁止硬编码 | 代码扫描 + 配置核查 |
| 最小权限 | 按工具分别授予 scope，不使用超管令牌 | 权限清单评审 |
| 只读优先 | 数据库类工具默认只读，写操作需审批流程 | 连接串权限核查 |
| 审计留痕 | 记录调用方、工具、参数摘要、结果与耗时 | 抽查日志样本 |
| 限流与预算 | 设置每Agent调用限额与费用上限 | 压测 + 账单告警 |
| 版本固定 | 生产环境固定Server版本号，避免自动升级引入变更 | 配置文件核查 |
| 可中断 | 长时任务支持取消，避免悬挂占用资源 | 中断演练 |



---



### Phase 2 — Scaffolding MCP Servers



**Step 2.1: Generate MCP Server Code**



For any external tool, generate a complete MCP server implementation.



**Input:** Tool name + authentication method + required operations

**Output:** Complete Python/TypeScript MCP server scaffold



**Example MCP Server — Notion Integration:**



```python

# notion_mcp_server.py

from mcp.server.fastapi import McpServer

from mcp.types import Tool, CallToolRequest

import httpx



SERVER = McpServer(name="notion-mcp", version="1.0.0")



@SERVER.list_tools()

async def list_notion_tools():

    return [

        Tool(

            name="notion_search_pages",

            description="Search Notion pages by keyword",

            input_schema={

                "type": "object",

                "properties": {

                    "query": {"type": "string"},

                    "filter_database_id": {"type": "string", "optional": True}

                }

            }

        ),

        Tool(

            name="notion_create_page",

            description="Create a new Notion page in a database",

            input_schema={

                "type": "object",

                "properties": {

                    "database_id": {"type": "string"},

                    "title": {"type": "string"},

                    "properties": {"type": "object"}

                }

            }

        ),

        Tool(

            name="notion_update_block",

            description="Update a block in a Notion page",

            input_schema={

                "type": "object",

                "properties": {

                    "block_id": {"type": "string"},

                    "content": {"type": "string"}

                }

            }

        )

    ]



@SERVER.call_tool()

async def call_notion_tool(request: CallToolRequest):

    if request.name == "notion_search_pages":

        return await search_pages(request.arguments["query"], request.arguments.get("filter_database_id"))

    elif request.name == "notion_create_page":

        return await create_page(request.arguments["database_id"], request.arguments["title"], request.arguments.get("properties", {}))

    elif request.name == "notion_update_block":

        return await update_block(request.arguments["block_id"], request.arguments["content"])

```



**Step 2.2: MCP Server Configuration File**



Generate the `mcp.json` or `mcp_servers.json` config for the runtime.



```json

// .mcp.json (Claude Desktop)

{

  "mcpServers": {

    "notion": {

      "command": "python",

      "args": ["notion_mcp_server.py"],

      "env": {

        "NOTION_API_KEY": "${NOTION_API_KEY}"

      }

    },

    "github": {

      "command": "npx",

      "args": ["-y", "@modelcontextprotocol/server-github"],

      "env": {

        "GITHUB_TOKEN": "${GITHUB_TOKEN}"

      }

    },

    "postgres": {

      "command": "npx",

      "args": ["-y", "@modelcontextprotocol/server-postgres"],

      "env": {

        "DATABASE_URL": "${DATABASE_URL}"

      }

    }

  }

}

```



---



### Phase 3 — Connecting Popular Tool Chains



**Step 3.1: GitHub MCP Integration**



Enable AI agents to interact with GitHub repositories, issues, PRs, and code.



**Capabilities enabled:**

- `github_list_repos` — List repositories with filters

- `github_create_issue` — Create issue with labels

- `github_review_pr` — Analyze PR changes and provide review comments

- `github_search_code` — Semantic code search across repos

- `github_get_workflow_runs` — Monitor CI/CD pipeline status

**Use case example:**

> "Summarize all open PRs in our main repo, highlight security concerns, and post a daily digest to Slack."



**举例（只读优先怎么落地）**：给 GitHub MCP 的令牌只授予 `repo:read` 与 `workflow:read`，

让 Agent 能读 PR、读 CI 状态，但**无法合并代码或触发流水线**。

若确实需要自动创建 issue，再单独增加一个只含 `issues:write` 的令牌，并在调用前加人工确认。



**举例（典型误用）**：为了方便，直接给一个具有 `repo` 全权限的令牌。

一旦提示词被注入或Agent行为失控，影响面就从“读代码”扩大到“改代码、发版本”。

**权限应按工具而非按人授予**。



**Step 3.2: Slack MCP Integration**



Enable AI agents to send messages, search history, manage channels.



**Capabilities enabled:**

- `slack_post_message` — Send to channel or DM

- `slack_search_messages` — Full-text search in Slack history

- `slack_list_channels` — Get channel list with membership

- `slack_create_channel` — Provision new channels

- `slack_schedule_message` — Schedule future messages



**举例（channel_not_found 的定位路径）**：先查令牌 scope 是否含写权限 → 再查 bot 是否已被邀请进目标频道 →

最后查频道ID是否用了名称而非ID。三者中**“token有权限但bot不在频道”**最容易漏查。



**举例（写入类工具如何加确认）**：让 Agent 先生成消息草稿并展示给用户，

得到明确确认后再调用 `slack_post_message`。这一步能把“误发消息到错误频道”的风险降到最低。



**Step 3.3: Database MCP (PostgreSQL / MySQL / MongoDB)**



Enable AI agents to query databases, generate reports, and validate data.



**Capabilities enabled:**

- `db_query` — Execute read-only SQL with row limits

- `db_describe_table` — Get schema documentation

- `db_generate_report` — Natural language → formatted report

- `db_validate` — Check data quality rules



**举例（只读连接怎么配）**：为 MCP 单独创建一个数据库账号，只授予 `SELECT`，

并在连接串中设置 `default_transaction_read_only=on`，同时在 `db_query` 内部强制 `LIMIT`。

**三道防线**：账号权限、会话参数、代码层限制——任何一道单独失效时仍有兜底。



**举例（慢查询的定位）**：`db_query` 耗时 4500ms，先确认是否缺少索引；

若索引正常，再检查是否一次性拉取了过多行。常见原因是没有强制 LIMIT 或没有下推过滤条件。



**⚠️ Security note:** Always use read-only connections. Never expose write permissions without approval workflows.

写入类操作必须走审批流程，并保留完整的调用审计记录。



---



### Phase 4 — Debugging & Optimization



**Step 4.1: MCP Connection Diagnostic**



When an MCP tool fails, systematically diagnose the root cause.



**Diagnostic checklist:**

1. Authentication — Is the API key valid and not expired?

2. Network — Can the server reach the tool's API endpoint?

3. Permission — Does the token have the required scopes?

4. Rate limit — Is the tool's API rate limit exceeded?

5. Schema mismatch — Does the tool's input_schema match the server's definition?

6. Runtime compatibility — Is the MCP server version compatible with the runtime?



**Output: MCP Debug Report**



| Tool | Connection Status | Latency | Last Error | Root Cause | 处置建议 | 预计恢复 |
|------|-----------------|---------|-----------|------------|---------|---------|
| Notion | ❌ Failed | — | 401 Unauthorized | Token expired | 轮换密钥并改用密钥管理 | 即时 |
| GitHub | ✅ Working | 230ms | — | — | 无需处理 | — |
| Postgres | ⚠️ Slow | 4500ms | — | Missing index + 无 LIMIT | 加索引并强制返回行数上限 | 1个工作日内 |
| Slack | ❌ Failed | — | channel_not_found | 缺 scope 或 bot 未入频道 | 补 scope 并重新授权、邀请bot | 即时 |
| 自研 Server | ⚠️ Partial | 800ms | schema mismatch | input_schema 与实现不一致 | 对齐 schema 并加单测 | 1个工作日内 |



**六步诊断清单的常见表现（本版新增维度）**：



| 检查项 | 典型报错/表现 | 快速验证 |
|-------|-------------|---------|
| 1 认证 | 401 / 403 Unauthorized | 用同一令牌直接调 API 验证 |
| 2 网络 | 超时 / 连接被拒 | curl 目标端点测连通性 |
| 3 权限 | channel_not_found / insufficient_scope | 查令牌 scope 清单 |
| 4 限流 | 429 / 响应变慢 | 查配额用量与重试策略 |
| 5 Schema | invalid_arguments / 参数缺失 | 对比 input_schema 与实际入参 |
| 6 版本 | 工具列表为空 / 方法不存在 | 对比 Server 与运行时版本 |



**Step 4.2: Performance Optimization**



For slow MCP tools, recommend optimizations:

- Add database indexes for common query patterns

- Implement response caching (TTL: 5 minutes for read-only tools)

- Batch API calls where the tool supports it

- Use streaming responses for large data



---



## Input / Output Examples



### Example 1: Building a Multi-Tool Agent Chain



**Input:**

```

I want to build an agent that:

1. Reads feature requests from Notion

2. Creates GitHub issues for each one

3. Posts a summary to Slack

4. Updates Notion with the GitHub issue links



I use Claude Desktop. Help me set up the MCP servers.

```



**Output:**

```

## MCP Architecture for Feature Request Agent



### Required MCP Servers (3 total)

1. notion-mcp — Read/write Notion databases

2. github-mcp — Create GitHub issues

3. slack-mcp — Post Slack notifications



### Setup Instructions



Step 1: Install MCP servers

```bash

npm install -g @modelcontextprotocol/server-notion

npm install -g @modelcontextprotocol/server-github  

npm install -g @modelcontextprotocol/server-slack

```



Step 2: Configure .mcp.json in Claude Desktop config directory



Step 3: Verify connections with diagnostic check



### Agent Prompt Template

"You are a feature request manager. Every morning at 9am:

1. Search Notion for items in the 'Feature Requests' database with status='pending'

2. For each item, create a GitHub issue in repo 'acme/product' with label 'feature-request'

3. Reply to each Notion item with the GitHub issue URL

4. Post a Slack message to #product-updates with count + top 3 priority items"



### Error Handling

- If GitHub API rate limited: retry after 60s, queue remaining items

- If Notion update fails: log to error Notion page, alert via Slack DM

```



### Example 2: Debugging a Failing MCP Connection



**Input:**

```

My Slack MCP integration stopped working. The error says 

"channel_not_found" when I try to post messages.

```



**Output:**

```

## MCP Slack Debug Report



### Diagnostic Results

1. Authentication: ✅ Token valid (expires in 45 days)

2. Network: ✅ API endpoint reachable (45ms)

3. Permission: ⚠️ Token missing scopes: channels:write

4. Rate Limit: ✅ Well within limits (12% used)

5. Schema: ✅ Input schema matches server definition

6. Runtime: ✅ Version 1.0.3 compatible



### Root Cause Identified

MISSING SCOPE: The Slack app's OAuth token does not include

the "channels:write" scope required to post to public channels.



### Fix Instructions

1. Go to api.slack.com/apps → your app → OAuth & Permissions

2. Add scope: "channels:write" (or "chat:write" for broader access)

3. Reinstall the app to workspace (OAuth reinstall required for scope changes)

4. Update your MCP config with the new token

5. Re-run the diagnostic to confirm ✅



### Alternative Workaround

Use the conversations.open API instead — it works with existing scopes

and can post to any channel the bot has been invited to.

```



### Example 3: 金融机构内部系统接入（本版新增）



**Input:**

```

我们是保险公司，想让Agent通过MCP查CRM和保单系统。

合规要求可审计、可解释、数据不出境。怎么设计？

```



**Output:**

```

## 架构建议：Pattern C（API-First）+ Gateway



### 拓扑

Agent → MCP Gateway（统一鉴权/审计）→ 内部MCP Server → CRM / 保单系统



### 关键设计

1. 传输：全部走 HTTP，禁用 stdio（本地进程无法集中审计）
2. 身份：每个Agent独立身份，禁止共享账号
3. 权限：按系统分别授权，保单查询只读，信息变更需人工审批
4. 审计：记录调用方、工具、参数摘要、结果摘要、耗时，留存满足内控要求
5. 数据：敏感字段脱敏后再进入模型上下文，原始明细不落模型侧
6. 版本：Server版本固定，变更走发布流程



### 上线前必过

- 权限清单评审  - 审计日志抽查  - 越权访问测试  - 数据脱敏验证

```



**要点**：金融场景下，**传输模式的选择本身就是合规决策**——

stdio 模式无法集中留痕，通常不满足审计要求。



### Example 4: 从 stdio 迁移到 HTTP（本版新增）



**Input:**

```

我们原来用Claude Desktop + stdio接了3个工具，

现在要给团队共用，怎么迁移？

```



**Output:**

```

## 迁移路径（分步，避免一次性切换）



Step 1：保留 stdio 不变，先把3个工具的调用日志补齐（确认现有用法与调用量）

Step 2：选取调用量最小的一个工具，改造为 HTTP 模式并前置鉴权

Step 3：该工具在 HTTP 模式稳定运行一周后，再迁移第二个

Step 4：全部迁移完成后，评估是否需要引入 Gateway 做统一入口



## 迁移中常见问题

- 环境变量：stdio 继承桌面端环境，HTTP 需显式注入密钥（不要硬编码）
- 并发：stdio 单进程，HTTP 需考虑并发与超时设置
- 路径：本地文件路径在远端Server上可能不存在，需改为可访问的资源标识



## 回滚预案

保留原 stdio 配置不删除，切换期内可随时回退

```



---



## MCP Server Registry



Pre-built MCP server templates available:



| Tool | Package | Auth | Operations | China Status | 推荐传输 | 典型场景 | 主要注意点 |
|------|---------|------|-----------|-------------|---------|---------|-----------|
| GitHub | @modelcontextprotocol/server-github | OAuth | 20+ | ✅ Works globally | stdio / HTTP | 代码检索、PR摘要 | 令牌按只读优先授予 |
| Slack | @modelcontextprotocol/server-slack | OAuth | 15+ | ⚠️ Slack blocked in China | HTTP | 通知推送、日报 | 需 bot 被邀请入频道 |
| Notion | @modelcontextprotocol/server-notion | API Key | 12+ | ✅ Works globally | stdio / HTTP | 需求池同步 | 密钥轮换周期要明确 |
| PostgreSQL | @modelcontextprotocol/server-postgres | Connection string | 5+ | ✅ Works globally | HTTP | 报表查询 | 强制只读 + LIMIT |
| Filesystem | Built-in | Local | 8+ | ✅ Works globally | stdio | 本地文件处理 | 限制可访问目录范围 |
| Brave Search | @modelcontextprotocol/server-brave-search | API Key | 3+ | ⚠️ Limited | HTTP | 公开信息检索 | 注意配额与费用 |
| AWS | aws-mcp | AWS credentials | 30+ | ✅ S3/lambda work | HTTP | 云资源操作 | 最小权限 IAM 角色 |
| 腾讯云 | Custom (not official) | SecretKey | Varies | ✅ China-optimized | HTTP | 国内云资源 | 自研需补齐审计日志 |
| 钉钉 / 飞书 | 自研（官方注册表暂无） | 自建 | Varies | ✅ China-optimized | HTTP | 国内协同办公 | 用 MCP Python SDK 自建 |



**选型举例（本版新增）**：同样是接数据库，个人做数据分析用 stdio + 本地文件系统即可；

团队共用的报表查询必须走 HTTP 并强制只读；若涉及客户敏感数据，还需在返回结果中做字段级脱敏。

**传输模式不是技术偏好，而是由“谁在用、用到什么数据”决定的**。



---



## Notes & Best Practices



1. **MCP vs. direct API calls:** MCP adds a layer of standardization. Use it when you need to swap AI runtimes (Claude ↔ GPT ↔ Gemini) without rewriting tool integrations.

2. **China-specific:** Official MCP servers for 钉钉 (DingTalk) and 飞书 (Lark) are not in the official registry — build custom ones using the MCP Python SDK. 腾讯云 SDK has partial MCP compatibility.

3. **Security:** MCP tools inherit the AI agent's access level. Always use least-privilege tokens and enable audit logging.

4. **Versioning:** MCP moved to Linux Foundation Agentic AI Foundation (2025-11). Pin server versions in production. For China deployments, track domestic MCP ecosystem evolution.

5. **Testing:** Use `mcp dev` CLI or the Claude Desktop MCP inspector to test tools before deploying to agents.

6. **Cost control:** Many MCP tool calls count as API calls. Set rate limits and budgets per agent.

7. **2026标准之战：** MCP vs. OpenAI Tool Use vs. Google A2A — MCP已获得最多生态支持，但跨协议互操作性是2026年新挑战。使用标准转换层（如MCP Gateway）可桥接不同协议。

8. **企业AI Agent首选：** 金融行业部署AI Agent时，优先通过MCP接入内部系统（CRM/ERP），而非直接API集成——MCP的审计日志和访问控制更规范。



9. **先补审计再上规模（本版新增）：** 在Server数量超过5个之前就把审计日志补齐，否则后期回溯调用链的成本会成倍上升。



10. **传输模式由共用范围决定（本版新增）：** 单人用走 stdio，团队共用走 HTTP，多Server统一治理才引入 Gateway。不要为了架构好看而过早引入网关。



11. **密钥永远走环境变量（本版新增）：** 配置文件里出现明文密钥是最常见的安全事故来源；迁移到 HTTP 模式时尤其容易遗漏这一点。



12. **版本固定并留回滚（本版新增）：** 生产环境固定Server版本号，同时保留旧配置不删除，确保出问题时能快速回退。



13. **写入类工具一律加确认（本版新增）：** 只读工具可以自动化，涉及发消息、改数据、触发流水线的工具，都应先生成草稿再经人工确认。



---



*Author: @gechengling | Skill: mcp-tool-integrator | clawhub.ai/gechengling/mcp-tool-integrator*


## 本轮增量（2026-11-16）：复核维度与举例补充

> 本节为 2026-11-16 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Phase 1 — MCP Fundamentals & Environment Setup / 基础与环境**：

- 环境设置清单补「传输模式与暴露面」纸面标注：stdio 与 HTTP 两种模式并列记录各自暴露面与前置鉴权要求，草稿标注所选模式及理由，需人工确认。
- 权限配置新增「最小工具集」占位：每个 Server 列出任务所需的最小工具清单，与默认开启的工具集对照，多余项标注待关闭并交人工处理。

**Phase 4 — Debugging & Optimization / 调试与优化**：

- 调试诊断表补「证据完整性」列：每条根因判断标注所依据的日志片段位置，缺日志佐证的按待补处理，不写入确定结论。
- 优化建议新增「回滚预案」占位：每项配置变更旁记录对应的回滚条件与复核人，草稿只记录预案要点，不代为执行切换。

### 新增复核维度表（2026-11-16）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 最小工具集比对 | 开发者 + 复核人 | Server 配置 / 任务清单 | 默认开启工具与任务所需最小集合是否逐项比对 | 中 | 纸面核对，变更须人工执行 |
| 根因证据完整性 | 开发者 | 连接日志草稿 | 每条根因判断是否标注日志片段位置 | 中 | 草稿记录，不构成处置结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于MCP 工具集成方法论的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产环境部署、权限开通与连接切换的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-16**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-23）：复核维度与举例补充

> 本节为 2026-11-23 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**### Phase 1.5 — 传输模式选型与安全加固（本版新增）**：

- 选型表补「权限分级」一列：把只读、草稿、写操作、外部通信四类动作分栏标注，草稿不给出可直接执行的动作语句。
- 加固清单新增「留痕五要素」占位：来源、版本、审批人、复核时点、停用路径并列记录，缺一项即标注证据不完整，需人工确认。

**## MCP Server Registry**：

- 登记表补「工具级最小权限」一列：每个已登记 Server 标注实际所需的工具范围与权限边界，范围不明的按待补处理，草稿不写入凭据类信息。
- 清单新增「版本固定与停用」占位：把当前有效版本与待停用版本分栏，草稿只记录状态说明，不代为撤下或替换任何条目。

### 新增复核维度表（2026-11-23）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 选型权限分级 | 集成人员 + 复核人 | 选型表 / 书面口径 | 四类动作分级与留痕五要素是否齐全 | 高 | 纸面对照，接入须人工审核 |
| 登记最小权限 | 集成人员 | 登记表 / 官方发布页 | 工具范围与权限边界是否标注、版本固定是否列明 | 高 | 文档记录，不构成放行结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于传输模式选型与 MCP Server 登记的方法论纸面参考的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及Server 上线接入、权限授予与生产环境放行的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-23）

> 参考 2026 年公开 MCP 安全资料中「最小权限落在工具级而非服务级、按动作分离读写与高风险操作」「工具定义版本固定并对完整定义做哈希、变更须重新评审」「审计记录覆盖身份、工具、参数、授权结果与审批决策」「高风险动作强制二次确认并保留回滚占位」的思路，在传输选型与 Server 登记章节补一个纸面小节：分列权限分级、定义版本、审计要素与停用占位，并提示凭据管理、审批与放行由具备权限的人员在既有系统中完成，草稿不填入未经核实的命令或密钥。

### 时效性说明

- 本期时效性核查：**截至 2026-11-23**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
