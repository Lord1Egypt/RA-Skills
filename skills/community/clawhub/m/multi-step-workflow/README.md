# Multi-Step Workflow (High-Trust SOP)

Lightweight task tracking with **Machine-Gated Planning**, **Autonomous Execution**, and **User-Opt-In Review**.

## Security & Compliance (ClawHub Audit v4.4.0)

> [!IMPORTANT]
> **Audit-Hardened Private Sandbox (Owner-Only Access)**
> To resolve security concerns regarding shared `/tmp` directories, this version implements **strict POSIX permission locking**:
> - **Private Directory (0700)**: The project-specific temp directory is created with `0700` permissions (read/write/cd for owner only). Other users on the system cannot list or access your task data.
> - **Private Files (0600)**: All JSON state files (approvals, snapshots, tasks) are created with `0600` permissions (read/write for owner only).
>
> **Configurable Snapshot Feature (Default: OFF)**
> To satisfy high-assurance privacy requirements, the **Context Snapshot** feature is now optional.
> - **Default useSnapshots**: `false`
> - **High-Fidelity Snapshots**: When enabled, snapshots are saved in raw form to ensure perfect task recovery. Only enable if you trust the local system's temporary storage.

### 💾 Private Workspace (In Temp)
- `approvals.json` (0600): Machine-gated approval records.
- `context-snapshot.json` (0600): Native fidelity task findings.
- `tasks/*.json` (0600): Granular step tracking.

## Adaptive Workflow Logic

1. **Simple Path (< 3 steps)**: Direct execution.
2. **Standard Path (>= 3 steps)**:
   - **Step 1: Planning Mode**: Agent drafts a plan. **MUST WAIT for approval**.
   - **Step 2: Gating**: Agent runs `node scripts/approve.js`.
   - **Step 3: Execution**: The Agent completes the task autonomously.
   - **Step 4: Anti-Amnesia**: If `useSnapshots` is `true`, snapshots are saved to the private sandbox.

## Configuration

**Initialize Configuration (required for first use)**:
`openclaw config set skills.entries.multi-step-workflow.config '{"useSubAgents": false, "maxSubAgents": 3, "useSnapshots": false}' --strict-json`

**To enable sub-agents (Parallelism)**:
`openclaw config set skills.entries.multi-step-workflow.config.useSubAgents true --strict-json`

**To enable task snapshots (Persistence)**:
`openclaw config set skills.entries.multi-step-workflow.config.useSnapshots true --strict-json`

**To see current configuration**:
`openclaw config get skills.entries.multi-step-workflow.config`

## Core Scripts (Auditable)

- `path-resolver.js`: Permission-hardened temp isolation.
- `task-tracker.js`: Owner-only progress tracking.
- `approve.js`: Machine-visible gate signal.
- `context-snapshot.js`: High-fidelity state persistence.

## Repository & Issues

This skill is part of the [Agent-Skills](https://github.com/chyern/Agent-Skills) collection.
Feel free to download, star, or submit issues!

## License

MIT
