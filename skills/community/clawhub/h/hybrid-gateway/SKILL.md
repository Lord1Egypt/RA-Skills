---
name: hybrid-gateway
description: Set up and troubleshoot a secure hybrid OpenClaw architecture where the Gateway runs on a VPS and a Mac or other local machine is a paired node. Covers Tailscale node pairing (single-use join links), exact-request approval and reapproval, remote node exec with least-privilege allowlists, node reconnect, and SSH as a separate fallback. Use when connecting a local node to a remote Gateway, debugging node connectivity or "reapproval pending", or planning a VPS + local hardware split.
license: MIT
---

# Hybrid Gateway: VPS + Local Node

The Gateway runs on an always-on VPS and owns messaging, agents, and models. A local machine (Mac Mini, desktop, Pi) is a paired **node** for what the VPS lacks: GPU or local models, a real browser with a residential IP, macOS tools, local files. A node is a peripheral.

## Safety contract

- **Route:** Gateway stays on loopback; Tailscale Serve (or another stable HTTPS reverse proxy with WebSocket upgrade) gives it a `wss://` URL on the tailnet. Never expose port 18789 to the public internet, never use Tailscale Funnel for it. `gateway.bind=lan`, `0.0.0.0`, and plaintext `ws://` are not defaults.
- **Pairing:** a single-use Node-host join link from the Control UI or `openclaw devices join-code`. Never paste Gateway tokens, setup codes, or keys into chat, logs, or shell history.
- **Approval:** inspect the exact request (name, device id, IP, requested commands) and approve that request id only. A capability expansion is a new approval and may stay pending.
- **Exec:** named absolute-path commands plus approval gates. No shell (`sh`, `bash`, `zsh`) in any allowlist.
- **SSH:** optional, separate, least-privilege. It is not a substitute for pairing and is set up in the companion `remote-node-ssh` skill.

Each step ends with a **Done when** check. Stop at a failed check.

## Prerequisites

Upgrade the Gateway first; a node may run the same version or the previous supported release (N-1) until it is upgraded. Both machines are on one tailnet (`tailscale status` shows both) and the VPS Gateway is running (`openclaw gateway status`).

## Step 1: Keep the Gateway private, publish it with Tailscale Serve

On the VPS:

```bash
openclaw config get gateway.bind          # keep "loopback"
openclaw config get gateway.auth.mode     # "token" or "password"; never "none"
tailscale serve --bg --https=443 http://127.0.0.1:18789
tailscale serve status                    # https://<vps>.<tailnet>.ts.net (tailnet only)
```

Serve runs on the same host and forwards from 127.0.0.1, so for this exact setup `gateway.trustedProxies` should contain only `127.0.0.1`. If you already run another legitimate reverse proxy, keep its address too; never widen the list to the Tailscale range `100.0.0.0/8`, or every node counts as a proxy and is rejected with `403 Proxy client attribution is required`.

A direct tailnet or LAN bind without Serve is possible but outside this skill: it needs token or password auth, a firewall limiting 18789 to private addresses, no port-forward or Funnel, and a TLS route for pairing. If you cannot prove that boundary, use Serve.

**Done when:** `openclaw gateway status` shows `bind=loopback`, and `tailscale serve status` lists the `https://…ts.net` route as tailnet only.

## Step 2: Mint a single-use join link

Control UI: **Devices → Node host → Create pairing link**, then copy the link privately to the node machine. CLI equivalent on the VPS:

```bash
openclaw devices join-code --json    # prints {"joinUrl": "https://…/j/<code>", "command": "…"}
```

Put only the `joinUrl` value into a private file on the node (for example `~/join.txt`, `chmod 600`), not the JSON document. The link is single-use and expires. Never relay it through a chat transcript.

**Done when:** the join URL exists in that one file on the node and nowhere in chat or shell history.

## Step 3: Connect the node

On the node machine, pick one. `--target-file` reads the join URL from the file and deletes it, and the link is single-use, so each command below needs its own link from Step 2.

**A. Service install (normal path):**

```bash
openclaw connect --target-file ~/join.txt --display-name "Mac Mini" --service
openclaw node status                          # service, pid, command
```

**B. Foreground proof first:** run `openclaw connect --target-file ~/join.txt --display-name "Mac Mini"` without `--service`, watch it register, stop it, then return to Step 2, mint a fresh link, and run A with that fresh file.

The service form writes `~/Library/LaunchAgents/ai.openclaw.node.plist` on macOS or a systemd user unit on Linux; the node log is `~/Library/Logs/openclaw/node.log` on macOS.

**Done when:** `openclaw node status` on the node shows the service running, and `openclaw nodes pending` on the VPS shows one new request from it.

## Step 4: Approve the exact request

On the VPS:

```bash
openclaw nodes pending                      # request id, node name, IP, requested caps
openclaw nodes describe --node "Mac Mini"   # device, model, PATH, current vs pending caps and commands
openclaw nodes approve <request-id>         # that id only; needs operator.admin
openclaw nodes status
```

Compare the request with the machine you just installed: display name, IP, hardware model, requested commands. Approve nothing you did not just create.

After an upgrade the node advertises new capabilities (for example `claude-sessions`, `mcp`, `fs.listDir`) and files a **reapproval** request. Existing caps keep working while it is pending. Approving it grants Gateway agents that new surface (including Claude Code session and terminal control), so read `describe` first and leave it pending if the workflow does not need it.

**Done when:** `openclaw nodes status` shows the node `paired · connected` with no unreviewed request accepted.

## Step 5: Route exec and allowlist named binaries

```bash
openclaw config set tools.exec.node "Mac Mini"
openclaw approvals get --node "Mac Mini"                   # defaults + current allowlist
openclaw approvals allowlist add --agent main --node "Mac Mini" "/usr/bin/uname"
openclaw approvals allowlist add --agent main --node "Mac Mini" "/opt/homebrew/bin/ollama"
openclaw exec-policy show                                  # requested vs host vs effective
```

Agents then run `exec host=node command="/usr/bin/uname -a"`. Keep node defaults at `security=allowlist, ask=on-miss` so anything off the list raises an approval instead of running. One pattern per binary, absolute path, `--agent main` rather than `*`. Never allowlist a shell, an interpreter with arbitrary code, or `rm`. Direct probe from the VPS:

```bash
openclaw nodes invoke --node "Mac Mini" --command system.which --params '{"bins":["ollama"]}' --json
```

**Done when:** `approvals get` shows only binaries with a named use, and an unlisted command produces a pending approval rather than output.

## Step 6: SSH fallback (optional, separate)

SSH covers file transfer, a full login shell, and an offline node. It is a second trust boundary: dedicated non-root user, ed25519 key, verified host key, `IdentitiesOnly yes`, private Tailscale route, `rsync -avn` preview before any write, no destructive defaults. Set it up with the companion `remote-node-ssh` skill only after Steps 1 to 5 pass.

**Done when:** the fallback has a named owner, a least-privilege account, and a tested private route.

## Diagnose by the first failed transition

| Symptom | Meaning | Action |
|---|---|---|
| No connection attempt in `node.log` | route | fix DNS, Serve, TLS, firewall; `tailscale status` on both |
| `403 Proxy client attribution is required` | trustedProxies too wide | narrow `gateway.trustedProxies`, restart |
| `Cannot connect over plaintext ws://` | no TLS on the route | use the Serve `wss://` URL |
| auth error, pending list empty | credential | mint a new join link (Step 2); old links expire |
| `pairing required` | route and auth fine | `nodes pending` → approve the exact id |
| `reapproval pending` after upgrade | new caps requested | `nodes describe`, then approve or leave pending |
| paired but disconnected | node side | `openclaw node status` on the node; sleep, Wi-Fi; prefer Ethernet, disable sleep |
| exec denied or `command not found` | allowlist or PATH | `approvals get --node`; use the absolute path from `nodes describe` PATH |

A request id is stale after any retry that changed the node's identity or requested caps. Re-list before approving. Order: route → auth → pairing → disconnect.

## Verify

```bash
openclaw doctor
openclaw security audit
openclaw security audit --deep
openclaw nodes status
```

Confirm the node reconnects after the last change, the Gateway is unreachable from outside the tailnet, and no log line holds a token. Resolve critical findings; document intentional warnings. Upgrade procedure: `references/upgrade-notes.md`.

## Tested with

OpenClaw 2026.9.3 (Gateway and node), Node 24, Tailscale 1.x, macOS 26 node, Ubuntu 24.04 VPS.

## License

MIT
