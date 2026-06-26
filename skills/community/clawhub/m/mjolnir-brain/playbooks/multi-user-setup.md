# Multi-User Setup Playbook

**Purpose**: Set up Mjolnir Brain v2.0 for multi-user team environments.

**Prerequisites**:
- Mjolnir Brain v2.0 installed
- Bash shell access
- (Optional) Existing v1.0 installation to migrate

---

## Scenario 1: Fresh Multi-User Installation

### Step 1: Run Migration (Creates Structure)

```bash
cd /path/to/mjolnir-brain
scripts/migrate_to_v2.sh
```

This creates:
- `memory/users/` directory
- `memory/shared/` directory
- Default user structure

### Step 2: Create User Accounts

For each team member:

```bash
scripts/user.sh create alice
scripts/user.sh create bob
scripts/user.sh create charlie
```

### Step 3: Set Permissions

```bash
scripts/set_permissions.sh
```

### Step 4: Configure User Environment

Each user adds to their `~/.bashrc` or `~/.zshrc`:

```bash
export MJOLNIR_USER=<their_username>
```

Or use the switch command:

```bash
scripts/user.sh switch <their_username>
```

### Step 5: Verify Setup

```bash
# Check current user
scripts/user.sh whoami

# List all users
scripts/user.sh list

# Verify directory structure
ls -la templates/memory/users/
ls -la templates/memory/shared/
```

---

## Scenario 2: Migrate from v1.0

### Step 1: Backup (Recommended)

```bash
cd /path/to/mjolnir-brain
cp -r templates/memory memory_backup_$(date +%Y%m%d)
```

### Step 2: Run Migration

```bash
scripts/migrate_to_v2.sh
```

This automatically:
- Moves existing `memory/*.md` to `memory/users/default/`
- Creates `shared/` structure
- Preserves all data

### Step 3: Verify Migration

```bash
# Check default user has old files
ls -la templates/memory/users/default/

# Test that everything still works
scripts/user.sh whoami  # Should show 'default'
```

### Step 4: (Optional) Create Additional Users

```bash
scripts/user.sh create alice
scripts/user.sh switch alice
```

---

## Scenario 3: Add New Team Member

### Step 1: Create User

```bash
scripts/user.sh create <new_username>
```

### Step 2: Set Permissions

```bash
scripts/set_permissions.sh
```

### Step 3: Configure User's Environment

New user runs:

```bash
scripts/user.sh switch <their_username>
```

Or adds to their shell config:

```bash
echo 'export MJOLNIR_USER=<their_username>' >> ~/.bashrc
source ~/.bashrc
```

---

## Scenario 4: Shared Project Setup

### Step 1: Create Project Directory

```bash
mkdir -p templates/memory/shared/projects/<project_name>
```

### Step 2: Add Project Context

Create `templates/memory/shared/projects/<project_name>/CONTEXT.md`:

```markdown
# Project: <Project Name>

## Overview
Brief description of the project.

## Key Decisions
- Decision 1
- Decision 2

## Related Files
- Link to relevant files
```

### Step 3: Set Permissions

```bash
chmod 755 templates/memory/shared/projects/<project_name>
chmod 644 templates/memory/shared/projects/<project_name>/*
```

---

## Verification Checklist

After setup, verify:

- [ ] `scripts/user.sh list` shows all users
- [ ] `scripts/user.sh whoami` returns correct user
- [ ] User directories exist with correct permissions (700)
- [ ] Shared directories exist with correct permissions (755)
- [ ] Personal files have permission 600
- [ ] Shared files have permission 644
- [ ] Agent reads correct user's memory files
- [ ] Shared decisions are visible to all users

---

## Troubleshooting

### Problem: Wrong User's Memory Loaded

**Check**:
```bash
echo $MJOLNIR_USER
cat ~/.mjolnir_current_user
scripts/user.sh whoami
```

**Fix**:
```bash
unset MJOLNIR_USER  # Clear env var if wrong
scripts/user.sh switch <correct_user>
```

### Problem: Permission Denied

**Fix**:
```bash
scripts/set_permissions.sh
```

### Problem: User Directory Missing

**Fix**:
```bash
scripts/user.sh create <username>
```

### Problem: Can't See Shared Files

**Check permissions**:
```bash
ls -la templates/memory/shared/
```

**Fix**:
```bash
find templates/memory/shared -type f -exec chmod 644 {} \;
find templates/memory/shared -type d -exec chmod 755 {} \;
```

---

## Next Steps

After setup:
1. Read `docs/multi-user.md` for detailed architecture
2. Configure team workflows for shared memory
3. Set up automated backups for both personal and shared memory
4. Consider setting up cron jobs for maintenance

---

## Related Documents

- [docs/multi-user.md](../docs/multi-user.md) — Architecture details
- [INSTALL.md](../INSTALL.md) — Installation guide
- [README.md](../README.md) — Project overview
