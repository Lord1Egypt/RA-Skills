# Evidence Rules

## Conclusion Depth

- `evidence conclusion`
  - based on logs, metrics, system evidence, SQL text, or timeline only
- `source-level localization`
  - evidence conclusion plus a source path and the smallest useful call chain
- `history attribution`
  - source-level localization plus git-history analysis
  - use only when the user explicitly asked for branch, commit, or code-history tracing
- `pattern-consistent`
  - version, timeline, and symptom strongly match a known fault pattern
  - use when the pattern is strong but exact external confirmation is unavailable

## Statement Rules

- separate direct evidence from inference
- when the evidence supports more than one candidate, rank the leading possibilities instead of forcing a single answer
- distinguish `earliest exposed node` from `root cause` in cluster incidents
- separate the primary fault from amplifiers such as retries, backpressure, or restart-side symptoms
- when citing code, include the source path and the log, metric, or SQL evidence that led to it

## Do Not Overclaim

- do not call a branch or commit confirmed unless the code path and symptom both match
- do not treat a similar official issue as proof
- do not treat source correlation as required for an evidence conclusion
- do not collapse `pattern-consistent` into `confirmed by issue lookup`

## Known-Pattern Usage

- if the customer cannot access issue trackers, internal bug systems, or release-management links, do not block diagnosis on external retrieval
- when version, timeline, and symptom strongly match a known fault pattern, you may say that the case is `高度吻合某类已知问题模式`
- clearly distinguish `pattern-consistent` from `fully confirmed by issue lookup`
