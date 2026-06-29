# Intake Gate

Diagnose only after the minimum evidence contract is satisfied.

## Core Inputs For All Incidents

- fault symptom or user-visible failure
- fault time or time window
- at least one usable evidence root:
  - log directory
  - attached log snippet
  - case export
  - system-log export
  - permission to discover them

## Path-Specific Inputs

- OOM, restart, or process-kill incidents:
  - system-log path, exported `messages` / `syslog` / `dmesg`, or permission to inspect them
- performance incidents:
  - slow SQL text, or
  - access to the `kwdb-mcp-server` `query-metrics-history` tool, or
  - exported metrics-history results
- source-level localization:
  - a local source repo path, or
  - user approval to download the official repo
- cluster-level availability:
  - node list, node logs, or enough per-node timestamps to build a merged timeline when available

## Minimal Follow-Up Order

1. ask for the hard fault time or time window if it is missing
2. ask for the strongest missing evidence root for the selected path
3. ask for the path-specific blocker only after classification:
   - system evidence for OOM or restart
   - metrics access or slow SQL for performance
   - source repo only after the decisive evidence path is grounded
4. if more than one item is missing, ask the smallest set that unblocks the next diagnostic stage

## Gate Rules

- do not deep-scan logs before a usable time anchor exists
- do not request source access before the log or metric evidence is grounded
- do not ask for branch or commit information up front
- if the user cannot provide a critical input, say the diagnosis is blocked at that stage and list the remaining missing items
