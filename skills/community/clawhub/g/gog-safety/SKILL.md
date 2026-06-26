---
name: gog-safety
description: Build and deploy safety-profiled gogcli binaries with compile-time command removal. Use when setting up gog for an AI agent with restricted permissions — choosing between L1 (draft only), L2 (collaborate), or L3 (standard write). Covers building from PR #366, deploying to remote hosts, and verifying blocked commands.
---

# gog Safety Profiles

Build and deploy `gog` binaries with compile-time command removal. Commands that are disabled don't exist in the binary — no runtime bypass possible.

## Quick Start

### 1. Choose a safety level

| Level | Use case | Can send email/chat? |
|-------|----------|---------------------|
| **L1** | Email triage, drafting, inbox organization | No |
| **L2** | L1 + commenting, RSVP, collaborative work | No |
| **L3** | Full write access, no dangerous admin ops | Yes |

For full details: `references/levels.md`

### 2. Build

```bash
# Build for current platform
./scripts/build-gog-safe.sh L1

# Cross-compile for Linux ARM64 (e.g., AWS Graviton)
./scripts/build-gog-safe.sh L1 --arch arm64 --os linux

# Custom output
./scripts/build-gog-safe.sh L2 --output /tmp/gog-l2
```

Requires: Go 1.22+, git. First run clones the PR #366 branch (~30s).

### 3. Deploy

```bash
# Deploy to a remote host via SSH
./scripts/deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe

# Deploy with verification (tests blocked + allowed commands)
./scripts/deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe --verify
```

The deploy script:
- Backs up the existing `gog` as `gog-backup`
- Installs the new binary
- Verifies version output
- Optionally tests that blocked commands are gone and allowed commands work

### 4. Rollback

```bash
ssh <host> 'sudo mv /usr/local/bin/gog-backup /usr/local/bin/gog'
```

## How It Works

Uses gogcli's compile-time safety profiles feature (PR #366 on `steipete/gogcli`). A YAML file specifies which commands are enabled (`true`) or removed (`false`). The build system generates Go source files with only the enabled commands, then compiles. The resulting binary's version is tagged with `-safe`.

## YAML Profiles

In `references/`:
- `l1-draft.yaml` — Draft & Organize
- `l2-collaborate.yaml` — Draft & Collaborate
- `l3-standard.yaml` — Full Write (No Admin)

Custom profiles: copy any YAML, edit the `true`/`false` flags, pass to `build-gog-safe.sh`.

## Verification

After deployment, verify with:
```bash
ssh <host> "gog --version"                     # Should show -safe suffix
ssh <host> "gog gmail send --help 2>&1"        # Should fail (L1/L2)
ssh <host> "gog gmail drafts create --help"    # Should work (all levels)
```

## Known Edge Cases

- **Filter forwarding:** `gmail settings filters create` is allowed at L1+ for inbox organization. A filter with a forward action could auto-forward email. Accepted risk for v1.
- **Drive sharing:** `drive share` is allowed at L1+ because sharing grants access without sending a message notification. The shared user sees it in "Shared with me" but doesn't get an email.
