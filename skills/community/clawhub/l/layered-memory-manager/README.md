# Layered Memory Manager

A professional multi-tier memory management system designed for persistent AI agents. It implements a cache-coherent architecture with automated promotion and demotion logic.

## Key Features

- **Multi-tier Cache (L1/L2)**:
  - **L1 (Hot Cache)**: Inline metadata in `MEMORY.md` for fast, zero-latency context retrieval.
  - **L2 (Cold Storage)**: Detailed markdown files in `memory/*.md` for full context and history.
- **Automated Hygiene**:
  - **Promotion**: Frequently accessed L2 entries are automatically promoted to L1 after 3 unique sessions.
  - **Demotion**: Stale L1 entries are demoted back to L2 after 3 sessions of inactivity to keep context lean.
- **Strong Consistency**: Enforces a "Write-to-L2-then-Sync-L1" order to ensure the source of truth is always reliable.
## Security & Data Integrity

- **Grep Binary**: This skill recommends a pre-installed `grep` binary. It is strictly used for **read-only scanning** of `memory/*.md` files during the "Secondary: Layer Awareness" phase. This is safer, faster, and more token-efficient than making the AI read hundreds of small files.
- **Data Pruning Logic**:
  - **Promotion**: When an entry is promoted to L1, its record in `accessLog` is removed because it is now independently tracked in `L1accessLog`. This prevents redundant counting.
  - **Archiving**: Inactive entries (30+ days) are **moved** to `memory/archive/`, not deleted. This maintains a lean core context for the agent and prevents historical noise from interfering with current decisions.
- **Transparency**: All operations are logged in `hygiene.json`, and users can undo any archive operation using the `[[restore]]` command.

## Usage

Embed the following tags in your messages to manually trigger memory operations:

- `[[pin:<layer>:<slug>]]`: Permanently keep an entry in L1.
- `[[promote:<layer>:<slug>]]`: Force-promote an L2 entry to L1.
- `[[forget:<layer>:<slug>]]`: Demote a L1 entry immediately.
- `[[restore:<layer>:<slug>]]`: Restore an archived entry back to active storage.
- `[[memory_health]]`: Get a snapshot of your memory system status.

## Design Philosophy

This skill follows the "Layered Intelligence" principle—separating high-frequency operational facts (L1) from deep historical context (L2) to maximize agent performance while minimizing token overhead.
