# my_soul_upgrade_skill

## Purpose
Manage and synchronize Soul definitions across the agent system using a two-layer template architecture.

## Architecture
- **Global Layer**: `/home/admin/.openclaw/soul/SOUL.md` (Common principles, constraints, formatting)
- **Agent Layer**: `/home/admin/.openclaw/workspaces/workspace-<agent_id>/template.md` (Personalized role, specific capabilities)
- **Output**: Built SOUL.md → `/home/admin/.openclaw/workspaces/workspace-<agent_id>/SOUL.md`

New layout aligns with OpenClaw's per-agent workspace pattern.

## Workflow

### 1. Update Global Soul (Applies to all agents)
1.  **Edit**: Modify `/home/admin/.openclaw/soul/SOUL.md`.
2.  **Sync**: Execute `python3 ~/.openclaw/scripts/build_all_souls.py` to regenerate all agent SOUL files.

### 2. Update Agent-Specific Soul
1.  **Edit**: Modify `/home/admin/.openclaw/workspaces/workspace-<agent_id>/template.md`.
2.  **Sync**: Execute `python3 ~/.openclaw/scripts/build_all_souls.py` to rebuild the specific agent's SOUL.

---
_Note: Always run `build_all_souls.py` after any manual modification to maintain sync._
