# Orca Command Reference Cheatsheet

Quick CLI commands for Orca IDE and runtime management.

## Direct Headless CLI Execution Pattern
When running on headless servers or when `~/.local/bin/orca` fails with sandbox/FUSE mount errors:
```bash
# 1. Preferred Static Path (when unpacked under /opt/orca):
su - orca -c "node /opt/orca/squashfs-root/resources/app.asar.unpacked/out/cli/index.js <command>"

# Example: Register repository
su - orca -c "node /opt/orca/squashfs-root/resources/app.asar.unpacked/out/cli/index.js repo add --path /home/orca/orca/<repo-name> --json"

# 2. Dynamic Mount Path (AppImage mount fallback):
MOUNT_DIR=$(ls -d /tmp/.mount_orca-*/ 2>/dev/null | head -n1)
su - orca -c "ELECTRON_RUN_AS_NODE=1 ${MOUNT_DIR}orca-ide ${MOUNT_DIR}resources/app.asar.unpacked/out/cli/index.js <command>"

# Examples:
su - orca -c "ELECTRON_RUN_AS_NODE=1 ${MOUNT_DIR}orca-ide ${MOUNT_DIR}resources/app.asar.unpacked/out/cli/index.js status"
su - orca -c "ELECTRON_RUN_AS_NODE=1 ${MOUNT_DIR}orca-ide ${MOUNT_DIR}resources/app.asar.unpacked/out/cli/index.js project list"
su - orca -c "ELECTRON_RUN_AS_NODE=1 ${MOUNT_DIR}orca-ide ${MOUNT_DIR}resources/app.asar.unpacked/out/cli/index.js worktree list"
su - orca -c "ELECTRON_RUN_AS_NODE=1 ${MOUNT_DIR}orca-ide ${MOUNT_DIR}resources/app.asar.unpacked/out/cli/index.js terminal list"
```

## System & Diagnostics
```bash
orca status                      # Check runtime readiness, PID and graph state
orca diagnostics memory          # Memory usage breakdown
systemctl status orca-serve      # Service status
systemctl restart orca-serve     # Service restart
```

## Repositories & Worktrees
```bash
orca repo list                   # List registered repos
orca project list                # List projects
orca repo add <path>             # Register directory as repo
orca project setup-clone <url>   # Clone repo
orca worktree list               # List worktrees
orca worktree ps                 # Compact status
orca worktree create <branch>    # Create worktree
orca worktree rm <id>            # Remove worktree
```

## Orchestration & Workers
```bash
orca orchestration run-list      # List orchestration runs
orca orchestration run-create    # Create new run
orca orchestration task-list     # List tasks
orca orchestration task-create   # Create task
orca orchestration task-update   # Update task status
orca orchestration worker-list   # List active workers
orca orchestration worker-start  # Start worker for task
orca orchestration worker-read   # Read worker logs
orca orchestration worker-release # Release worker terminal
orca orchestration gate-list     # List decision gates
orca orchestration gate-resolve  # Resolve decision gate
orca orchestration inbox         # Inter-agent inbox
orca orchestration reply         # Reply to thread
```

## Terminals & Subagent Control
```bash
orca terminal list                                               # List live terminals, IDs and visual layout
orca terminal create                                             # Create terminal in current worktree
orca terminal read --terminal <terminal_id> --screen            # Read rendered screen frame (essential for TUI agents like agy/claude)
orca terminal read --terminal <terminal_id> --cursor <c>        # Read stream delta since cursor
orca terminal send --terminal <terminal_id> --text "<cmd>" --enter # Send prompt/command and press Enter
orca terminal send --terminal <terminal_id> --interrupt         # Send Ctrl+C / interrupt signal
orca terminal switch --terminal <terminal_id>                    # Focus terminal tab in UI
orca terminal close --terminal <terminal_id>                     # Close terminal session
```
