---
name: column-comment
description: When determining whether the specific column is anomaly with rules, follow this document.
---

## Execution Method

Column comment queries must be executed via `kwdb_sql_execute.py` **without** an output file argument. Results print to stdout and are not persisted.

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "SHOW COLUMNS FROM dbname.tbname WITH COMMENT"
```

## extract rules from the comment of the specified column
- SQL used to get comment of column from table tbname of database dbname: SHOW COLUMNS from dbname.tbname WITH COMMENT
