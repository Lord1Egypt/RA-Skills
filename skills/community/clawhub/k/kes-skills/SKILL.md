---
address: https://gitee.com/king-db/kes-skills
version: 1.0.0
license: Apache-2.0
---

# KES Skills

一套面向 KES V8/V9 的技能包，覆盖从安装部署到性能调优、数据迁移、故障排查和应用开发的全链路场景。

## 技能清单（31 个）

### 部署层

| 技能 | 说明 |
|------|------|
| `kes-deploy` | ISO 安装部署 — Linux/Windows 静默安装、系统参数、开发工具、配置 |
| `kes-docker` | Docker 容器化 — 镜像导入、容器启动、数据持久化、License 管理 |
| `docker-installer` | Docker 通用安装 — Linux/Windows/macOS Docker Engine/Desktop 安装与配置 |

### SQL 核心层

| 技能 | 说明 |
|------|------|
| `kes-core` | 核心 SQL 语法 — DDL/DML/DCL、分区表、窗口函数、CTE、JSON、系统目录 |
| `kes-plsql` | PL/SQL 编程 — 存储过程、函数、触发器、游标、包、异常处理、动态 SQL |
| `kes-oracle-compat` | Oracle 兼容模式 — 语法对照、数据类型映射、系统视图兼容、迁移指南 |

### 语言驱动层

| 技能 | 说明 |
|------|------|
| `kes-java` | Java/JDBC — Maven 依赖、HikariCP 连接池、SSL/TLS、国密配置 |
| `kes-python` | Python — ksycopg2 驱动、环境变量、连接配置、高可用 |
| `kes-go` | Go — gokb 驱动、Go Modules、连接参数 |
| `kes-nodejs` | Node.js — kb npm 包、Client API、Pool 连接池 |
| `kes-c-odbc` | C/ODBC — KCI 原生接口、ODBC DSN 配置、ESQL/C |
| `kes-php` | PHP — PDO pdo_kdb、kdbCopy 批量操作、kdbLOB 大对象 |
| `kes-perl` | Perl — DBD::KB、Perl DBI 标准接口、事务控制 |

### 框架层

| 技能 | 说明 |
|------|------|
| `kes-hibernate` | Java 框架 — Hibernate、MyBatis/MyBatis-Plus、Flyway、Liquibase |
| `kes-sqlalchemy` | Python 框架 — SQLAlchemy、Django ORM |
| `kes-dotnet` | .NET — KDBNDP、EF6、EF Core |
| `kes-qt` | Qt — qkingbase SQL 驱动、QSqlDatabase |
| `kes-devguide` | 开发指南 — 客户端接口选型、连接池配置、应用设计原则、OLTP 基准 |

### 运维层

| 技能 | 说明 |
|------|------|
| `kes-backup` | 备份恢复 — KRB 冷备、KRC 热备、逻辑备份、PITR 时间点恢复 |
| `kes-ha` | 高可用 — 远程复制 RWC、HA 集群、故障切换、读写分离 |
| `kes-security` | 安全合规 — 国密 SM2/3/4、三权分立、TDE、审计、MAC、防篡改 |
| `kes-monitoring` | 监控管理 — NMON、KWR、KSH、sys_stat_statements、告警配置 |
| `kes-user-mgmt` | 用户权限 — 角色管理、GRANT/REVOKE、表空间配额、资源限制 |

### 性能层

| 技能 | 说明 |
|------|------|
| `kes-sql-tuning` | SQL 调优 — 7 步诊断流程、KWR/KSH/KDDM、动态性能视图、执行计划 |
| `kes-index-design` | 索引设计 — 索引类型选择、复合索引、部分索引、GIN/GiST |
| `kes-db-optim` | 参数调优 — 数据库参数、统计信息、容量规划 |

### 迁移 / 故障 / 应用

| 技能 | 说明 |
|------|------|
| `kes-migration` | 数据迁移 — KDTS 工具、KFS 持续同步、多源迁移、应用适配、割接上线 |
| `kes-troubleshooting` | 故障排查 — 高可用故障、数据防丢失、性能诊断、常用命令速查 |
| `kes-app-builder` | 应用构建编排器 — 需求收集 → 技术栈确认 → 环境检查 → 开发 → 部署 |

### 扩展层

| 技能 | 说明 |
|------|------|
| `kes-vector` | 向量扩展 — KES_Vector 插件、vector/halfvec/sparsevec/bit 类型、ivfflat/hnsw 索引、相似度搜索 |
| `kes-mcp` | MCP Server — kingbase-mcp v0.3.0，10+ 个工具（结构探索、SQL 执行、执行计划、索引优化、健康检查、慢查询） |

## 安装

```bash
# 项目级安装（仅当前项目可用）
mkdir -p .claude/skills
cp -r kes-* docker-installer .claude/skills/

# 或全局安装（所有项目可用）
mkdir -p ~/.claude/skills
cp -r kes-* docker-installer ~/.claude/skills/
```

安装完成后，Claude Code 会根据你的提问自动调用对应的技能。

## 适用版本

KingbaseES V8 / V9

## 支持的操作系统与架构

- **Linux**: CentOS 7/8、银河麒麟 V10、统信 UOS、openEuler、凝思安全操作系统、麒麟信安
- **Windows**: Windows 7/10/11/Server 2008+
- **架构**: x86_64、龙芯 (LoongArch)、飞腾/鲲鹏 (ARM64)、海光、兆芯
