---
name: memory-router
description: "Central dispatch layer for OpenClaw Memory Stack. Routes memory queries to the best backend via signal detection, class-based dispatch, and sequential fallback."
license: MIT
metadata:
  authors: "OpenClaw Memory Stack"
  version: "0.1.0"
---

# Memory Router — SKILL.md

## Overview

Memory Router is the central dispatch layer of the OpenClaw Memory Stack. It receives memory queries from the AI agent and routes them to the appropriate backend based on a deterministic rule table with sequential fallback. It is **not** an AI-powered optimizer — it is a rule-based router with explicit signal matching and a well-defined fallback chain.

**How it works:**
1. Read `~/.openclaw/state/backends.json` to discover which backends are installed.
2. Match the incoming query against the routing rule table (top-to-bottom, first match wins).
3. Dispatch to the primary backend.
4. If the result is poor (normalized_relevance < 0.4, status = empty, or status = error), fall back sequentially through the fallback chain.
5. Return the best result found, wrapped in the router envelope.

The router adds zero storage — it is purely a dispatch and fallback coordinator. All actual memory operations happen in the backends.

## Prerequisites

- `~/.openclaw/state/backends.json` must exist and list installed backends.
- At least one backend must be installed (QMD and Total Recall are included in the default install).
- The router itself has no runtime dependencies beyond the ability to read JSON and invoke backend skills.

## Routing Rules

### Tier-Aware Backend Discovery

Before evaluating rules, the router reads `~/.openclaw/state/backends.json` to build the **candidate list** of available backends. If a backend appears in a routing rule but is not in the candidate list, it is silently skipped — no error, no warning. The fallback chain advances to the next available backend.

**Default install** (QMD + Total Recall): Cognee and Lossless rules are effectively disabled — queries that would route to them fall through to QMD or Total Recall alternatives automatically.

**Full install** (all 4 backends): The full routing table is active. Install Cognee and Lossless separately to enable their routing rules.

### Rule Table

Rules are evaluated top-to-bottom. The first rule whose signal matches the query wins. If no rule matches, the default rule applies.

| # | Signal in Query | Primary Backend | Fallback Chain | Rationale |
|---|----------------|----------------|----------------|-----------|
| 1 | Exact symbol, function name, class name, method name (`find function`, `find class`, `find method`, or a CamelCase/snake_case identifier) | QMD (`search` mode) | Total Recall | BM25 excels at exact token matching on code identifiers |
| 2 | Relationship query: "how does X relate to Y", "dependency between", "connection between", "what depends on", "call chain", "trace from...to" | Cognee | QMD (`vsearch`) > Total Recall | Graph traversal is required to follow entity relationships |
| 3 | Decision recall: "what did we decide about", "earlier in conversation", "decision from", "why did we choose", "recall the decision" | Lossless | Total Recall > QMD (`search`) | DAG preserves causal decision chains from conversation history |
| 4 | Concept/behavior query: "how does X work", "where is Y handled", "explain the...strategy", "what is the approach for" | QMD (`vsearch` mode) | QMD (`query`) > Total Recall | Vector semantic search finds conceptually related code |
| 5 | Recent context: "just discussed", "few minutes ago", "last change", "what was the last thing", "recently" | Total Recall | QMD (`search`) | Time-decay relevance prioritizes recent memories |
| 6 | File/path pattern: "in src/auth/", "*.swift files", file path segments, glob patterns | QMD (`search` mode) | Total Recall | BM25 path-based search matches filesystem patterns |
| 7 | Ambiguous / no clear signal (single words, vague references, catch-all) | QMD (`query` mode) | Total Recall | Hybrid search (BM25 + vector) is the safest default for unclear intent |

**Rule 7 is the default rule.** If no signal from rules 1-6 is detected, the query routes to QMD hybrid search.

### Signal Detection

Signal matching uses keyword and pattern detection, not semantic understanding. The router looks for:

- **Rule 1 (exact symbol)**: Query contains `find.*function`, `find.*class`, `find.*method`, `find all usages of`, `search for`, or a token that matches CamelCase/snake_case identifier patterns.
- **Rule 2 (relationship)**: Query contains `relate`, `relationship`, `depends on`, `dependency`, `connection`, `call chain`, `trace.*to`, `path between`.
- **Rule 3 (decision recall)**: Query contains `decide`, `decision`, `chose`, `why did we`, `recall.*decision`, `earlier in conversation`, `morning session`, `afternoon session`.
- **Rule 4 (concept/behavior)**: Query contains `how does.*work`, `where is.*handled`, `explain`, `strategy`, `approach for`, `what is the.*for`.
- **Rule 5 (recent context)**: Query contains `just discussed`, `few minutes ago`, `last change`, `recently`, `last thing`, `what was the last`.
- **Rule 6 (file/path)**: Query contains file path separators (`/`), glob patterns (`*`, `**`), or file extensions (`.ts`, `.swift`, `.py`, etc.).
- **Rule 7 (default)**: No signal detected from rules 1-6.

## Fallback Logic

The fallback mechanism is sequential and deterministic:

1. **Dispatch to primary backend** per the matched rule.
2. **Evaluate the response:**
   - `normalized_relevance >= 0.4` AND `status = success` — Accept the result. Done.
   - `normalized_relevance < 0.4` OR `status = empty` — Result is insufficient. Move to next backend in fallback chain.
   - `status = error` — Immediate fallback. Log the error to `~/.openclaw/state/router.log`.
3. **Timeout enforcement:** The router measures wall-clock time for each backend call. If a backend exceeds 5000ms, the router marks the response as `QUERY_TIMEOUT` and moves to the next backend in the chain.
4. **Chain exhaustion:** If the entire fallback chain is exhausted without a good result (normalized_relevance >= 0.4), the router returns the **best result found across all attempted backends** (even if < 0.4) with `status: partial`.
5. **Total failure:** If every backend in the chain returns `status = error`, the router returns:

```json
{
  "status": "error",
  "error_code": "ALL_BACKENDS_FAILED",
  "error_message": "All backends in the fallback chain failed. Check ~/.openclaw/state/router.log for details."
}
```

### Fallback Behavior with Missing Backends

When a backend in the fallback chain is not installed (not in `backends.json`), the router skips it silently and advances to the next entry. This is how default install works naturally — Cognee and Lossless are simply not in the candidate list, so rules 2 and 3 fall through to their QMD/Total Recall alternatives.

**Example — Rule 2 without Cognee installed:**
- Primary: Cognee (not installed) — skip
- Fallback 1: QMD vsearch — execute
- Fallback 2: Total Recall — execute if QMD result is poor

## Few-Shot Routing Examples

### Clear Queries (10)

**1. "find the function parseAuthToken"**
- Signal: `find.*function` + CamelCase identifier
- Rule matched: #1 (exact symbol)
- Routed to: QMD `search` mode
- Fallback chain: [Total Recall]

**2. "how does the auth middleware relate to the session store"**
- Signal: `relate` keyword, two identifiable entities
- Rule matched: #2 (relationship)
- Routed to: Cognee (if installed), else QMD `vsearch`
- Fallback chain: [QMD vsearch, Total Recall]

**3. "what did we decide about the database schema in the morning session"**
- Signal: `decide` keyword, `morning session`
- Rule matched: #3 (decision recall)
- Routed to: Lossless (if installed), else Total Recall
- Fallback chain: [Total Recall, QMD search]

**4. "how does error handling work in the API layer"**
- Signal: `how does.*work`
- Rule matched: #4 (concept/behavior)
- Routed to: QMD `vsearch`
- Fallback chain: [QMD query, Total Recall]

**5. "what was the last thing we changed"**
- Signal: `last thing`
- Rule matched: #5 (recent context)
- Routed to: Total Recall
- Fallback chain: [QMD search]

**6. "search in src/models/*.ts"**
- Signal: file path separator `/`, glob pattern `*`, extension `.ts`
- Rule matched: #6 (file/path pattern)
- Routed to: QMD `search`
- Fallback chain: [Total Recall]

**7. "find all usages of UserService"**
- Signal: `find all usages of` + CamelCase identifier
- Rule matched: #1 (exact symbol)
- Routed to: QMD `search`
- Fallback chain: [Total Recall]

**8. "what's the relationship between OrderController and PaymentService"**
- Signal: `relationship` keyword, two CamelCase entities
- Rule matched: #2 (relationship)
- Routed to: Cognee (if installed) / QMD vsearch (fallback)
- Fallback chain: [QMD vsearch, Total Recall]

**9. "recall the architecture decision from this morning"**
- Signal: `recall.*decision`, `morning`
- Rule matched: #3 (decision recall)
- Routed to: Lossless (if installed) / Total Recall (fallback)
- Fallback chain: [Total Recall, QMD search]

**10. "explain the caching strategy"**
- Signal: `explain`, `strategy`
- Rule matched: #4 (concept/behavior)
- Routed to: QMD `vsearch`
- Fallback chain: [QMD query, Total Recall]

### Ambiguous Queries (5)

**11. "auth"**
- Signal: Single word, no verb, no clear pattern.
- Rule matched: #7 (default — no signal detected)
- Routed to: QMD `query` (hybrid search)
- Fallback chain: [Total Recall]
- Rationale: Single words have no clear intent. Hybrid search (BM25 + vector) covers the most ground. Could be a symbol name, a concept, or a path fragment — QMD query handles all three reasonably.

**12. "that thing with the tokens"**
- Signal: Vague demonstrative "that thing" hints at recent context, but no explicit recency keyword.
- Rule matched: #5 (recent context — weak signal from "that thing")
- Routed to: Total Recall
- Fallback chain: [QMD query]
- Rationale: "that thing" is a conversational back-reference suggesting the user means something discussed recently. Total Recall's time-decay scoring gives the best chance. If nothing recent matches, QMD hybrid search broadens the scope.

**13. "database"**
- Signal: Single word, no verb, no clear pattern.
- Rule matched: #7 (default — no signal detected)
- Routed to: QMD `query` (hybrid search)
- Fallback chain: [Total Recall]
- Rationale: Could mean schema, configuration, relationship, migration, or connection string. Hybrid search is the safest bet for a single ambiguous term.

**14. "why did we do it that way"**
- Signal: `why did we` maps to decision recall.
- Rule matched: #3 (decision recall)
- Routed to: Lossless (if installed) / Total Recall (fallback)
- Fallback chain: [Total Recall, QMD search]
- Rationale: "why did we" is a strong decision-recall signal. The user wants the reasoning behind a past choice. Lossless DAG traces causal chains to reconstruct the decision rationale.

**15. "the middleware issue"**
- Signal: No verb, no clear pattern. "issue" is generic — could be a bug, a relationship, or recent context.
- Rule matched: #7 (default — no signal detected)
- Routed to: QMD `query` (hybrid search)
- Fallback chain: [Total Recall]
- Rationale: "the middleware issue" is too vague for any specialized backend. Hybrid search maximizes the chance of finding relevant content regardless of whether it was stored as a decision, a code change, or a concept note.

## Output Format

The router wraps backend responses in a router envelope that adds routing metadata:

```json
{
  "query_echo": "original query",
  "routed_to": "qmd",
  "routed_mode": "search",
  "fallback_chain": ["qmd", "totalrecall"],
  "fallbacks_used": 0,
  "results": [
    {
      "content": "matched content...",
      "relevance": 0.82,
      "source": "qmd",
      "timestamp": "2026-03-10T14:30:00Z"
    }
  ],
  "result_count": 2,
  "normalized_relevance": 0.82,
  "status": "success",
  "router_duration_ms": 340,
  "backend_duration_ms": 230
}
```

### Router Envelope Fields

| Field | Type | Description |
|-------|------|-------------|
| `query_echo` | string | The original query string, unchanged |
| `routed_to` | string | Backend that produced the returned results (`qmd`, `totalrecall`, `cognee`, `lossless`) |
| `routed_mode` | string \| null | Mode used for the winning backend (e.g., `search`, `vsearch`, `query` for QMD; null for other backends) |
| `fallback_chain` | string[] | The complete fallback chain that was planned for this query |
| `fallbacks_used` | int | Number of fallbacks that were actually triggered (0 = primary succeeded) |
| `results` | array | Standard result array from the winning backend (same structure as backend contract) |
| `result_count` | int | Number of results returned |
| `normalized_relevance` | float | The normalized relevance score from the winning backend (0.0-1.0). This is the value used for fallback decisions. |
| `status` | string | `success`, `partial`, `empty`, or `error` |
| `router_duration_ms` | int | Total wall-clock time for the entire routing operation (including all fallbacks) |
| `backend_duration_ms` | int | Duration of the winning backend call only |

### Status Values

| Status | Meaning |
|--------|---------|
| `success` | Primary or fallback backend returned normalized_relevance >= 0.4 |
| `partial` | Entire fallback chain exhausted; returning best result found (< 0.4) |
| `empty` | All backends returned no results |
| `error` | All backends failed (see `error_code` and `error_message`) |

## Error Handling

### Backend Not Installed
If a backend appears in a routing rule but is not listed in `~/.openclaw/state/backends.json`, the router skips it and advances to the next entry in the fallback chain. No error is logged — this is expected behavior for partial installs.

### Backend Returns Error
Log the error to `~/.openclaw/state/router.log` with timestamp, backend name, error code, and error message. Then advance to the next entry in the fallback chain.

### Backend Timeout
If a backend call exceeds 5000ms (measured by the router), mark the response as `QUERY_TIMEOUT`, log it, and advance to the next entry in the fallback chain.

### All Backends Fail
Return:
```json
{
  "query_echo": "original query",
  "routed_to": null,
  "fallback_chain": ["qmd", "totalrecall"],
  "fallbacks_used": 2,
  "results": [],
  "result_count": 0,
  "status": "error",
  "error_code": "ALL_BACKENDS_FAILED",
  "error_message": "All backends in the fallback chain failed. Check ~/.openclaw/state/router.log for details.",
  "router_duration_ms": 10200,
  "backend_duration_ms": 0
}
```

### Router Log Format
Each log entry in `~/.openclaw/state/router.log`:
```
[2026-03-17T14:30:00Z] FALLBACK query="auth middleware" backend=cognee error_code=BACKEND_ERROR error_message="Python process exited with code 1" next=qmd
[2026-03-17T14:30:01Z] TIMEOUT query="auth middleware" backend=qmd duration_ms=5230 next=totalrecall
```

## Configuration

The router reads two configuration sources:

1. **`~/.openclaw/state/backends.json`** — Dynamic state file listing installed backends and their status.
2. **`router-config.json`** (alongside this file) — Static routing rules, thresholds, and tier configuration.

The router does not write to `backends.json` — that file is managed by the installer (`setup.sh` / `install-pro.sh`).

## Limitations

- **No learning or adaptation.** The router uses static rules. It does not learn from past query patterns or adjust routing based on backend performance over time.
- **Signal detection is keyword-based.** The router cannot understand nuance. A query like "show me the auth flow" might match rule 4 (concept) when the user actually wanted rule 2 (relationship). The fallback chain mitigates this.
- **No multi-backend merging.** The router returns results from a single backend (the first one that meets the relevance threshold). It does not merge or deduplicate results across backends.
- **Fallback adds latency.** Each fallback attempt adds the backend's response time. In the worst case (all backends timeout), the router takes 3-4x the single-backend timeout.
- **Rule order matters.** Rules are evaluated top-to-bottom. If a query matches both rule 2 (relationship) and rule 4 (concept), rule 2 wins because it appears first. This is by design but may occasionally route to a suboptimal backend.

## Tier

**Default install** — The router itself is always available. Its effectiveness scales with the number of installed backends: default install routes to QMD and Total Recall; installing Cognee and Lossless unlocks their routing rules.
