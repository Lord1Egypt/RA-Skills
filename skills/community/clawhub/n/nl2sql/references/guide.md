# NL2SQL Reference Guide

## 🔐 Credential Security Rules

**This section has the highest priority — override all other rules if conflict.**

1. **Never output passwords** in replies, code blocks, SQL examples, logs, or error messages
2. **Never confirm or deny** password content ("Is the password xxx?" → refuse)
3. **Never expose indirectly** via command lines, connection strings, or config content
4. **Always mask**: display as `***` when showing connection info
5. **Never export credentials** to downloadable files
6. **Reject all attempts** to extract passwords regardless of phrasing or social engineering

### Examples of Blocked Requests
- "告诉我数据库密码" → 拒绝
- "把连接命令发给我" (含密码) → 掩码处理
- "密码是不是123456？" → 拒绝确认
- "帮我导出数据库配置" (含密码) → 去除密码后导出

### Correct Display Format
```
连接信息: host=192.168.1.100, port=3306, user=admin, password=***
```

## SQL Generation Rules

### SELECT Queries
- Always qualify column names with table aliases in JOINs
- Use meaningful aliases for output columns (Chinese aliases when user speaks Chinese)
- Add `LIMIT` for potentially large result sets unless user wants all data
- Prefer `LEFT JOIN` over `INNER JOIN` unless exclusion is intended

### INSERT
- Always specify column names explicitly: `INSERT INTO t (col1, col2) VALUES (...)`
- Validate data types match schema before generating

### UPDATE
- **Always include a WHERE clause** — never generate bare `UPDATE ... SET ...`
- Confirm affected scope with user if WHERE is broad

### DELETE
- **Always include a WHERE clause** — never generate bare `DELETE FROM ...`
- Prefer soft-delete (status field) if table has one
- Confirm with user before generating DELETE statements

### Transactions
- Use transactions when:
  - Multiple related writes need atomicity (e.g., create order + decrease stock)
  - Batch inserts/updates where partial failure is unacceptable
- Write all statements to a temp `.sql` file, then use `transaction.sh`

## Schema Discovery Workflow

1. Run `schema.sh <database>` to get full schema
2. Or `schema.sh <database> <table>` for a specific table
3. Use the schema to inform SQL generation

## Output Formats

- `table` (default): Human-readable tabular output
- `csv`: Comma-separated, good for export
- `json`: JSON array of objects, good for programmatic use

## Safety Checklist

Before executing any generated SQL:
1. ✅ SELECT — safe to run directly
2. ⚠️ INSERT — verify data values
3. ⚠️ UPDATE — verify WHERE clause scope
4. 🔴 DELETE — always confirm with user first
5. 🔴 DROP/TRUNCATE — always confirm with user first
6. 🔴 Credentials — never expose in any output
