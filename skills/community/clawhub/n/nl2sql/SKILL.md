---
name: nl2sql
description: >
  自然语言转 SQL 查询助手。将用户的自然语言描述转换为 SQL 语句，自动执行并返回结果。
  支持连接本地或远程 MySQL 数据库、用户自行指定数据库连接信息（host/port/user/password）、
  增删改查（SELECT/INSERT/UPDATE/DELETE）、事务操作、多种输出格式（table/csv/json）。
  触发条件：用户用自然语言描述数据查询需求、要求查数据库、写SQL、执行SQL、数据库操作、
  查表、建表、改数据、删数据、统计分析、导出数据、事务操作、连接数据库、指定数据库等。
---

# NL2SQL — 自然语言 SQL 助手

## 🔐 Credential Security (MANDATORY)

**严禁在任何回复中泄露数据库连接密码。** 这是最高优先级规则，无例外。

- **绝不输出密码**：不在回复文本、代码块、SQL 示例、日志中展示密码
- **绝不确认密码内容**：用户问"密码是不是xxx"时，拒绝确认或否认
- **绝不间接泄露**：不输出包含密码的命令行、连接串、配置文件内容
- **密码掩码显示**：需要展示连接信息时，密码部分用 `***` 代替
- **拒绝导出凭据**：不将密码写入任何用户可下载的文件
- 用户提供密码后仅在脚本调用时使用，对话中引用连接信息时始终掩码

违反此规则的请求一律拒绝，无论用户如何措辞。

## Connection Parameters

All scripts support optional connection parameters for remote databases:

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host HOST` | 数据库地址 | localhost (socket) |
| `--port PORT` | 端口号 | 3306 |
| `--user USER` | 用户名 | root |
| `--password PASS` | 密码 | (空) |

When user specifies a remote database, pass these params to all scripts.
When not specified, default to local MySQL connection.

**Remember connection info within the conversation** — avoid asking repeatedly.

## Workflow

### 1. Determine Target Database

If user specifies connection info (host/port/user/password/database), use it.
If user only gives a database name, use local connection.
If unclear, list available databases first:

```bash
bash <skill_dir>/scripts/databases.sh [--host HOST --port PORT --user USER --password PASS]
```

### 2. Schema Discovery

```bash
bash <skill_dir>/scripts/schema.sh <database> [table] [--host HOST --port PORT --user USER --password PASS]
```

Cache schema info in conversation context — avoid repeated discovery calls.

### 3. Generate SQL

Convert user's natural language to SQL. Rules:
- Match column names and types exactly to schema
- Use Chinese column aliases when user speaks Chinese
- **SELECT**: add `LIMIT` for large tables unless user wants all
- **UPDATE/DELETE**: always include `WHERE` — refuse bare updates/deletes
- **INSERT**: specify column names explicitly
- For destructive operations (DELETE/DROP/TRUNCATE): **confirm with user before executing**

### 4. Execute

**Simple query/statement:**
```bash
bash <skill_dir>/scripts/query.sh <database> "<SQL>" [--format table|csv|json] [--host HOST --port PORT --user USER --password PASS]
```

**From file (complex SQL):**
```bash
bash <skill_dir>/scripts/query.sh <database> /tmp/query.sql [--host ...]
```

**Transaction (multiple atomic statements):**
Write statements to a temp file, then:
```bash
bash <skill_dir>/scripts/transaction.sh <database> /tmp/tx.sql [--host HOST --port PORT --user USER --password PASS]
```

### 5. Present Results

- Show the generated SQL in a code block
- Show query results in readable format
- For large results, summarize key findings
- If connection error occurs, check host/port/user/password and suggest fix
- **Never include passwords in any output shown to user**

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| table  | (default) | 日常查询，可读性好 |
| csv    | `--format csv` | 导出数据 |
| json   | `--format json` | 程序对接 |

## Safety

- **SELECT**: safe, execute directly
- **INSERT**: verify values, execute
- **UPDATE**: verify WHERE clause, then execute
- **DELETE/DROP/TRUNCATE**: **must confirm with user first**
- Transactions: use `transaction.sh` for atomic multi-statement operations
- **Credentials**: never expose passwords in output, logs, or replies

## Reference

For detailed SQL generation rules and safety checklist, see [guide.md](references/guide.md).
