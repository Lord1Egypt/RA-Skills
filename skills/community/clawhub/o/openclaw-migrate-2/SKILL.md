---
name: agent-migrate
description: Cross-platform agent migration and deployment. Use when: (1) migrating OpenClaw agent to new servers, (2) backing up and restoring agent state, (3) deploying agent configurations across environments, (4) syncing workspace between development and production. NOT for: general file backup, non-agent data migration.
---

# Agent Migration

Migrate OpenClaw agents across servers and platforms while preserving identity, memory, and configuration.

## When to Use

✅ **USE this skill when:**

- Moving agent from local machine to remote server
- Cloning agent configuration to multiple environments
- Backing up complete agent state for disaster recovery
- Syncing workspace changes between dev/prod
- Upgrading OpenClaw with full rollback capability

❌ **DON'T use when:**

- Simple file copy operations → use `cp`/`rsync` directly
- Database migrations → use database-specific tools
- Non-OpenClaw application deployment

## Core Concepts

### Agent State Components

```
Agent State = Identity + Memory + Config + Skills + Extensions
├── workspace/           # Core identity files
│   ├── IDENTITY.md      # Who the agent is
│   ├── USER.md          # Who they serve
│   ├── SOUL.md          # Personality
│   ├── MEMORY.md        # Long-term memory
│   ├── AGENTS.md        # Operational rules
│   ├── TOOLS.md         # Environment notes
│   └── memory/          # Daily logs
├── .openclaw/
│   ├── openclaw.json    # Gateway config
│   ├── agents/          # Session data
│   └── extensions/      # Custom plugins
└── skills/              # Custom skills (if any)
```

### Migration Workflows

#### 1. Export (Source Machine)

```bash
# Full agent export
./scripts/export-agent.sh [export-name]

# Creates:
# /tmp/agent-export-[name]/
#   ├── manifest.json      # Export metadata
#   ├── workspace.tar.gz   # Core files
#   ├── config.tar.gz      # OpenClaw config
#   └── restore.sh         # Self-contained restore
```

#### 2. Transfer

```bash
# Via SSH
scp -r /tmp/agent-export-[name] user@new-server:/tmp/

# Via GitHub (recommended for versioned deployments)
# Push to repo, clone on target
```

#### 3. Import (Target Machine)

```bash
# Run self-contained restore
cd /tmp/agent-export-[name] && ./restore.sh

# Or manual:
./scripts/import-agent.sh /tmp/agent-export-[name]
```

## Scripts

### Export Agent

```bash
scripts/export-agent.sh [name] [--full]
```

Options:
- `name` - Export identifier (default: timestamp)
- `--full` - Include session history and logs

### Import Agent

```bash
scripts/import-agent.sh <export-path> [--merge|--replace]
```

Options:
- `--merge` - Merge with existing agent (default)
- `--replace` - Wipe existing, clean install

### Sync to GitHub

```bash
scripts/sync-github.sh <repo-url> [--push|--pull]
```

Syncs agent state to GitHub for versioned deployment.

## Platform-Specific Notes

### Linux → Linux
Direct transfer, no conversion needed.

### macOS → Linux
- Check for macOS-specific paths in scripts
- Update file watchers if used

### Windows WSL → Native Linux
- Line endings auto-handled
- Verify executable permissions

### Docker Deployment

See `references/docker-deploy.md` for containerized deployment.

## Security Checklist

- [ ] Sanitize `openclaw.json` (remove sensitive tokens before export)
- [ ] Verify target machine permissions
- [ ] Rotate any exposed credentials post-migration
- [ ] Test agent functionality before production cutover

## Rollback

Exports are immutable snapshots. To rollback:

```bash
# Re-import previous export
./scripts/import-agent.sh /path/to/previous-export --replace
```
