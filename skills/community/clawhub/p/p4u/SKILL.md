---
name: p4u
description: >
  Perforce / Helix Core (p4) power-user CLI. Use for any p4 task: show or
  inspect changelists (CLs), shelve/unshelve/reshelve, switch between CLs,
  delete CLs or clients/workspaces, revert files, find untracked files, blame
  a line (annotate), sync, or manage depots. Prefer over raw p4 commands.
allowed-tools:
  - Bash(p4u *)
  - Bash(which *)
  - Bash(uname *)
---

# p4u

Single Go binary, zero external dependencies. Wraps common `p4` workflows with
colour output, JSON mode, and `--non-interactive` for automation.

**Repo:** https://github.com/m9rco/p4u-skill

## Binary status

!`which p4u 2>/dev/null && echo "✓ $(p4u --version 2>/dev/null || which p4u)" || echo "✗ p4u not found — install required (see Prerequisites below)"`

## Prerequisites

`p4u` and `p4` must be installed before using this skill.

### Install p4u

Download the pre-built binary for your platform from the [releases page](https://github.com/m9rco/p4u-skill/releases):

**macOS / Linux:**
```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]') && ARCH=$(uname -m)
[[ "$ARCH" == "x86_64" ]] && ARCH=amd64 || ARCH=arm64
BASE="https://github.com/m9rco/p4u-skill/releases/download/nightly"
curl -fsSL "${BASE}/p4u-${OS}-${ARCH}" -o /tmp/p4u
curl -fsSL "${BASE}/checksums.txt" -o /tmp/p4u-checksums.txt
# Verify integrity before installing (works on both macOS and Linux)
EXPECTED=$(grep "p4u-${OS}-${ARCH}" /tmp/p4u-checksums.txt | awk '{print $1}')
ACTUAL=$(command -v sha256sum >/dev/null 2>&1 && sha256sum /tmp/p4u | awk '{print $1}' || shasum -a 256 /tmp/p4u | awk '{print $1}')
[ "$EXPECTED" = "$ACTUAL" ] || { echo "Checksum mismatch — aborting"; rm -f /tmp/p4u; exit 1; }
chmod +x /tmp/p4u && sudo mv /tmp/p4u /usr/local/bin/p4u
```

**Windows** (PowerShell):
```powershell
Invoke-WebRequest -Uri "https://github.com/m9rco/p4u-skill/releases/download/nightly/p4u-windows-amd64.exe" `
  -OutFile "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\p4u.exe"
```

### Install p4 CLI

**macOS** (Homebrew):
```bash
brew install p4
```

**Linux:**
```bash
curl -fsSL "https://cdist2.perforce.com/perforce/r24.2/bin.linux26x86_64/p4" \
  -o /tmp/p4 && chmod +x /tmp/p4 && sudo mv /tmp/p4 /usr/local/bin/p4
```

**Windows:**
```powershell
Invoke-WebRequest -Uri "https://cdist2.perforce.com/perforce/r24.2/bin.ntx64/p4.exe" `
  -OutFile "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\p4.exe"
```

Or use the official instructions at: https://www.perforce.com/downloads/helix-command-line-client-p4

Then log in: `p4 login`

## Rules

0. **Check first**: run `which p4u` to verify the binary is installed. If missing,
   inform the user and show the install command above — do not execute install
   commands autonomously.
1. **Always** pass `--non-interactive` — prevents hanging on prompts.
2. **Destructive operations** (`delete-client`, `delete-cl`, `revert-all`, any `-f`/`--force`
   flag) **require explicit user confirmation** before running. Show the command and
   ask the user to confirm — never execute destructive commands autonomously.
3. Pass `--json` when output needs to be parsed programmatically; omit it for
   human-readable display.
4. Changelist numbers are plain integers, e.g. `12345`.
5. `p4u` auto-reads current user and client from `p4 info`.
6. **Error handling**: on non-zero exit show the raw output as-is; do not silently
   retry with different flags.

## Workflow Decision Tree

Match the user's intent to the right command — act immediately, no clarifying
questions needed for these standard cases:

| User says…                                      | Run this                                         |
|-------------------------------------------------|--------------------------------------------------|
| "show my work", "what CLs do I have"            | `p4u show --non-interactive`                     |
| "switch to CL 12345", "load changelist 12345"   | `p4u switch 12345 --non-interactive`             |
| "who changed line N of //depot/…"               | `p4u annotate //depot/… N --non-interactive`     |
| "inspect CL 12345", "what's in changelist …"    | `p4u show-cl 12345 --non-interactive`            |
| "delete this client", "remove my workspace"     | confirm first, then `p4u delete-client --non-interactive` |
| "find untracked files", "what's not in p4"      | `p4u untracked --non-interactive`                |
| "revert everything", "undo all changes"         | confirm first, then `p4u revert-all --non-interactive`    |
| "reshelve CL 12345"                             | `p4u reshelve 12345 --non-interactive`           |
| "unshelve CL 12345"                             | `p4u unshelve 12345 --non-interactive`           |
| "delete CL 12345"                               | confirm first, then `p4u delete-cl 12345 --non-interactive` |

---

## Workflow Examples

### Show my open work

```bash
p4u show --non-interactive          # pending + shelved
p4u show -p --non-interactive       # pending only
p4u show -s --non-interactive       # shelved only
p4u show --json --non-interactive   # for further processing
```

### Switch to a different changelist

Shelves current work first, then unshelves the target:

```bash
p4u switch 12345 --non-interactive
p4u switch 12345 -s -m --non-interactive   # also sync + auto-resolve
p4u switch 12345 -k --non-interactive      # keep existing shelve
```

### Who changed this line?

```bash
p4u annotate //depot/main/src/foo.cpp 42 --non-interactive
p4u annotate -v //depot/main/src/foo.cpp 42 --non-interactive  # verbose
p4u annotate --json //depot/main/src/foo.cpp 42 --non-interactive
```

### Inspect a changelist

```bash
p4u show-cl 12345 --non-interactive
p4u show-cl 12345 -b --non-interactive     # brief: no file list
p4u show-cl 12345 --json --non-interactive
```

### Clean up a stale client

```bash
p4u delete-client --non-interactive        # uses current client
p4u delete-client -c myclient --non-interactive
p4u delete-client -f --non-interactive     # skip confirmation
p4u delete-client -n --non-interactive     # keep local files
```

### Find untracked files

```bash
p4u untracked --non-interactive
p4u untracked ./src ./assets --non-interactive
p4u untracked -d 3 --non-interactive       # max depth 3
p4u untracked --json --non-interactive
```

---

## Full Command Reference

### Show client status

```bash
p4u show --non-interactive              # pending + shelved changelists
p4u show -s --non-interactive           # shelved only
p4u show -p --non-interactive           # pending only
p4u show --json --non-interactive       # JSON output
p4u show -u <user> --non-interactive    # filter by user
p4u show -c <client> --non-interactive  # filter by client
p4u show -m 10 --non-interactive        # limit to 10 results
```

### Reshelve / unshelve

```bash
p4u reshelve <CL> --non-interactive
p4u unshelve <CL> --non-interactive
```

### Revert all opened files

```bash
p4u revert-all --non-interactive
```

### Delete a changelist

```bash
p4u delete-cl <CL> --non-interactive
p4u delete-cl -f <CL> --non-interactive   # force, no confirmation
p4u delete-cl <CL1> <CL2> --non-interactive
```

---

## Global flags

| Flag                | Short | Description                     |
|---------------------|-------|---------------------------------|
| `--non-interactive` |       | Disable all interactive prompts |
| `--json`            |       | JSON output                     |
| `--no-color`        |       | Disable colour                  |
| `--force-color`     |       | Force colour when piping        |
