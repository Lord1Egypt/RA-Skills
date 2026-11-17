---
name: metadata-query
description: when querying the metadata of database/table/column,follow this document.
---

## Execution Method

All metadata queries must be executed via `kwdb_sql_execute.py` **without** an output file argument. Results print to stdout and are not persisted.

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "<metadata-sql>"
```

## database metadata query
- SQL used  to get all database in KaiwuDB/KWDB: SHOW DATABASES;

## table metadata query
- SQL used to get all tables of database dbname: SHOW TABLES FROM dbname;
- SQL used to get definition of table tbname: SHOW CREATE TABLE dbname.tbname;

## column metadata query
- SQL used to get definition of column in tbname: DESCRIBE dbname.tbname;
- Another SQL used to get definition of column in tbname: SHOW COLUMNS from dbname.tbname;
