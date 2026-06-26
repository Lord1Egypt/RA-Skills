---
name: memory-totalrecall
description: "Total Recall memory backend — git-branch-based persistent memory store with time-decay relevance."
license: MIT
metadata:
  authors: "OpenClaw Memory Stack"
  version: "0.1.0"
---

# Total Recall — SKILL.md

## Overview

Total Recall is a git-based memory backend that stores memories as structured markdown files on a dedicated orphan branch (`openclaw-memory`) within your existing project repository. It requires zero external dependencies beyond git itself, making it the simplest backend to deploy and the most portable across environments. Each memory is a timestamped markdown file in a `_memory/` directory, committed with a searchable commit message. Retrieval uses git's built-in search (`git log --grep`, `git grep`). Relevance scoring is time-based: recent memories rank higher than older ones. Total Recall is ideal for conversation history, architectural decisions, and context snapshots in any project where installing additional tooling is impractical or undesirable.

## Prerequisites

- **Git** (version >= 2.20) — pre-installed on macOS and most Linux distributions.
- A POSIX shell (bash or zsh).
- No external services, databases, or runtimes required.

Verify with:
```bash
git --version
```

## Configuration

Configuration is stored in `config.json` alongside this file. The router reads it to understand backend capabilities.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `backend` | string | `"totalrecall"` | Backend identifier for the router |
| `branch` | string | `"openclaw-memory"` | Orphan branch where memories are stored |
| `memory_dir` | string | `"_memory"` | Directory within the branch for memory files |
| `file_format` | string | `"markdown"` | File format for stored memories |
| `relevance.method` | string | `"time_decay"` | Relevance scoring method |
| `relevance.formula` | string | `"max(0.2, 1.0 - (days_ago * 0.043))"` | Continuous decay formula |
| `relevance.today` | float | `1.0` | Score for memories from today |
| `relevance.this_week` | float | `0.7` | Score for memories from this week |
| `relevance.this_month` | float | `0.4` | Score for memories from this month |
| `relevance.older` | float | `0.2` | Floor score for older memories |
| `search.max_results` | int | `20` | Maximum results per query |
| `store.commit_prefix` | string | `"memory:"` | Prefix for commit messages |

## Usage

All operations target the `openclaw-memory` orphan branch. The agent reads and writes memory files on this branch using `git show` and `git checkout` commands, avoiding disruption to the working tree. Alternatively, use `git worktree` for a persistent second checkout.

### Store

To store a memory with key `auth-decision`:

```bash
# Save current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Switch to memory branch
git checkout openclaw-memory

# Create memory file with structured content
TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%S")
FILENAME="_memory/${TIMESTAMP}_auth-decision.md"

cat > "$FILENAME" << 'MEMORY_EOF'
---
key: auth-decision
timestamp: 2026-03-17T14:30:00Z
tags: [auth, architecture, decision]
---

# Auth Decision

We chose JWT with RS256 signing for the auth middleware.
Refresh tokens use httpOnly cookies for storage.
MEMORY_EOF

# Commit the memory
git add "$FILENAME"
git commit -m "memory: auth-decision — JWT auth middleware decision"

# Return to working branch
git checkout "$CURRENT_BRANCH"
```

**File naming convention**: `{ISO-timestamp}_{slugified-key}.md`
- Timestamp format: `YYYY-MM-DDTHH-MM-SS` (colons replaced with hyphens for filesystem safety)
- Key slug: lowercase, hyphens for spaces, alphanumeric and hyphens only

**Commit message convention**: `memory: {key} — {brief description}`
This convention enables `git log --grep` to find memories by key.

### Retrieve

To retrieve a memory by key:

```bash
# Search for the key in commit messages on the memory branch
git log openclaw-memory --grep="memory: auth-decision" --format="%H %ai %s" --max-count=5

# Get the file path from the most recent matching commit
COMMIT_HASH=$(git log openclaw-memory --grep="memory: auth-decision" --format="%H" --max-count=1)
FILEPATH=$(git diff-tree --no-commit-id --name-only -r "$COMMIT_HASH" | grep "_memory/")

# Read the file content without switching branches
git show "openclaw-memory:$FILEPATH"
```

**Output construction** — build the contract JSON from the results:

```json
{
  "query_echo": "auth-decision",
  "results": [
    {
      "content": "We chose JWT with RS256 signing for the auth middleware...",
      "relevance": 1.0,
      "source": "totalrecall",
      "timestamp": "2026-03-17T14:30:00Z"
    }
  ],
  "result_count": 1,
  "status": "success",
  "error_message": null,
  "error_code": null,
  "backend_duration_ms": 45,
  "normalized_relevance": 1.0,
  "backend": "totalrecall"
}
```

### Search

To search memories by pattern across all memory files:

```bash
# Search commit messages for pattern
git log openclaw-memory --grep="auth" --format="%H %ai %s"

# Search file contents on the memory branch for a pattern
git grep -l "JWT" openclaw-memory -- "_memory/"

# Read matching files
for FILE in $(git grep -l "JWT" openclaw-memory -- "_memory/"); do
  echo "--- $FILE ---"
  git show "$FILE"
done
```

For broader search with context:

```bash
# Full-text search with surrounding lines
git grep -n -C 2 "pattern" openclaw-memory -- "_memory/"

# Case-insensitive search
git grep -il "jwt" openclaw-memory -- "_memory/"
```

## Interface Contract

### Input

- `store(key, content, metadata?)` — Create a markdown file on the memory branch and commit it.
- `retrieve(query, options?)` — Search commit messages with `git log --grep`, read matching files via `git show`.
- `search(pattern, scope?)` — Search file contents with `git grep` on the memory branch.

### Output Format

All backends return the same JSON structure:

```json
{
  "query_echo": "original query string",
  "results": [
    {
      "content": "...",
      "relevance": 0.0,
      "source": "totalrecall",
      "timestamp": "ISO8601"
    }
  ],
  "result_count": 0,
  "status": "success | partial | empty | error",
  "error_message": null,
  "error_code": null,
  "backend_duration_ms": 0,
  "normalized_relevance": 0.0,
  "backend": "totalrecall"
}
```

### Failure Codes

| Code | Meaning |
|------|---------|
| `BACKEND_UNAVAILABLE` | Git not installed, not in a git repo, or memory branch missing |
| `QUERY_TIMEOUT` | Exceeded 5s (router-measured) |
| `EMPTY_RESULT` | Query succeeded but no matching memories found |
| `PARTIAL_RESULT` | Some results returned but search may be incomplete |
| `BACKEND_ERROR` | Git command failed (see error_message for stderr) |

### Relevance Normalization

Total Recall uses **time-decay** relevance scoring. There is no semantic similarity — relevance is purely a function of how recently the memory was stored.

**Formula**:
```
relevance = max(0.2, 1.0 - (days_ago * 0.043))
```

This produces a continuous decay curve that roughly aligns with these buckets:

| Age | Score | Calculation |
|-----|-------|-------------|
| Today (0 days) | 1.0 | max(0.2, 1.0 - 0) |
| 3 days ago | 0.871 | max(0.2, 1.0 - 0.129) |
| 7 days ago | 0.699 | max(0.2, 1.0 - 0.301) |
| 14 days ago | 0.398 | max(0.2, 1.0 - 0.602) |
| 19+ days ago | 0.2 | max(0.2, ...) = floor |

The `normalized_relevance` field in the response is the highest relevance score among all results. When multiple results match, they are sorted by relevance (most recent first).

### Router Integration

- Normalized relevance >= 0.4 -> "good enough", no fallback needed.
- Normalized relevance < 0.4 or status = empty -> trigger fallback to another backend.
- status = error -> immediate fallback, log error.

## Limitations

- **No semantic search.** Total Recall uses literal text matching (`git grep`). It cannot understand that "authentication" and "login" are related concepts. If the query uses different words than the stored memory, it will not match.
- **No relationship or graph queries.** Cannot answer "what decisions led to X" unless those links are explicitly stored in the memory content.
- **Time-based relevance only.** A highly relevant old memory scores lower than a trivial recent one. The scoring model has no understanding of content importance.
- **Branch switching overhead.** Store operations require switching to the memory branch and back, which can be disruptive during active development. Use `git worktree` to mitigate this.
- **Linear scaling.** Search performance degrades linearly with the number of stored memories. Git grep is fast, but thousands of memory files will eventually slow down.
- **No concurrent writes.** Git does not support concurrent commits safely. Simultaneous store operations from multiple agents may conflict.
- **Keyword matching is case-sensitive by default.** Use `-i` flag with `git grep` and `git log --regexp-ignore-case` for case-insensitive matching.

## Tier

**Starter** — Free and open source (MIT). Zero additional cost, zero additional dependencies.
