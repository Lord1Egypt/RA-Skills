# User Memory Isolation

This directory contains per-user memory files for multi-user Mjolnir Brain deployments.

## Structure

```
users/
├── default/           # Default user (v1.0 compatibility)
│   ├── MEMORY.md      # Long-term personal memory
│   └── YYYY-MM-DD.md  # Daily session logs
├── alice/             # User: alice
│   ├── MEMORY.md
│   └── YYYY-MM-DD.md
└── bob/               # User: bob
    ├── MEMORY.md
    └── YYYY-MM-DD.md
```

## How User Resolution Works

The system determines the current user using this priority:

1. **Environment variable** `MJOLNIR_USER` (highest priority)
2. **File** `~/.mjolnir_current_user` (session persistence)
3. **Default**: `default` (v1.0 backward compatibility)

## Privacy & Permissions

- **Personal memory** (`users/{user}/`): Mode 600 — only readable by the user
- **Shared memory** (`shared/`): Mode 644 — readable by all users

## Usage

```bash
# List all users
scripts/user.sh list

# Create a new user
scripts/user.sh create alice

# Switch to a user
scripts/user.sh switch alice

# Check current user
scripts/user.sh whoami
```

## v1.0 Compatibility

Single-user deployments don't need to configure anything. All existing memory files work as before under the `default` user.

Run `scripts/migrate_to_v2.sh` to upgrade existing v1.0 installations.
