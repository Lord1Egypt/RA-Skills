# Action contract

schema/integrity:database relative path. query:database,sql SELECT/CTE only,parameters optional positional list or named map,limit1..10000 default1000,timeoutSeconds1..15. SQLite authorizer blocks writes,ATTACH,PRAGMA from queries and risky functions; read-only connection, query_only and progress budget apply. Source<=256MiB. import-csv:file,table identifier optional data creates a new exported database with TEXT columns preserving IDs. Queries output CSV/JSON/HTML and a truncated flag. No extensions or arbitrary SQL scripts execute. For formula calculation or another database server, use a different tool.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
