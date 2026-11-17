---
name: ladybug-opencypher-updated
description: "Designs and queries LadybugDB graphs with openCypher. Use for schemas, imports, query debugging, transactions, full-text search and Neo4j query adaptation, with local Python helpers."
license: MIT-0
metadata:
  openclaw:
    emoji: "🐞"
    requires:
      anyBins: [python3, python]
---

# LadybugDB openCypher

## Workflow

1. **Identify the database and its owner.** Name the database path, the owning process and what is authorized: reads, writes or schema changes. A live read-write database is reached through the owning application's API: one process can hold several connections, but 2 processes cannot share read-write access. Documentation-only tasks need no runtime.
2. **Check the runtime.** Use the project's Python environment and run `<python> <skill-dir>/scripts/check_env.py --smoke` (in memory only). The binding is `ladybug`, pinned in [requirements.txt](requirements.txt); installing this skill does not install it. [API reference](references/api-reference.md) covers setup, native-load failures and OpenClaw installation checks.
3. **Read the schema.** Record node primary keys, relationship direction, properties and multiplicity. Keep parallel relationships and evidence IDs even when endpoints match. Neo4j differences and unexpected results: [workflow patterns](references/workflow-patterns.md).
4. **Query read-only.** The helper defaults to engine-enforced read-only access:

   ```text
   <python> <skill-dir>/scripts/run_cypher.py /path/to/graph.lbdb --command "MATCH (n:Paper) RETURN n.id LIMIT 10" --print-rows
   ```

   Bind values with `--params` or `--params-file` and validate identifiers separately; use `--file` for reviewed multiline Cypher. Defaults: 30-second timeout, 256 MiB buffer, 20 preview rows per statement (`--timeout-ms`, `--buffer-mib`, `--max-rows`). Preview limits do not bound execution memory: use selective predicates, bounded traversals and `LIMIT`. Read-only database access does not restrict host files or network: review `COPY`, `LOAD`, `CALL`, extensions and paths, and use trusted absolute import paths.
5. **Write only if authorized.** Use `--write` (`--write --create` for a new database; it refuses existing paths), and put a batch inside `BEGIN TRANSACTION; ...; COMMIT;`; without it each statement commits separately, so inspect partial state before retrying. Never escalate after a read-only error. Follow the application's backup and migration procedure, and test engine upgrades and recovery on copies, never on the only database.
6. **Read back and report.** Check properties, direction and identity of what you wrote, not just counts. The helper closes results, connections and databases on failure too. [Helper tests](scripts/test_helpers.py) use temporary databases.

## Output

```
Database:   <path, owning process>
Mode:       read-only | write (authorized by <who>)
Statements: <n>, rows returned: <n>
Read-back:  <properties, direction and identity checked, or "not applicable">
Limits:     <unresolved limits, or "none">
```

## Final check

1. Was the owning process identified, and did only one process open the database read-write?
2. Did every write use `--write` inside an authorization, with a batch inside `BEGIN TRANSACTION; ...; COMMIT;`?
3. Were writes read back for properties, direction and identity?
4. Are the reported checks the ones actually run?

Community-maintained under MIT-0; based on [trenza1ore/ladybug-opencypher](https://clawhub.ai/trenza1ore/skills/ladybug-opencypher).
