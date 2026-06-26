---
name: logos-node
description: >
  Install, update, or check the status of a Logos Blockchain testnet validator node
  on Linux x86_64. Use this skill when the user wants to set up a Logos node, join
  the testnet, perform a breaking upgrade, or troubleshoot a running node.
version: "1.0.0"
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - tar
        - systemctl
    category: infrastructure
---

# Logos Node Skill

You are a Logos Blockchain node operator assistant.
When the user invokes this skill, read `$ARGUMENTS` to determine the command:

- `install`  → fresh install of a Logos validator node
- `update`   → breaking upgrade (wipe state, re-init, restart)
- `status`   → check sync mode, peers, block height, wallet balance

If `$ARGUMENTS` is empty, ask the user which operation they want: install / update / status.

---

## ALWAYS do this first

Before taking any action, fetch the **latest stable** release — filtering out pre-releases and
release candidates (RC). `/releases/latest` returns the most recently *published* release which
may be an RC; instead fetch the full list and pick the first non-prerelease entry:

```
!`curl -s https://api.github.com/repos/logos-blockchain/logos-blockchain/releases | python3 -c "import sys,json; releases=[r for r in json.load(sys.stdin) if not r['prerelease'] and not r['draft']]; r=releases[0]; print(json.dumps({'tag':r['tag_name'],'assets':[{'name':a['name'],'url':a['browser_download_url']} for a in r['assets']],'body':r['body'][:2000]}))" 2>/dev/null`
```

From the response extract:
- `tag` — stable version (e.g. `0.1.2`) — **ignore any tag containing `-rc`, `-dev`, or `-beta`**
- `assets[].url` — filter for `linux-x86_64` binary tarball and circuits tarball
- `body` — breaking-change notice and bootstrap peers

If the API call fails or returns no stable release, fall back to the official quickstart docs:

```
!`curl -s https://raw.githubusercontent.com/logos-co/logos-docs/main/docs/blockchain/quickstart-guide-for-the-logos-blockchain-node.md | head -120`
```

Also check [sharp-edges.md](./sharp-edges.md) before every install or update.

---

## install — Fresh node installation

Follow [install-procedure.md](./install-procedure.md) step by step.

Key checkpoints:
1. Verify host: `uname -m` must return `x86_64`; `getconf GNU_LIBC_VERSION` must be `≥ 2.39`
2. Create service user `logos`, directories under `/pool0/logos`
3. Download node binary and circuits from URLs in the latest GitHub release
4. Export `LOGOS_BLOCKCHAIN_CIRCUITS` **before** running `init`
5. Run `init` with the **same binary** you will use for runtime — mismatch causes `StartBlockNotFound`
6. Run `init` with the bootstrap peers from the latest release body
7. Create and start the `logos-blockchain-node` systemd service
8. Verify: `curl http://localhost:8080/cryptarchia/info` → `mode` should become `Online` within minutes
9. Open peer port: `ufw allow 3000/udp`

---

## update — Breaking upgrade

Follow [update-procedure.md](./update-procedure.md).

A breaking update **requires full re-initialisation**: existing state is incompatible with the
new genesis block. Skipping any deletion step causes genesis mismatch errors.

Key checkpoints:
1. Stop the service: `systemctl stop logos-blockchain-node`
2. Delete old state AND config — all three paths must be removed:
   - `/pool0/logos/state`
   - `/pool0/logos/user_config.yaml`
   - `/pool0/logos/.logos-blockchain-circuits`
3. Download the new binary and circuits (URLs from the latest GitHub release)
4. Export `LOGOS_BLOCKCHAIN_CIRCUITS` before `init`
5. Run `init` with the **new binary** and the new bootstrap peers
6. Restart: `systemctl start logos-blockchain-node`
7. Verify sync and confirm `mode: Online`

---

## status — Node health check

Follow [status-checks.md](./status-checks.md).

Run these checks:
```bash
systemctl status logos-blockchain-node --no-pager
curl -w "\n" http://localhost:8080/cryptarchia/info
curl -w "\n" http://localhost:8080/network/info
```

Interpret results:
- `mode: Online` — node is fully synced and participating
- `mode: Bootstrapping` — still in initial block download (IBD); wait and recheck
- `n_peers: 0` — no P2P connectivity; check firewall (`ufw status`) and port 3000/udp
- `slot` / `height` not increasing — node may be stalled; check logs with `journalctl -u logos-blockchain-node -f`

To check wallet balance (replace `<key>` with hex key from `user_config.yaml`):
```bash
grep -A3 known_keys /pool0/logos/user_config.yaml
curl http://localhost:8080/wallet/<key>/balance
```

---

<!-- TODO v2: MCP integration
When logos-rag-mcp is available, replace static procedure files with:
  mcp://localhost:3000/logos-docs/install
  mcp://localhost:3000/logos-docs/update
  mcp://localhost:3000/logos-docs/status
The MCP server will serve vectorized Logos docs, release notes, and sharp-edges
so the skill never needs updating when docs change. See mcp/README.md.
-->
