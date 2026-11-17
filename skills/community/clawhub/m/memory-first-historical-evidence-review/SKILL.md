---
name: "memory-first-historical-evidence-review"
description: "Historical debug review: read dated memory first, then narrow raw session evidence only where memory leaves a causal gap."
---

# memory-first-historical-evidence-review

Use when answering questions about what earlier runs established, especially incident causality across multiple dates.

1. Start with dated memory or other curated summaries for the suspected dates.
2. Extract a provisional timeline: symptom, verified config/state, observed fallback/path, working explanation.
3. Note which claims are still unsupported or ambiguous.
4. Search raw session logs only for those gaps.
5. Narrow raw-log lookup by known date, session id, or exact phrase from memory. Avoid wide scans across all archives first.
6. If a raw log is noisy or truncated, reduce scope again instead of broadening the search.
7. Answer from the converged evidence. Separate verified cause from likely cause.

Pitfalls:
- Broad grep over archived session files can silently miss matches because of quoting/glob mistakes or return irrelevant/noisy hits.
- Raw session dumps may be truncated; do not treat absence in a noisy scan as disproof.
- Memory is a summary, not ground truth; use it to route investigation, not to invent missing evidence.

Verification:
- Before concluding, cite at least two independent supporting artifacts, or one curated memory entry plus one raw-session excerpt for any disputed claim.
- Confirm the final claim explains the observed symptom better than the discarded hypothesis.
