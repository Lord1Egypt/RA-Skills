# MemoClaw usage examples

## Example 1: CLI basics

The fastest way to use MemoClaw. Install once, then store and recall from any shell.

```bash
# Setup (one-time)
npm install -g memoclaw
memoclaw init    # Interactive wallet setup — saves to ~/.memoclaw/config.json
memoclaw status  # Check your free tier remaining

# Store a memory
memoclaw store "User prefers vim keybindings" --importance 0.8 --tags tools,preferences --memory-type preference

# Recall memories
memoclaw recall "editor preferences" --limit 5

# Full-text keyword search (free, no embeddings)
memoclaw search "vim" --namespace default
```

## Example 2: OpenClaw agent session

Typical flow for an OpenClaw agent using MemoClaw throughout a session:

```bash
# Session start — load relevant context
memoclaw context "user preferences and recent decisions" --limit 10

# User says "I switched to Neovim last week"
memoclaw recall "editor preferences"         # check for existing memory
memoclaw store "User switched to Neovim (Feb 2026)" \
  --importance 0.85 --tags preferences,tools --memory-type preference

# User asks "what did we decide about the database?"
memoclaw recall "database decision" --namespace project-alpha

# Session end — store a summary
memoclaw store "Session 2026-02-16: Discussed editor migration, reviewed DB schema" \
  --importance 0.6 --tags session-summary --memory-type observation

# Periodic maintenance
memoclaw consolidate --namespace default --dry-run
memoclaw suggested --category stale --limit 5
```

## Example 3: Ingesting raw text

Feed a conversation or document and let MemoClaw extract, deduplicate, and relate facts automatically.

```bash
# Extract facts from a sentence
memoclaw ingest --text "User's name is Ana. She lives in São Paulo. She works with TypeScript."

# Or from a file
cat conversation.txt | memoclaw ingest --namespace default --auto-relate

# Extract without dedup (just parse facts)
memoclaw extract "I prefer dark mode and use 2-space indentation"
```

## Example 4: Project namespaces

Keep memories organized per project.

```bash
# Store architecture decisions scoped to a project
memoclaw store "Team chose PostgreSQL over MongoDB for ACID requirements" \
  --importance 0.9 --tags architecture,database --namespace project-alpha --memory-type decision

# Recall only from that project
memoclaw recall "what database did we choose?" --namespace project-alpha

# List all namespaces
memoclaw namespace list

# Export a project's memories
memoclaw export --format markdown --namespace project-alpha
```

## Example 5: Memory lifecycle

Storing, updating, pinning, relating, and deleting.

```bash
# Store
memoclaw store "User timezone is America/Sao_Paulo (UTC-3)" \
  --importance 0.7 --tags user-info --memory-type preference


# Update when things change
memoclaw update <uuid> --content "User timezone is America/New_York (UTC-5)" --importance 0.8

# Pin a memory so it never decays
memoclaw update <uuid> --pinned true

# Link related memories
memoclaw relations create <uuid-1> <uuid-2> supersedes

# View change history
memoclaw history <uuid>

# Delete when no longer relevant
memoclaw delete <uuid>
```

## Example 6: Consolidation and maintenance

Over time, memories fragment. Consolidate periodically.

```bash
# Preview what would merge (dry run)
memoclaw consolidate --namespace default --dry-run

# Actually merge duplicates
memoclaw consolidate --namespace default

# Find stale memories worth reviewing
memoclaw suggested --category stale --limit 10

# Bulk delete an old project
memoclaw purge --namespace old-project
```

## Example 7: Migrating from local markdown files

If you've been using `MEMORY.md` or `memory/*.md` files:

```bash
# Import all .md files at once
memoclaw migrate ./memory/

# Verify what was stored
memoclaw list --limit 50
memoclaw recall "user preferences"

# Pin the essentials
memoclaw update <id> --pinned true
```

Run both systems in parallel for a week before phasing out local files.

## Example 8: Interactive browse session

Use the built-in REPL to explore and manage memories interactively.

```bash
# Launch interactive browser
memoclaw browse

# Inside the REPL you can:
# - Search and recall memories
# - View details, update importance, pin/unpin
# - Delete or relate memories
# - Navigate namespaces
```

## Example 9: Multi-agent namespace patterns

When multiple agents share a wallet but need isolation:

```bash
# Agent A stores project context
memoclaw store "API uses REST with JSON:API spec" \
  --importance 0.85 --namespace project-backend --memory-type decision \
  --tags architecture,api

# Agent B stores frontend decisions separately
memoclaw store "Using React 19 with Server Components" \
  --importance 0.85 --namespace project-frontend --memory-type decision \
  --tags architecture,frontend

# Either agent can cross-query when needed
memoclaw recall "what tech stack are we using?" --namespace project-backend
memoclaw recall "frontend framework" --namespace project-frontend

# List all namespaces to see the full picture
memoclaw namespace list
```

## Example 10: Automated session summarization

Store structured session summaries for continuity across sessions.

```bash
# At session end, store a structured summary
memoclaw store "Session 2026-02-28: Refactored auth module to use JWT. \
Decided to drop session cookies. User wants migration script by Friday. \
Open question: Redis vs Postgres for token blacklist." \
  --importance 0.7 --tags session-summary --memory-type observation \
  --namespace project-backend

# Next session start — recall recent summaries
memoclaw recall "recent session summaries and open questions" --limit 5

# Periodically consolidate session summaries to avoid fragmentation
memoclaw consolidate --namespace project-backend --dry-run
```

## Example 11: Error recovery and graceful degradation

What to do when things go wrong — keep helping the user regardless.

```bash
# Check if MemoClaw is reachable before a session
memoclaw config check && memoclaw status
# If this fails: fall back to local files for this session

# Handle "402 Payment Required" — free tier exhausted
memoclaw status                    # confirm free_calls_remaining is 0
memoclaw whoami                    # get wallet address to fund
# Fund wallet with USDC on Base, then retry

# Handle "409 Conflict" — tried to update an immutable memory
# Don't try to update it. Store a new memory and link them:
memoclaw store "Updated: user now prefers spaces (was tabs)" \
  --importance 0.85 --memory-type preference --tags code-style
memoclaw relations create <new-id> <old-id> supersedes

# Handle "413 Payload Too Large" — content over 8192 chars
# Split the content into smaller chunks:
memoclaw extract "First half of the long content..."
memoclaw extract "Second half of the long content..."

# Handle network errors — API unreachable
# Write to a local scratch file and sync later:
echo "User prefers dark mode (importance: 0.8)" >> /tmp/memoclaw-pending.txt
# Next session, when API is back:
cat /tmp/memoclaw-pending.txt | memoclaw ingest && rm /tmp/memoclaw-pending.txt
```

**Key principle:** Never let a MemoClaw outage block the user. Fall back to local files, note what needs syncing, and catch up when the API returns.

## Example 12: Cost-aware session patterns

Keep costs predictable by using free commands first and paid ones only when needed.

```bash
# === BUDGET-FRIENDLY SESSION START ===
# Step 1: Free — load pinned + high-importance memories
memoclaw core --limit 5

# Step 2: Free — keyword check for recent context
memoclaw search "project-alpha" --since 7d

# Step 3: Paid ($0.005) — only if free methods didn't surface what you need
memoclaw recall "user's deployment preferences" --since 7d --limit 3

# === DURING SESSION ===
# Before storing, always check if it already exists (free search first)
memoclaw search "dark mode"              # free keyword check
# Only if not found:
memoclaw store "User prefers dark mode" --importance 0.8 --memory-type preference

# === SESSION END ===
# One store for the summary ($0.005)
memoclaw store "Session 2026-03-12: reviewed CI pipeline, user wants faster deploys" \
  --importance 0.6 --tags session-summary --memory-type observation

# === DAILY COST ESTIMATE ===
# 3 stores + 2 recalls = 5 × $0.005 = $0.025/day
# Everything else (list, search, core, stats) is free
```

**Monthly cost at different usage levels:**

| Style | Paid calls/day | Daily cost | Monthly cost |
|-------|---------------|------------|-------------|
| Light (hobbyist) | 3-5 | $0.015-0.025 | ~$0.50-0.75 |
| Moderate (daily agent) | 10-20 | $0.05-0.10 | ~$1.50-3.00 |
| Heavy (multi-agent) | 30-50 | $0.15-0.25 | ~$4.50-7.50 |

## Example 13: Piping and scripting patterns

Combine MemoClaw with standard Unix tools for powerful workflows.

```bash
# Export all high-importance memories as plain text
memoclaw list --sort-by importance --limit 20 --raw

# Get just the IDs of memories matching a tag
memoclaw list --tags preferences --json | jq -r '.memories[].id'

# Bulk pin all memories with "critical" tag
memoclaw list --tags critical --json | jq -r '.memories[].id' | \
  xargs -I{} memoclaw pin {}

# Move all stale memories to an archive namespace
memoclaw suggested --category stale --json | jq -r '.suggested[].id' | \
  memoclaw move --namespace archive

# Count memories by type
memoclaw list --json --limit 1000 | jq '.memories | group_by(.memory_type) | map({type: .[0].memory_type, count: length})'

# Back up a namespace to a file before purging
memoclaw export --format json --namespace old-project --output backup-old-project.json
memoclaw purge --namespace old-project --force

# Diff all memories that changed this week
memoclaw list --since 7d --json | jq -r '.memories[].id' | \
  xargs -I{} sh -c 'echo "=== {} ===" && memoclaw diff {} 2>/dev/null'

# Pipe recall results into another tool
memoclaw recall "deployment process" --raw | pbcopy   # copy to clipboard (macOS)
memoclaw recall "API endpoints" --raw > context.txt   # save to file for LLM prompt
```

## Cost breakdown

For a typical agent running daily:

| Activity | Operations | Cost |
|----------|-----------|------|
| 10 stores | 10 × $0.005 | $0.05 |
| 20 recalls | 20 × $0.005 | $0.10 |
| 2 list queries | Free | $0.00 |
| **Total** | | **~$0.15/day** |

Under $5/month for continuous agent memory. First 100 calls are free.
