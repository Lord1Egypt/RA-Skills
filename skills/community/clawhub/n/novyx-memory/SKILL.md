---
name: novyx-memory
description: "Enterprise-grade persistent memory for AI agents — rollback, audit trails, knowledge graph, governed actions, time-travel debugging, and 60+ commands covering 100% of Novyx Core"
version: 3.0.0
homepage: https://novyxlabs.com
metadata:
  openclaw:
    primaryEnv: NOVYX_API_KEY
    requires:
      env:
        - NOVYX_API_KEY
---

# Novyx Memory

The only memory skill with rollback, cryptographic audit trails, and governed actions. 60+ commands covering 100% of Novyx Core — memory, drafts, knowledge graph, context spaces, time-travel replay, eval scoring, execution tracing, and policy-controlled actions.

## Why Novyx Memory

Every other memory skill gives you save and search. Novyx gives you the full stack:

| Capability | Novyx | Built-in | SuperMemory | Mem0 | memory-tools |
|---|---|---|---|---|---|
| Semantic search | ✓ | ✗ | ✓ | ✓ | ✓ |
| Time-travel rollback | ✓ | ✗ | ✗ | ✗ | ✗ |
| Cryptographic audit trail | ✓ | ✗ | ✗ | ✗ | ✗ |
| Draft review workflow | ✓ | ✗ | ✗ | ✗ | ✗ |
| Knowledge graph | ✓ | ✗ | ✗ | ✗ | ✗ |
| Context spaces (multi-agent) | ✓ | ✗ | ✗ | ✗ | ✗ |
| Governed actions | ✓ | ✗ | ✗ | ✗ | ✗ |
| Execution tracing | ✓ | ✗ | ✗ | ✗ | ✗ |
| Memory health eval | ✓ | ✗ | ✗ | ✗ | ✗ |
| Confidence & decay | ✓ | ✗ | ✗ | ✗ | ✓ |

## When to Use This Skill

- Agent needs memory that persists across sessions
- You need to undo, roll back, or audit what the agent remembered
- Multiple agents need shared context spaces
- Agent actions need policy approval before execution
- You want a knowledge graph built from agent observations
- You need time-travel debugging ("what did the agent know at 3pm?")
- CI pipeline needs a memory health gate

## Automatic Behavior

When active, this skill:
- **Auto-recalls** relevant memories before each response and injects them as context
- **Auto-saves** each user message and agent response to persistent storage
- Skips trivial messages (under 15 characters) to conserve API calls
- Filters out previously injected context to prevent feedback loops

## Commands (60+)

### Memory Basics

| Command | What it does |
|---------|-------------|
| `!remember <text> [--tags t1,t2]` | Save a specific fact or note with optional tags |
| `!search <query>` | Semantic search with relevance scores |
| `!list [--tag tag] [--limit N]` | List stored memories with optional filters |
| `!forget <topic>` | Find and delete all memories matching a topic |
| `!undo [N]` | Delete the last N saved memories (default: 1) |
| `!supersede <id> <new text>` | Replace an old memory with a corrected version |

### Draft Review Workflow

Stage memory changes before committing — like git for agent memory.

| Command | What it does |
|---------|-------------|
| `!draft <text> [--branch name]` | Create a reviewable draft |
| `!drafts` | List pending drafts |
| `!draft-diff <id>` | Show field-level diff for a draft |
| `!merge-draft <id>` | Commit draft to canonical memory |
| `!reject-draft <id>` | Reject a draft without saving |
| `!branch <name>` | View all drafts in a branch |
| `!merge-branch <name>` | Merge all drafts in a branch at once |
| `!reject-branch <name>` | Reject all drafts in a branch |

### Memory Links

| Command | What it does |
|---------|-------------|
| `!link <from_id> <to_id> [relation]` | Create a directed link between memories |
| `!unlink <from_id> <to_id>` | Remove a link |
| `!links <memory_id>` | Show all links for a memory |

### Knowledge Graph

Build structured knowledge from unstructured observations.

| Command | What it does |
|---------|-------------|
| `!triple <subject> \| <predicate> \| <object>` | Add a knowledge triple |
| `!triples [--subject x] [--predicate y]` | Query triples with filters |
| `!entities [--type t]` | List all entities |
| `!entity <id>` | Get entity with all connected triples |
| `!del-triple <id>` | Delete a triple |
| `!del-entity <id>` | Delete entity and cascade triples |
| `!graph [--relation r]` | View memory graph edges |

### Context Spaces (Multi-Agent Collaboration)

Isolated memory namespaces that can be shared between agents.

| Command | What it does |
|---------|-------------|
| `!space <name> [--description d]` | Create a context space |
| `!spaces` | List accessible spaces |
| `!space-memories <id> [query]` | List or search within a space |
| `!update-space <id> [--name n]` | Update space metadata |
| `!del-space <id>` | Delete a space (owner only) |
| `!share <space_id> <email>` | Share a space with another user |
| `!shared` | List spaces shared with you |
| `!accept <token>` | Accept a share invitation |
| `!revoke <token>` | Revoke a share |

### Replay (Time-Travel Debugging)

Scrub through the full history of your agent's memory.

| Command | What it does |
|---------|-------------|
| `!timeline [N]` | Full timeline of memory operations |
| `!snapshot <time>` | Reconstruct memory state at a point in time |
| `!lifecycle <id>` | Full biography of a single memory |
| `!replay <id>` | Complete history of a memory |
| `!replay-diff <t1> <t2>` | Diff memory state between two timestamps |
| `!recall-at <time> <query>` | What would search have returned in the past? |
| `!replay-drift <t1> <t2>` | Memory composition drift analysis |

### Audit & Rollback

| Command | What it does |
|---------|-------------|
| `!audit [N]` | Last N operations with SHA-256 hashes (default: 10) |
| `!audit-verify` | Verify cryptographic audit chain integrity |
| `!rollback <time>` | Rewind memory to a point in time ("1h", "2 days ago", ISO) |
| `!rollback-preview <time>` | Preview what rollback would do without executing |
| `!rollback-history` | List past rollback operations |

### Cortex (Autonomous Intelligence)

AI that watches your memory and generates insights automatically.

| Command | What it does |
|---------|-------------|
| `!cortex` | Cortex status and last run |
| `!cortex-run` | Manually trigger a Cortex cycle |
| `!insights` | List auto-generated insights |
| `!cortex-config` | View current configuration |

### Eval (Memory Health Scoring)

Quantify your agent's memory quality with weighted scoring.

| Command | What it does |
|---------|-------------|
| `!eval` | Run memory health evaluation (recall 40%, drift 30%, conflict 15%, staleness 15%) |
| `!eval-gate [threshold]` | CI gate — pass/fail on memory quality (default: 0.7) |
| `!eval-history` | Past evaluation scores with trends |
| `!eval-drift` | Detect memory drift over time |
| `!health` | Quick memory stats overview |

### Tracing (Execution Audit)

Track multi-step agent workflows with cryptographic verification.

| Command | What it does |
|---------|-------------|
| `!trace <name>` | Create a new execution trace |
| `!trace-step <id> <description> [--type THOUGHT\|ACTION\|OBSERVATION]` | Add a step |
| `!trace-complete <id>` | Finalize trace with RSA signature |
| `!trace-verify <id>` | Verify trace chain integrity |

### Control (Governed Actions)

Policy-evaluated agent actions with approval workflows.

| Command | What it does |
|---------|-------------|
| `!pending` | List pending approval requests |
| `!approve <id>` | Approve a pending action |
| `!policy` | View active security policies |
| `!actions [N]` | Recent action history |

### Overview

| Command | What it does |
|---------|-------------|
| `!status` | Memory usage, tier, and rollback count |
| `!dashboard` | Full dashboard with health score and activity |
| `!context` | Current memory context snapshot |
| `!stats` | Detailed memory statistics |
| `!help` | List all 60+ commands |

## Key Differentiators

- **Rollback**: `!rollback 1h` restores memory to exactly one hour ago. No other memory skill supports this.
- **Audit trail**: Every operation logged with SHA-256 hashes forming a tamper-proof chain. `!audit-verify` checks integrity.
- **Draft workflow**: Stage memory changes in branches, review diffs, merge or reject — like git for memory.
- **Knowledge graph**: Build structured triples from unstructured observations. Query relationships, not just content.
- **Context spaces**: Isolated memory namespaces with sharing. Perfect for multi-agent architectures.
- **Governed actions**: Policy-evaluated agent actions with Solo/Team/Enterprise approval workflows.
- **Time-travel**: `!recall-at 3pm "project status"` shows what the agent would have found at 3pm yesterday.
- **Eval scoring**: Quantified memory health with CI gate integration. Catch memory rot before it matters.
- **Execution tracing**: Cryptographically signed audit trail for multi-step agent workflows.
- **Graceful degradation**: If rate limits are hit or the API is unavailable, the agent continues working — it never crashes.

## Tiers

| Tier | Price | Memories | Rollbacks | Features |
|------|-------|----------|-----------|----------|
| Free | $0 | 5,000 | 10/month | Memory, search, audit, rollback |
| Starter | $12/mo | 50,000 | 100/month | + Drafts, eval, conflict resolution |
| Pro | $39/mo | 500,000 | Unlimited | + Cortex, replay, knowledge graph, tracing |
| Enterprise | $199/mo | Unlimited | Unlimited | + Governed actions, team sharing, SSO |

## Configuration

Requires `NOVYX_API_KEY` environment variable. Get a free key at https://novyxlabs.com (5,000 memories, no credit card).

Options:
- `autoSave` (default: true) — Automatically save messages
- `autoRecall` (default: true) — Automatically recall context before each response
- `recallLimit` (default: 5) — Max memories to recall per query
