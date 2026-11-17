# KingbaseES Claude Code Skills

A comprehensive set of Claude Code skills for KingbaseES V8/V9, covering the full lifecycle from installation and deployment to performance tuning, data migration, troubleshooting, and application development. Enables AI assistants to provide accurate answers to KingbaseES-related questions.

## Skills Overview

| Category | Count | Skills |
|----------|-------|--------|
| Deployment | 3 | kes-deploy, kes-docker, docker-installer |
| SQL Core | 3 | kes-core, kes-plsql, kes-oracle-compat |
| Language Drivers | 7 | kes-java, kes-python, kes-go, kes-nodejs, kes-c-odbc, kes-php, kes-perl |
| Frameworks | 5 | kes-hibernate, kes-sqlalchemy, kes-dotnet, kes-qt, kes-devguide |
| Operations | 5 | kes-backup, kes-ha, kes-security, kes-monitoring, kes-user-mgmt |
| Performance | 3 | kes-sql-tuning, kes-index-design, kes-db-optim |
| Migration | 1 | kes-migration |
| Troubleshooting | 1 | kes-troubleshooting |
| Application | 1 | kes-app-builder |
| Extensions | 2 | kes-vector, kes-mcp |

**Total: 31 skills**

## Skill Details

### kes-deploy — Installation & Deployment

Complete installation and deployment guide for KingbaseES, including ISO installation on Linux/Windows, development tools, and basic configuration.

**Key Topics**:
- Hardware requirements and environment preparation (kernel parameters, resource limits, directory layout)
- Linux/Windows ISO installation (GUI / interactive CLI / silent)
- Development tools (ksql, ksqlcmd, KStudio, kconsole)
- kingbase.conf and sys_hba.conf configuration
- National cryptographic algorithms (scram-sm3, sm4, sm3)
- Post-installation verification and troubleshooting

### kes-docker — Docker Deployment

Docker container deployment guide for KingbaseES, covering image import, container startup, data persistence, and license management.

### kes-plsql — PL/SQL Programming

Complete guide for KingbaseES procedural SQL programming, including stored procedures, functions, triggers, cursors, packages, exception handling, and dynamic SQL.

### kes-oracle-compat — Oracle Compatibility

Oracle compatibility mode reference, including syntax mapping, data type comparison, system view compatibility, and migration guidelines.

### kes-java — Java/JDBC Driver

Java connection setup with Maven dependencies, HikariCP connection pool, SSL/TLS, and national crypto configuration.

### kes-python — Python Driver

Python connection via ksycopg2 driver (Python 2.7 ~ 3.13), environment variables, DSN connections, and high availability.

### kes-go — Go Driver

Go connection via gokb driver, GOPATH/Go Modules setup, and connection parameters.

### kes-nodejs — Node.js Driver

Node.js connection via kb npm package, Client API, and Pool connection pooling.

### kes-c-odbc — C/ODBC Driver

C language integration via KCI native interface, ODBC DSN configuration, and ESQL/C.

### kes-php — PHP Driver

PHP connection via PDO pdo_kdb, kdbCopy batch operations, and kdbLOB large object handling.

### kes-perl — Perl Driver

Perl connection via DBD::KB, standard DBI interface, and transaction control.

### kes-hibernate — Java Framework Integration

Java framework configuration for Hibernate, MyBatis/MyBatis-Plus, Flyway, and Liquibase.

### kes-sqlalchemy — Python Framework Integration

Python ORM setup with SQLAlchemy and Django.

### kes-dotnet — .NET Framework Integration

.NET integration via KDBNDP, Entity Framework 6, and EF Core.

### kes-qt — Qt SQL Driver

Qt integration with qkingbase SQL driver and QSqlDatabase.

### kes-devguide — Development Guide

Application development best practices, client interface selection, connection pool configuration, design principles, and OLTP benchmarks.

### kes-backup — Backup & Recovery

Backup and recovery strategies including KRB cold backup, KRC hot backup, logical backup, PITR, and incremental backup.

### kes-ha — High Availability

HA cluster setup with remote replication (rwc), automatic failover, read-write splitting, and multi-active deployment.

### kes-security — Security Compliance

Security compliance guide covering national crypto SM2/3/4, three-authority separation, TDE, auditing, MAC, and tamper-proof.

### kes-monitoring — Monitoring & Management

Monitoring setup with NMON, KWR, KSH, sys_stat_statements, alert configuration, and daily inspections.

### kes-user-mgmt — User & Permission Management

User management, role permissions (GRANT/REVOKE), tablespace quotas, resource limits, and password policies.

### kes-sql-tuning — SQL Performance Tuning

7-step diagnosis workflow with KWR/KSH/KDDM, dynamic performance views, execution plans, and SQL optimization patterns.

### kes-index-design — Index Design

Index type selection, composite indexes, partial indexes, GIN/GiST full-text indexes, and covering indexes.

### kes-db-optim — Database Parameter Tuning

Database parameter optimization (shared_buffers, work_mem), statistics management, and capacity planning.

### kes-migration — Data Migration

Migration workflow from multi-source databases to KingbaseES via KDTS tool, KFS continuous sync, application adaptation, and cutover.

### kes-troubleshooting — Troubleshooting

Standardized troubleshooting for HA failures, resource exhaustion, data loss prevention, and performance diagnosis.

### kes-app-builder — Application Builder

Application construction orchestrator: requirements collection → technology stack confirmation → environment check → development → deployment.

### kes-vector — Vector Database Extension

KES_Vector extension guide covering vector types (vector/halfvec/sparsevec/bit), ivfflat/hnsw indexes, distance calculations, and similarity search.

### kes-mcp — MCP Server

KingbaseES MCP Server (kingbase-mcp v0.3.0) with 10+ tools (schema exploration, SQL execution, execution plan analysis, index optimization, health checks, slow query detection), supporting Stdio/SSE/HTTP transport.

## Installation

### Option 1: Let Claude Install Automatically (Easiest)

Simply drop the skill package file into Claude Code and say:

```
Please install this skill package: @kes-skills-master.zip
```

Claude Code will automatically extract and install it to `.claude/skills/` at the project level.

### Option 2: Manual Installation

```bash
# Download from Gitee
cd /tmp
git clone https://gitee.com/your-org/kes-skills.git --depth 1
cd kes-skills
unzip -q ../kes-skills-master.zip  # if downloaded as zip

# Project-level installation (recommended, current project only)
mkdir -p .claude/skills
cp -r kes-* docker-installer .claude/skills/

# Or global installation (available for all projects)
mkdir -p ~/.claude/skills
cp -r kes-* docker-installer ~/.claude/skills/
```

### Option 3: Via oh-my-claudecode (if installed)

If you have the oh-my-claudecode plugin installed, run:

```
/oh-my-claudecode:skill add kes-skills.tar.gz
```

### Option 4: Install Directly from Gitee Repository

```bash
# Clone and install in one command
git clone https://gitee.com/your-org/kes-skills.git /tmp/kes-skills \
  && mkdir -p .claude/skills \
  && cp -r /tmp/kes-skills/kes-* /tmp/kes-skills/docker-installer .claude/skills/ \
  && rm -rf /tmp/kes-skills
```

## Usage

Once installed, Claude Code automatically invokes the relevant skill based on your questions:

| You Say | Auto-Triggers |
|---------|---------------|
| "How to install KingbaseES" | kes-deploy |
| "Docker deployment" | kes-docker |
| "How to create a partitioned table" | kes-core |
| "Write a stored procedure" | kes-plsql |
| "Oracle syntax replacement" | kes-oracle-compat |
| "Java JDBC connection" | kes-java |
| "Python connection" | kes-python |
| "Go connection" | kes-go |
| "Hibernate configuration" | kes-hibernate |
| "SQL optimization" | kes-sql-tuning |
| "Index design" | kes-index-design |
| "Database backup" | kes-backup |
| "High availability setup" | kes-ha |
| "National crypto config" | kes-security |
| "Database monitoring" | kes-monitoring |
| "Oracle to KingbaseES migration" | kes-migration |
| "Dual-primary issue" | kes-troubleshooting |
| "Build an application" | kes-app-builder |
| "Vector similarity search" | kes-vector |
| "Configure MCP Server" | kes-mcp |

## Directory Structure

```
kes-skills/
├── docker-installer/       # Docker Engine/Desktop installation guide
├── kes-app-builder/        # Application builder orchestrator
├── kes-backup/             # Backup & recovery (KRB/KRC/PITR)
├── kes-c-odbc/             # C/ODBC/DCI driver
├── kes-core/               # Core SQL syntax
│   ├── ref/
│   │   ├── data-types.md
│   │   ├── error-codes.md
│   │   ├── sql-syntax.md
│   │   ├── schema-design.md
│   │   └── system-catalog.md
├── kes-db-optim/           # Database parameter tuning
│   └── ref/
│       ├── statistics.md
│       └── perf-optimization-experience.md
├── kes-deploy/             # ISO installation & deployment
│   └── ref/
│       └── hardware-requirements.md
├── kes-devguide/           # Application development guide
│   └── ref/
│       ├── connection-pool.md
│       ├── development-spec.md
│       └── capacity-planning.md
├── kes-docker/             # Docker deployment
│   └── ref/
│       └── docker-compose-examples.md
├── kes-dotnet/             # .NET framework integration
├── kes-go/                 # Go driver (gokb)
├── kes-ha/                 # High availability (rwc/HA cluster)
│   └── ref/
│       ├── ha-concepts.md
│       └── rwc-cluster-deployment.md
├── kes-hibernate/          # Java framework integration
│   └── ref/
│       └── java-frameworks.md
├── kes-index-design/       # Index design strategies
│   └── ref/
│       └── index-design-guide.md
├── kes-java/               # Java/JDBC driver
├── kes-migration/          # Data migration (KDTS/KFS)
│   └── ref/
│       ├── migration-tools.md
│       ├── migration-best-practice.md
│       └── migration-faq.md
├── kes-monitoring/         # Monitoring & alerting
│   └── ref/
│       └── monitoring.md
├── kes-nodejs/             # Node.js driver (kb)
├── kes-oracle-compat/      # Oracle compatibility mode
│   └── ref/
│       └── oracle-compat.md
├── kes-perl/               # Perl driver (DBD::KB)
├── kes-php/                # PHP driver (pdo_kdb)
├── kes-plsql/              # PL/SQL programming
│   └── ref/
│       └── plsql.md
├── kes-python/             # Python driver (ksycopg2)
├── kes-qt/                 # Qt SQL driver (qkingbase)
├── kes-security/           # Security compliance
│   └── ref/
│       ├── security-audit.md
│       ├── security-auth.md
│       ├── security-encryption.md
│       ├── security-label-mac.md
│       ├── national-crypto.md
│       └── three-authority.md
├── kes-sql-tuning/         # SQL performance tuning
│   └── ref/
│       ├── explain-plan.md
│       ├── sql-optimization-patterns.md
│       ├── auto-tuning.md
│       └── perf-optimization-experience.md
├── kes-sqlalchemy/         # Python ORM (SQLAlchemy/Django)
├── kes-troubleshooting/    # Troubleshooting guide
│   └── ref/
│       ├── ha-troubleshooting.md
│       ├── data-security.md
│       ├── performance-diagnosis.md
│       └── common-commands.md
├── kes-user-mgmt/          # User & permission management
│   └── ref/
│       └── user-management.md
├── kes-vector/             # Vector database extension
│   └── ref/
│       ├── data-types.md
│       ├── functions-operators.md
│       └── indexes.md
└── kes-mcp/                # MCP Server (kingbase-mcp)
    └── ref/
        └── mcp-tools.md
```

## Supported Versions

KingbaseES V8 / V9

## Supported OS & Architectures

- **Linux**: CentOS 7/8, Kylin V10, UnionTech UOS, openEuler, LinuxSight, Kirin SecOS
- **Windows**: Windows 7/10/11/Server 2008+
- **Architectures**: x86_64, LoongArch (Loongson), ARM64 (Phytium/Kunpeng), Hygon, ZhaoXin

## License

Apache License 2.0
