# Limitations — Incident Replay

## What It Doesn't Do

### No Real-Time Monitoring
Incident Replay is a forensic tool, not a monitoring system. It captures snapshots when you tell it to. It doesn't watch your workspace continuously. For real-time detection, pair it with cron/scheduled snapshot capture.

### No Causation, Only Correlation
Root cause classification is heuristic. It looks at signals (config changes + crash = probably config error) but cannot prove causation. The classification guides investigation — it doesn't replace human judgment.

### No Distributed Tracing
Designed for single-workspace analysis. Cannot correlate events across multiple agents, services, or machines. Each workspace is analysed independently.

### Snapshots Are Point-in-Time
Changes between snapshots are invisible. If a file was created and deleted between two snapshot points, Incident Replay won't know it existed. Increase snapshot frequency for finer granularity (at the cost of disk space).

### Simple Diff Algorithm
File diffs use a basic set-difference approach (lines present in one version but not the other). This is not a proper unified diff — it doesn't show context lines or handle moved blocks well. For detailed diffs, export the snapshots and use `diff` or `git diff`.

### Decision Extraction Is Pattern-Based
Decision chains are extracted via regex on log files. If your agent doesn't log decisions in a recognisable pattern, extraction will miss them. Configure `DECISION_MARKERS` to match your agent's logging format.

### No Binary File Analysis
Binary files are tracked (path + hash + size) but their content isn't captured or diffed. The tool is designed for text-based agent workspaces.

### JSON File Storage
Incidents and snapshots are stored as JSON files. No database, no indexing, no query language. Works well for dozens to low hundreds of incidents. At enterprise scale, export to a proper database.

### No Automated Remediation
Incident Replay suggests remediation steps but never executes them. All remediation is manual and advisory. This is deliberate — automated fixes for production failures should require human approval.

### Snapshot Size Limits
Large workspaces may exceed the configurable `MAX_SNAPSHOT_SIZE`. Binary assets, large datasets, and generated files should be excluded via `EXCLUDE_PATTERNS`.
