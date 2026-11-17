---
name: kes-mcp
name_for_command: kes-mcp
description: KingbaseES MCP Server 使用指南。当用户提到 MCP、MCP Server、Model Context Protocol、kingbase-mcp、数据库 AI 工具调用、SQL 执行、执行计划分析、索引优化、健康检查、慢查询时，必须使用此技能。
---

# KingbaseES MCP Server 使用指南

本技能提供 KingbaseES MCP Server（`kingbase-mcp`）的完整参考，涵盖安装配置、传输方式、访问模式、工具列表和常见问题。

> **核心 SQL** → 见 `kes-core` 技能
> **向量扩展** → 见 `kes-vector` 技能

## 快速导航

| 主题 | 参考文件 |
|------|---------|
| 安装与配置 | 本节第 1 部分 |
| 工具详解 | `ref/tools-reference.md` |
| 测试用例 | `test-cases.md` |

## 1. 概述

KingbaseES MCP Server 是基于 [Model Context Protocol](https://modelcontextprotocol.io)（MCP）标准开发的 KingbaseES 数据库集成服务器，使 AI 助手能够通过结构化工具调用与 KingbaseES 数据库交互。

### 1.1 核心特性

- **10+ 个标准工具**：结构探索、SQL 执行、执行计划分析、索引优化、健康检查、慢查询
- **三种传输方式**：Stdio / SSE / Streamable HTTP
- **两种访问模式**：Restricted（只读）/ Unrestricted（读写）
- **连接池管理**：HikariCP 风格连接池
- **安全机制**：RESTRICTED 模式下仅执行 SELECT 查询，30 秒超时

### 1.2 项目信息

| 项 | 值 |
|---|---|
| 版本 | v0.3.0 |
| 语言 | Python 3.10+ |
| 框架 | FastMCP |
| 仓库 | Gitee: `king-db/kingbase-mcp` |

## 2. 安装

### 2.1 环境要求

- Python 3.10 及以上
- KingbaseES V8/V9
- `uv` 包管理器（推荐）或 pip

### 2.2 安装步骤

```bash
# 克隆项目
git clone https://gitee.com/king-db/kingbase-mcp.git
cd kingbase-mcp

# 使用 uv 安装（推荐）
uv sync

# 或 pip 安装
pip install -e .
```

### 2.3 验证安装

```bash
uv run kingbase-mcp --help
```

## 3. 启动配置

### 3.1 数据库连接

通过环境变量或命令行参数指定数据库连接：

```bash
# 方式一：环境变量
export DATABASE_URI="kingbase://user:password@localhost:54321/database"
uv run kingbase-mcp

# 方式二：命令行参数
uv run kingbase-mcp "kingbase://user:password@localhost:54321/database"
```

### 3.2 传输方式

默认使用 `stdio`，也可选择 SSE 或 Streamable HTTP：

```bash
# Stdio（默认，适用于 Claude Code、VS Code 等）
uv run kingbase-mcp "${DATABASE_URI}"

# SSE（适用于需要独立进程的场景）
uv run kingbase-mcp "${DATABASE_URI}" --transport sse --sse-port 8000

# Streamable HTTP（适用于远程访问）
uv run kingbase-mcp "${DATABASE_URI}" --transport streamable-http --streamable-http-port 8000
```

### 3.3 访问模式

```bash
# Restricted 模式（默认，只读，30秒超时）
uv run kingbase-mcp "${DATABASE_URI}" --access-mode restricted

# Unrestricted 模式（可执行任意 SQL）
uv run kingbase-mcp "${DATABASE_URI}" --access-mode unrestricted
```

## 4. AI 编辑器集成

### 4.1 Claude Code

在 `.claude/CLAUDE.md` 或项目根目录 `CLAUDE.md` 中配置：

```yaml
mcpServers:
  kingbase:
    command: uv
    args: ["run", "kingbase-mcp", "kingbase://user:password@localhost:54321/database"]
```

安装 kes-skills：
```bash
cp -r /path/to/kes-skills/kes-* .claude/skills/
```

### 4.2 Cursor

在 `.cursor/rules` 或项目配置中添加 MCP Server 配置：

```json
{
  "mcpServers": {
    "kingbase": {
      "command": "uv",
      "args": ["run", "kingbase-mcp", "kingbase://user:password@localhost:54321/database"]
    }
  }
}
```

### 4.3 Zed

在 `settings.json` 中配置：

```json
{
  "mcp_servers": {
    "kingbase": {
      "command": {
        "path": "uv",
        "args": ["run", "kingbase-mcp", "kingbase://user:password@localhost:54321/database"]
      }
    }
  }
}
```

## 5. 工具速览

| # | 工具名 | 说明 | 模式 |
|---|--------|------|------|
| 1 | `list_schemas` | 列出所有模式 | 只读 |
| 2 | `list_objects` | 列出 schema 中的表/视图/序列/扩展 | 只读 |
| 3 | `get_object_details` | 获取表结构、约束、索引详情 | 只读 |
| 4 | `execute_sql` | 执行 SQL 查询 | 受限/不限 |
| 5 | `explain_query` | SQL 执行计划分析 | 只读 |
| 6 | `analyze_workload_indexes` | 工作负载索引优化建议 | 只读 |
| 7 | `analyze_query_indexes` | 指定 SQL 索引优化建议 | 只读 |
| 8 | `analyze_db_health` | 数据库健康检查 | 只读 |
| 9 | `get_top_queries` | 获取慢查询/资源消耗 TOP N | 只读 |

> 完整工具参数和返回值说明见 `ref/tools-reference.md`

## 6. 使用示例

### 6.1 探索数据库结构

```
# AI 助手调用流程
1. list_schemas() → 获取所有 schema
2. list_objects(schema_name="public", object_type="table") → 获取表列表
3. get_object_details(schema_name="public", object_name="users") → 获取表结构
```

### 6.2 SQL 分析与优化

```
1. explain_query(sql="SELECT * FROM users WHERE email = 'test@example.com'")
2. analyze_query_indexes(queries=[上述SQL], method="dta")
3. 根据建议创建索引后再次 explain_query 验证
```

### 6.3 数据库健康检查

```
analyze_db_health(health_type="all")
# 检查项：索引状态、连接使用、vacuum 健康、序列风险、复制延迟、缓存命中率、约束有效性
```

## 7. 安全注意事项

1. **默认 RESTRICTED 模式**：仅执行 SELECT，30 秒超时
2. **UNRESTRICTED 模式需谨慎**：允许任意 SQL，仅在受信环境使用
3. **数据库凭证**：使用环境变量 `DATABASE_URI` 传递，不要在日志中暴露密码
4. **生产环境**：建议使用专用只读账号连接

## 8. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 启动后无法连接数据库 | 连接 URL 错误或格式不对 | 检查 `DATABASE_URI` 格式 |
| execute_sql 报错 | RESTRICTED 模式禁止非 SELECT | 改用 `--access-mode unrestricted` |
| SSE 端口被占用 | 端口冲突 | 修改 `--sse-port` |
| 工具调用超时 | 查询耗时超过 30 秒 | 优化查询或使用 unrestricted 模式 |
| MCP 目录注册失败 | 提交材料不完整 | 补充 README 和安装说明 |

## 9. 相关技能

- **kes-core** — SQL 语法参考
- **kes-vector** — 向量扩展
- **kes-sql-tuning** — SQL 调优
- **kes-index-design** — 索引设计
- **kes-monitoring** — 监控管理

## 10. 参考文档

```
kes-mcp/
├── SKILL.md                # 本文件
├── ref/
│   └── tools-reference.md  # 工具参数和返回值详解
└── test-cases.md           # 测试用例
```
