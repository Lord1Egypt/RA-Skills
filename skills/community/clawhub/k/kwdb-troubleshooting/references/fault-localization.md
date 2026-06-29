# Fault Localization Chain

Default chain: `hard time -> log window -> optional source call chain -> overall analysis`.

History attribution is an optional extension only when the user explicitly asks for branch, commit, or code-history tracing after the code path is already confirmed.

## 1. Anchor the Hard Fault Time

- Prefer targeted system-level evidence first for OOM or process-kill incidents.
- Usual sources:
  - `messages`
  - `dmesg`
  - `syslog`
  - exported kernel records
- Prefer grepping `oom` and `kwbase` first instead of reading broad system-log ranges.
- Capture the exact timestamp, timezone, process name, and pid when available.
- If the user-reported time and the hard time disagree, report both and use the hard time for the main analysis window.

## 2. Slice Logs Around the Time Anchor

- Narrow the search window before broad log reading.
- Recommended windows when log volume is high:
  - `30 minutes before`
  - `10 minutes before`
  - `1 minute before`
- Look for:
  - the first decisive crash or severity line
  - repeated amplifier events
  - repeated SQL objects, table names, node ids, or modules
- Common amplifier patterns:
  - `retry`
  - `context canceled`
  - `schema version`
  - `alter`
  - `add column`
  - `add tag`
  - `node unavailable`

## 3. Map Logs To The Smallest Useful Source Call Chain

- This step is optional and requires source access.
- Start from the exact log phrase, file suffix, function name, SQL object, or module hint.
- Find the log-print site first, then connect the shortest closed path:
  - entry path
  - middle execution layer
  - engine or storage layer
- The goal is not to prove one exact bad line immediately.
- A valid intermediate result is a tight set of `3-5` suspicious modules that explain the observed chain.

## 4. Optional History Attribution Extension

- This step is optional and requires source access plus an explicit user request for branch, commit, or history tracing.
- Do not start with git history before the code path is grounded.
- After the code path is confirmed:
  - use `git blame` for the current responsibility lines
  - use `git log --follow` for file evolution
  - use `git log -S` or `git log -G` for behavior-changing strings
- Distinguish:
  - current responsibility line author
  - recent active modifier of the module
- Cite a commit only when it matches both the code path and the incident symptom.

## 5. Produce The Overall Analysis

- State:
  - confirmed timeline
  - primary amplifier or bottleneck
  - suspicious modules when source access exists
  - remaining gaps needed for closure
- If branch or commit cannot be narrowed to one answer, say that directly.

## Useful Commands

```bash
rg -n "auto add column|node unavailable|context canceled" /path/to/logs
rg -n "file.go:[0-9]+|cpp:[0-9]+" /path/to/logs
grep -iE 'oom|kwbase' /var/log/messages
grep -iE 'oom|kwbase' /var/log/syslog
dmesg -T | grep -iE 'oom|kwbase'
git -C /path/to/repo blame -L 120,180 pkg/sql/rowexec/tsInserter.go
git -C /path/to/repo log --follow -- pkg/sql/rowexec/tsInserter.go
git -C /path/to/repo log -S "auto add column" -- pkg/sql/opt/optbuilder/insert.go
```
