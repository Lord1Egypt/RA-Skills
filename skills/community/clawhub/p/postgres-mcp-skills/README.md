# postgres-mcp-skills

基于 [postgres-mcp](https://github.com/crystaldba/postgres-mcp) 的 Agent Skills 集合，为 PostgreSQL 数据库提供完整的管理和优化能力。兼容 [Agent Skills 开放标准](https://agentskills.io)，支持 OpenClaw、Claude Code 等平台。

## 功能

| Skill | 说明 |
|---|---|
| **setup-postgres-mcp** | 安装部署 postgres-mcp 服务 |
| **pg-health** | 数据库健康检查（索引健康、连接利用率、缓存、vacuum、复制延迟等） |
| **pg-index-tuning** | 索引优化建议和性能调优 |
| **pg-query-plan** | 查询执行计划分析和优化 |
| **pg-schema** | 数据库模式查询和智能 SQL 生成 |
| **pg-execute** | 安全的 SQL 执行（支持只读模式和访问控制） |

## 前置条件

- 已安装并运行 [postgres-mcp](https://github.com/crystaldba/postgres-mcp) 服务
- 如未安装，使用 `setup-postgres-mcp` skill 引导完成

## 安装

### OpenClaw

下载本项目到本地后，将 `SKILL.md` 文件和 `reference/` 目录复制到 OpenClaw 的 SKILLS 目录下重启会话生效。

### Claude Code

```bash
# 项目级别
cp SKILL.md .claude/skills/postgres.md
cp -r reference/ .claude/skills/postgres-reference/

# 或全局级别
cp SKILL.md ~/.claude/skills/postgres.md
cp -r reference/ ~/.claude/skills/postgres-reference/
```

使用 `/postgres` 调用，它会根据你的意图自动路由到相应的功能模块。

## 使用示例

```
# 首次使用：安装 MCP 服务
/setup-postgres-mcp

# 健康检查
/pg-health

# 索引优化
/pg-index-tuning

# 查询计划分析
/pg-query-plan

# 执行 SQL
/pg-execute
```

## 许可证

MIT
