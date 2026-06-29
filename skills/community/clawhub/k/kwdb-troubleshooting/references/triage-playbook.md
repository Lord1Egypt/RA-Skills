# Triage Playbook

## Functional Path

1. confirm the fault time or ask the user for the fault time window
2. for OOM or process-kill incidents, inspect system evidence with a targeted `oom` / `kwbase` grep first and lock the hard timestamp before reading service logs broadly
3. determine the effective log directory from `--log-dir`, `--store/logs`, or the default path
4. inspect `errlog` first
5. if `errlog` contains a crash stack, extract the top frames, component, and file suffix, then map them to the source repo only when source access is available
6. if there is no crash stack, search decisive `Eyy...`, `Wyy...`, or `Fyy...` lines only within the fault time window
7. expand around the first decisive severity line and repeated amplifier events to capture nearby retries, warnings, and hot business objects
8. if source access is available, map the decisive file suffix, log phrase, or object name to the smallest useful source call chain
9. stop at source-level localization unless the user explicitly requested history attribution
10. if the log indicates a known SQL object, include the object name, SQL text, or operation in the report

## Performance Path

1. confirm the fault time or ask the user for the fault time window
2. determine the effective log directory from `--log-dir`, `--store/logs`, or the default path so warnings can be correlated with the metric window
3. if the user already provided the slow SQL statement, go directly to `EXPLAIN ANALYZE`
4. if no slow SQL statement is confirmed, call the `kwdb-mcp-server` `query-metrics-history` tool for the fault time window
5. decide whether the first hard bottleneck is CPU, IO, memory, or slow SQL
6. if slow SQL is primary, capture the SQL text and run `EXPLAIN ANALYZE` when possible
7. if memory growth or process-kill symptoms are present, inspect targeted system evidence and repeated amplifier events in the same window before naming a cause
8. use the execution plan or memory evidence to identify the concrete bottleneck: large scan, bad join order, sort or hash pressure, network exchange, spill, contention, or native-memory growth
9. correlate the plan, metrics, and nearby warnings before naming the root cause
10. if source access is available, map the confirmed bottleneck to the smallest useful source call chain
11. stop at source-level localization unless the user explicitly requested history attribution

## Mixed Path

1. choose the first decisive artifact by time
2. explain whether the performance symptom caused the functional symptom or vice versa
3. keep one primary root-cause candidate and move the rest to supporting hypotheses
4. still follow the default `time -> log -> optional source -> analysis` chain for the primary candidate

## Cluster-Availability Upgrade

Upgrade the incident to cluster-level availability analysis when any of the following hold:

1. logs from 2 or more nodes share `gossip stalled`
2. logs from 2 or more nodes share `failed node liveness heartbeat`
3. logs mention `lease holder unknown` or `NotLeaseHolderError` on `r1`, `r2`, `r6`, first range, `NodeLiveness`, or `SystemConfig`
4. the user reports that all nodes cannot connect through `kwbase sql`

When upgraded:

1. build the earliest-to-latest node timeline first
2. identify the earliest node exposing system-range symptoms
3. distinguish `earliest exposed node` from `confirmed root cause`
4. if the fault involves a restart after a long degraded-running period, reconstruct `initial failure -> degraded running period -> restart symptom -> recovery behavior` before naming the pattern or root cause
5. do not over-weight restart-day symptoms if earlier failure evidence explains why the cluster later stalled
6. stop after the cluster-level fault chain, key evidence, and missing inputs are clear; do not turn the report into a recovery plan

## Minimal Verification

- functional issue: confirm the decisive log line still maps to the cited source file when source access exists
- performance issue: confirm the plan and metrics point to the same bottleneck class
- mixed issue: confirm the timeline is consistent across logs, metrics, and SQL evidence
- if a branch or commit is cited: confirm it actually touches the cited file or behavior and matches the incident symptom

## Known-Issue Check

1. after the local signature is clear, optionally run `scripts/search_gitee_issues.sh "<signature>"`
2. search by decisive error text, file:line, function name, or slow-SQL symptom
3. if a similar issue exists, use it only as supporting context for versions, fixes, or workarounds
4. if no similar issue exists, do not block the diagnosis

## Output Depth Gate

1. no source access: stop at the evidence conclusion
2. source access with a confirmed code path: extend to source-level localization
3. explicit branch, commit, or history-tracing request plus a confirmed code path: extend to history attribution
