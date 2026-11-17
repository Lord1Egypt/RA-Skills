# TPC-H

TPC-H preparation can generate large local `.tbl` files, transfer them to Observer hosts, create/load database tables, and retain temporary SQL and logs. Resolve every stage before running `obd test tpch`.

## Parameter-to-Stage Plan

Read installed help and map each selected option to these artifacts:

| Input | Decision to record |
|---|---|
| Scale factor | Expected logical data size, generated-file size, database size, and safety headroom |
| Local temporary/TBL path | Controller path, owner, existing content, generation/reuse decision |
| Remote TBL directory | Exact target servers, canonical path, owner, free space, transfer/reuse decision |
| DDL and SQL paths | Built-in or supplied files and their checksums |
| Test-only/reuse option | Which generation, transfer, schema creation, and load phases are skipped |
| Transfer-disable option | Proof that the complete matching dataset already exists on every required target |

In verified command surfaces, `--remote-tbl-dir` is needed when the workflow loads generated data, while `--test-only` skips initialization. `--disable-transfer` can reuse files already on target hosts. Confirm these semantics in the installed version; neither option proves that the files match the requested scale or schema.

Estimate peak space rather than only final database size: local generated data, transfer copies, remote files, loaded tables/indexes, logs, temporary merge/sort space, and retained results can coexist.

Inspect the selected DDL and load workflow before authorization. Verified current TPC-H assets drop the benchmark tables and tablegroups before recreating them, and the load path issues a major freeze after loading. Freeze scope is plugin-version dependent: inspected 3.1 code uses cluster-level `ALTER SYSTEM MAJOR FREEZE`, while later 4.x code can use a tenant-scoped form. Show the exact objects that will be replaced and the observed freeze scope's I/O/compaction impact; obtain dataset-replacement and major-freeze authorization separately from permission to run queries. A `--test-only` or reuse path must be proven to skip the destructive initialization in the selected version.

Inspect credential propagation as well. Verified current workflows construct OBClient commands with a password argument. If no protected input is available, use the common dedicated short-lived credential procedure, restrict process/log visibility, and retain only redacted commands.

## Command Shape

```bash
obd test tpch <deploy_name> \
  --component=<component> \
  --test-server=<server> \
  --tenant=<tenant> \
  --user=<user> \
  --database=<database> \
  --scale-factor=<scale> \
  --remote-tbl-dir=<absolute_remote_path> \
  --tmp-dir=<absolute_run_owned_path> \
  --optimization=0 \
  [reviewed generation/reuse options] \
  [version-supported credential option; value supplied only through the approved local procedure]
```

Use long options even when installed help also exposes short aliases. TPC-H has no universal workload-duration option: inspected current paths can wait for major compaction or an individual OBClient query. Apply the common timeout handling to generation, transfer/load, freeze/merge, warmup, queries, and the complete invocation; after a caller timeout, verify database-side query state before retrying.

## Stage and Accept

1. **Generate/reuse:** checksum or otherwise identify local `.tbl`, DDL, and SQL artifacts.
2. **Transfer/reuse:** verify every remote file belongs to this dataset and expected target; record counts and sizes.
3. **Load:** verify required tables, row counts, schema, statistics, and the authorized major-freeze outcome before queries.
4. **Run:** preserve per-query status, duration, output/error, and the query set actually executed.
5. **Report:** distinguish generation, transfer, load, and query time; do not report their sum as query performance.
6. **Cleanup/retain:** separately decide the database dataset, local files, remote files, temporary SQL, and results. Never delete a reusable dataset merely because query execution completed.

Success requires every requested query to reach an accepted result, no unexplained missing/extra row-count state, complete raw results, and healthy SQL and cluster state after the run.
