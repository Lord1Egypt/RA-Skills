---
name: ipfs-pin
description: >
  IPFS content persistence for OpenClaw via a local kubo node. Adds files
  to IPFS, pins them so they stay robust while active, and tracks a
  per-file TTL in a ledger. `decay` unpins entries not referenced within
  their TTL and garbage-collects the repo; a systemd user timer runs it
  daily so unused content decays naturally without manual cleanup.
  Reports only CIDs and status the ipfs CLI actually returned.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🌐", "requires": {"bins": ["ipfs"], "files": [], "config": []}}}
---

# ipfs-pin skill

Content is added to the local kubo node (API on 127.0.0.1:5001) and
pinned. Content-addressing means every file gets a stable CID that works
across the IPFS network; pinned entries are also served from local disk
so they survive offline. The ledger at `~/.openclaw/ipfs-pin/ledger.json`
tracks each CID with a TTL; the `decay` sweep (run daily by an `ipfs-pin-decay.timer`
systemd user unit) unpins entries past TTL and runs `ipfs repo gc`, so
unused content decays rather than accumulating forever.

**Only cite CIDs or status the `ipfs` CLI returned** — never invent one.
If the daemon is down, say so (`status` reports it); don't guess.

## Setup (done once)

- kubo binary: `~/bin/ipfs` (kubo 0.43.1, verified via upstream .sha512)
- daemon: `systemctl --user status ipfs` (unit in `~/.config/systemd/user/ipfs.service`)
- decay sweep: `systemctl --user status ipfs-pin-decay.timer`

## Command reference

Run via bash: `~/.openclaw/plugin-skills/ipfs-pin/ipfs_pin.py <cmd> ...`.
Add `--json` right after the program name for structured output.

| Command | Purpose |
|---|---|
| `add <path> [--name N] [--ttl H]` | Add+pin a file; TTL refreshes on re-add. Default TTL 72h (`config --default-ttl-hours` to change). |
| `ls` | Show tracked CIDs with hours remaining |
| `touch <cid>` | Refresh `last_referenced` on a CID you're still using |
| `rm <cid> [--no-gc]` | Unpin immediately and drop from ledger |
| `decay [--dry-run] [--quiet]` | Unpin everything regretted past TTL + `repo gc` |
| `get <cid> [-o PATH]` | Retrieve by CID from local node (cat to stdout or write file) |
| `status` | Daemon up? repo size, pin count, tracked vs untracked |
| `config [--default-ttl-hours H]` | Show or set default TTL |

## Decay semantics

- A file added today with default TTL decays ~3 days from last reference.
- Re-`add`ing the same content (identical bytes = same CID) refreshes its
  TTL instead of duplicating.
- Explicitly `touch` a CID during work to keep it alive without re-adding.
- `decay --dry-run` previews what would be unpinned without touching anything.
- Manual `ipfs add` (outside this skill) still pins on the node — `status`
  flags these as "untracked" so they don't silently miss the sweep.

## One-command decay check

```bash
~/.openclaw/plugin-skills/ipfs-pin/ipfs_pin.py decay --dry-run
```
