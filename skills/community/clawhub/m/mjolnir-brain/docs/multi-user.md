# Multi-User Architecture — Mjolnir Brain v2.0

This document describes the multi-user isolation architecture introduced in Mjolnir Brain v2.0.

## Overview

Mjolnir Brain v2.0 introduces **user isolation** while maintaining **full backward compatibility** with v1.0 single-user deployments.

### Key Features

- ✅ **User isolation**: Each user has their own personal memory directory
- ✅ **Shared memory**: Team knowledge accessible to all users
- ✅ **v1.0 compatible**: Existing single-user setups work without changes
- ✅ **Zero configuration**: Default user works out of the box
- ✅ **Privacy by default**: Personal files have restrictive permissions (600)

## Directory Structure

```
templates/memory/
├── users/
│   ├── .gitkeep
│   ├── README.md
│   ├── default/              # Default user (v1.0 compatibility)
│   │   ├── MEMORY.md         # Personal long-term memory
│   │   └── YYYY-MM-DD.md     # Personal daily logs
│   ├── alice/                # User: alice
│   │   ├── MEMORY.md
│   │   └── YYYY-MM-DD.md
│   └── bob/                  # User: bob
│       ├── MEMORY.md
│       └── YYYY-MM-DD.md
└── shared/
    ├── .gitkeep
    ├── README.md
    ├── projects/             # Shared project context
    ├── decisions/            # Team decisions (all users)
    └── playbooks/            # Shared procedures
```

## User Resolution

The system determines the current user using this priority order:

### Priority 1: Environment Variable (Highest)

```bash
export MJOLNIR_USER=alice
```

This takes precedence over all other methods. Useful for:
- Script automation
- CI/CD pipelines
- Temporary user switching

### Priority 2: Current User File

```bash
~/.mjolnir_current_user
```

Contains the username of the last switched user. Persists across sessions.

**Set via script:**
```bash
scripts/user.sh switch alice
```

### Priority 3: Default (v1.0 Compatibility)

If neither environment variable nor file exists, the system uses `default` as the current user. This ensures v1.0 installations continue to work without any configuration.

## File Permissions

### Personal Memory (users/*)

| Type | Permission | Description |
|------|------------|-------------|
| Directory | 700 | Owner can read/write/execute |
| Files | 600 | Owner can read/write only |

**Rationale**: Personal memory may contain sensitive context. Only the owner should access it.

### Shared Memory (shared/*)

| Type | Permission | Description |
|------|------------|-------------|
| Directory | 755 | Owner rwx, others rx |
| Files | 644 | Owner rw, others r |

**Rationale**: Shared memory is team knowledge. Everyone should be able to read it.

## User Management

### Create a User

```bash
scripts/user.sh create alice
```

Creates:
- `memory/users/alice/` directory (mode 700)
- `.gitkeep` placeholder file (mode 600)

### List Users

```bash
scripts/user.sh list
```

Shows all users and marks the current user.

### Switch User

```bash
scripts/user.sh switch alice
```

Writes `alice` to `~/.mjolnir_current_user`. Affects all subsequent sessions.

### Check Current User

```bash
scripts/user.sh whoami
```

Shows:
- Current username
- Resolution source (env var / file / default)
- User directory path

### Delete User

```bash
scripts/user.sh delete alice
```

**Requires confirmation.** Deletes the user directory and all contained files.

**Warning**: Deleting `default` user breaks v1.0 compatibility.

## Migration from v1.0

Existing v1.0 installations can upgrade to v2.0 with zero data loss.

### Automatic Migration

```bash
scripts/migrate_to_v2.sh
```

This script:
1. Creates the new directory structure
2. Moves existing `memory/*.md` files to `memory/users/default/`
3. Creates `shared/` directories
4. Sets appropriate permissions
5. Creates README documentation

### Manual Migration

If you prefer manual control:

```bash
cd ~/.openclaw/workspace

# Create structure
mkdir -p memory/users/default memory/shared/{projects,decisions,playbooks}

# Move existing files
mv memory/*.md memory/users/default/

# Set permissions
chmod 700 memory/users/default
chmod 600 memory/users/default/*
chmod 755 memory/shared
chmod 755 memory/shared/*
find memory/shared -type f -exec chmod 644 {} \;
```

## Session Startup Flow

When a session starts, the agent:

1. **Resolves current user** (env → file → default)
2. **Reads SOUL.md** — global personality (shared)
3. **Reads USER.md** — global user profile (shared)
4. **Reads personal logs** — `memory/users/{user}/YYYY-MM-DD.md`
5. **Reads shared decisions** — `memory/shared/decisions/`
6. **Main session only**: Reads personal memory — `memory/users/{user}/MEMORY.md`

## Use Cases

### Single User (v1.0 Compatibility)

```bash
# No configuration needed
# Everything works under 'default' user
```

### Multi-User Team

```bash
# Alice sets up her environment
export MJOLNIR_USER=alice
scripts/user.sh create alice

# Bob sets up his environment
export MJOLNIR_USER=bob
scripts/user.sh create bob

# Both share team decisions
# Team decisions go to memory/shared/decisions/
```

### Shared Development Machine

```bash
# Each developer has their own user
scripts/user.sh create dev1
scripts/user.sh create dev2
scripts/user.sh create dev3

# Personal context stays isolated
# Project context goes to shared/projects/
```

### CI/CD Pipeline

```bash
# Use environment variable for automation
export MJOLNIR_USER=ci-bot
scripts/user.sh whoami  # Returns: ci-bot
```

## Security Considerations

### File System Permissions

- Personal files use mode 600 (owner-only)
- Shared files use mode 644 (world-readable)
- Ensure home directories have appropriate permissions

### Environment Variables

- `MJOLNIR_USER` can be set in shell config (~/.bashrc)
- Consider using `~/.mjolnir_current_user` for interactive sessions

### Multi-User Systems

On systems with multiple OS users:
- Each OS user has their own home directory
- `~/.mjolnir_current_user` is per-OS-user
- File permissions provide additional isolation

## Troubleshooting

### Wrong User Loaded

**Symptom**: Agent reads another user's memory

**Cause**: `MJOLNIR_USER` environment variable is set incorrectly

**Fix**:
```bash
unset MJOLNIR_USER
scripts/user.sh switch <correct_user>
```

### Permission Denied

**Symptom**: Cannot read/write user files

**Cause**: Incorrect file permissions

**Fix**:
```bash
scripts/set_permissions.sh
```

### User Directory Missing

**Symptom**: "User directory does not exist"

**Fix**:
```bash
scripts/user.sh create <username>
```

## API Reference

### user.sh Commands

| Command | Description |
|---------|-------------|
| `create <user>` | Create new user directory |
| `list` | List all users |
| `switch <user>` | Switch to user |
| `whoami` | Show current user |
| `delete <user>` | Delete user (with confirmation) |
| `help` | Show help |

### set_permissions.sh

Sets correct permissions for all memory files. Run after:
- Creating new users
- Migrating from v1.0
- Permission issues

### migrate_to_v2.sh

Migrates v1.0 installations to v2.0 structure. Preserves all data under `default` user.

## Version History

### v2.0 (Current)

- Multi-user isolation architecture
- User management scripts
- Migration tools
- Permission management
- Full v1.0 backward compatibility

### v1.0

- Single-user architecture
- Flat memory directory
- No user isolation

## See Also

- [INSTALL.md](../INSTALL.md) — Installation guide
- [security.md](security.md) — Security model
- [architecture.md](architecture.md) — System architecture
