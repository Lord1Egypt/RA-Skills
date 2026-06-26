---
name: perkoon-transfer
version: 2.0.2
description: >
  The agent data layer. Perkoon moves files between agents and the physical world —
  agent to human, agent to agent, agent to pipeline. P2P over WebRTC.
  Free. Encrypted. Unlimited. No accounts. Files never touch our servers.
  CLI, MCP server, A2A protocol, browser automation — pick the interface
  that fits your runtime.
homepage: https://perkoon.com
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins:
        - node
    install:
      - id: perkoon
        kind: node
        package: perkoon
        bins:
          - perkoon
        label: Install Perkoon CLI
---

# Perkoon — The Agent Data Layer

File transfer for humans and the things replacing them.

Your agent has compute, memory, and context. What it lacks is a jump gate to the physical world. Perkoon is that gate — P2P file transfer over WebRTC, engineered for autonomous machines from day one.

Not "AI-ready" the way a gas station is gourmet-ready. Actually built for machines — JSON event streams, structured exit codes, MCP native tools, an A2A protocol endpoint, and a state machine that doesn't need a browser, a mouse, or a soul.

**Four integration methods — pick the one that fits your runtime:**

| Method | Best for | Install size |
|--------|----------|-------------|
| **MCP Server** | Coding agents (Claude Code, Cursor, Windsurf, VS Code Copilot) | ~8 MB |
| **CLI** | Agents with shell access | ~8 MB |
| **A2A Protocol** | Agents with HTTP but no shell (ChatGPT, web agents) | Zero — just POST |
| **Browser Automation** | Full UI control via Playwright/Puppeteer | ~200 MB (Chromium) |

**Three supported flight paths:**
- **Agent → Human**: Your agent sends a file. The human opens a link in any browser. No install on their end.
- **Agent → Agent**: CLI to CLI, MCP to MCP, or A2A to A2A. Two machines, no humans in the loop.
- **Agent → Pipeline**: Stream received files to stdout, pipe into processing. No disk writes required.

P2P transfers are free, unlimited, and encrypted. Both ends need to be online — that's the only constraint. For sensitive files, always use `--password` — without it, anyone with the share link can download.

---

## METHOD 1: MCP Server (recommended for coding agents)

If your host supports MCP, this is the fastest path. Three native tools, zero shell commands.

Install: `npx -y @perkoon/mcp@0.2.2` (stdio transport, pinned version)

**Tools provided:**
- `send_file` — Send a file. Returns session code + share URL. Waits for receiver.
- `receive_file` — Receive files from a session code. Saves to disk.
- `check_session` — Check if a session is active, expired, or not found.

Configuration for common hosts:

```json
{
  "mcpServers": {
    "perkoon": {
      "command": "npx",
      "args": ["-y", "@perkoon/mcp@0.2.2"]
    }
  }
}
```

- **Claude Code**: Add to `.mcp.json` in your project
- **Claude Desktop**: Add to `claude_desktop_config.json`
- **Cursor / VS Code / Windsurf**: Settings → MCP → Add Server → `npx -y @perkoon/mcp@0.2.2`

Once configured, just call the tools directly — no bash, no log polling, no background processes.

---

## METHOD 2: CLI (for agents with shell access)

**IMPORTANT**: Use `npx -y perkoon@0.4.5` (pinned version) to avoid dynamic fetching of unaudited code.

### SENDING a file

#### Step 1: Confirm the file path with the user, then start send

Before sending, confirm the file path and name with the user. Do not send files from sensitive directories without explicit user approval.

Replace `/path/to/file` with the actual file path:

```bash
rm -f /tmp/perkoon-send.log /tmp/perkoon-send.pid
npx -y perkoon@0.4.5 send /path/to/file --json --timeout 1800 > /tmp/perkoon-send.log 2>&1 &
echo $! > /tmp/perkoon-send.pid

# Wait for session code (up to 30s)
for i in $(seq 1 30); do
  if grep -q session_created /tmp/perkoon-send.log 2>/dev/null; then
    grep session_created /tmp/perkoon-send.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-send.log 2>/dev/null; then
    echo "===SEND FAILED===" && cat /tmp/perkoon-send.log
    break
  fi
  sleep 1
done
```

Output: `{"event":"session_created","session_code":"K7MX4QPR9W2N","share_url":"https://perkoon.com/K7MX4QPR9W2N"}`

Once `session_created` appears, share the URL with the user. Example: "Here's your file — open this link on any device to download it: https://perkoon.com/K7MX4QPR9W2N"

The receiver doesn't need to install anything. The link works in any browser.

For password-protected sends, add `--password SECRET` and share both the URL and password.

#### Step 2: Monitor until complete — then REPORT BACK

You MUST run this after sharing the link. Do NOT skip this step.

```bash
for i in $(seq 1 360); do
  if grep -q transfer_complete /tmp/perkoon-send.log 2>/dev/null; then
    echo "===TRANSFER COMPLETE===" && grep transfer_complete /tmp/perkoon-send.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-send.log 2>/dev/null; then
    echo "===TRANSFER FAILED===" && grep error /tmp/perkoon-send.log
    break
  fi
  if [ "$((i % 30))" -eq 0 ]; then
    grep progress /tmp/perkoon-send.log 2>/dev/null | tail -1
  fi
  sleep 5
done
```

- **`===TRANSFER COMPLETE===`** → Tell the user: "File sent successfully!" Include speed and duration from the JSON.
- **`===TRANSFER FAILED===`** → Tell the user what went wrong.
- **You MUST tell the user the outcome. Never finish silently.**

### SENDING into a pre-created session (Agent → Agent)

When another agent creates a session via A2A and gives you a session code + sender key:

```bash
rm -f /tmp/perkoon-send.log /tmp/perkoon-send.pid
npx -y perkoon@0.4.5 send /path/to/file --session CODE --sender-key KEY --json --timeout 1800 > /tmp/perkoon-send.log 2>&1 &
echo $! > /tmp/perkoon-send.pid
```

Then monitor with the same Step 2 above. This joins an existing session as sender instead of creating a new one. The receiving agent runs `npx -y perkoon@0.4.5 receive CODE --json` on their end.

### RECEIVING a file

Replace `CODE` with the 12-character session code:

```bash
rm -f /tmp/perkoon-recv.log /tmp/perkoon-recv.pid
npx -y perkoon@0.4.5 receive CODE --json --overwrite --output /home/openclaw/.openclaw/workspace/received/ > /tmp/perkoon-recv.log 2>&1 &
echo $! > /tmp/perkoon-recv.pid

for i in $(seq 1 360); do
  if grep -q transfer_complete /tmp/perkoon-recv.log 2>/dev/null; then
    echo "===TRANSFER COMPLETE===" && grep transfer_complete /tmp/perkoon-recv.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-recv.log 2>/dev/null; then
    echo "===TRANSFER FAILED===" && grep error /tmp/perkoon-recv.log
    break
  fi
  sleep 5
done
```

For password-protected sessions, add `--password SECRET`.

- **`===TRANSFER COMPLETE===`** → Tell the user: "File received!" and the save path.
- **`===TRANSFER FAILED===`** → Tell the user what went wrong.
- **You MUST tell the user the outcome. Never finish silently.**

Files are saved to `/home/openclaw/.openclaw/workspace/received/`.

### Pipe to stdout

Stream a received file directly into another process — no disk write:

```bash
npx -y perkoon@0.4.5 receive CODE --output - > /path/to/destination
```

---

## METHOD 3: A2A Protocol (for agents with HTTP, no shell)

If you can make HTTP requests but can't run shell commands, use the A2A endpoint directly.

**Endpoint:** `POST https://perkoon.com/a2a`
**Protocol:** JSON-RPC 2.0
**Agent Card:** `https://perkoon.com/.well-known/agent.json`

### Discover capabilities

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
      "parts": [{ "type": "data", "data": { "skill": "describe" } }]
    }
  }
}
```

### Create a send session

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
      "parts": [{
        "type": "data",
        "data": {
          "skill": "send-files",
          "name": "quarterly-report"
        }
      }]
    }
  }
}
```

Returns `sender_url` (for browser upload) + CLI commands + `sender_key` for A2A sender joining.

If you have shell access, run the CLI command from the response. If not, share the `sender_url` with your user — they open it in any browser to upload.

### Join a session as receiver

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
      "parts": [{
        "type": "data",
        "data": {
          "skill": "receive-files",
          "session_code": "K7MX4QPR9W2N"
        }
      }]
    }
  }
}
```

### Check session status

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
      "parts": [{
        "type": "data",
        "data": {
          "skill": "session-status",
          "session_code": "K7MX4QPR9W2N"
        }
      }]
    }
  }
}
```

### Runtime hints

Include `clientCapabilities` in your DataPart to get optimized instructions:

```json
{
  "type": "data",
  "data": {
    "skill": "send-files",
    "clientCapabilities": { "shellAccess": true, "nodeJs": true }
  }
}
```

Agents declaring shell access get CLI commands. Web-only agents get browser URLs.

---

## METHOD 4: Browser Automation (Playwright/Puppeteer)

For agents that need full browser UI control. Heavier than CLI but gives visual verification.

**Ready-to-run scripts** (requires `npm install playwright`):

```bash
curl https://perkoon.com/perkoon_send.mjs > send.mjs && node send.mjs /path/to/file.zip
curl https://perkoon.com/perkoon_receive.mjs > receive.mjs && node receive.mjs SESSION_CODE ./output
```

### Manual sender flow

1. Navigate to `https://perkoon.com/create`, accept TOS, click Start
2. Skip confirmation modals: `localStorage.setItem('perkoon_skip_confirm_direct-confirm', 'true')` and `localStorage.setItem('perkoon_skip_confirm_staged-confirm', 'true')`
3. Add files: `page.setInputFiles('[data-testid="file-input"]', filePath)`
4. Share session code with recipient
5. Wait for receiver: `page.waitForFunction(() => window.__perkoon?.participants?.length >= 2, null, { timeout: 300000 })`
6. Click `[data-testid="send-transfer"]`
7. Wait: `page.waitForFunction(() => window.__perkoon?.transfer?.status === 'complete', null, { timeout: 600000 })`

### Manual receiver flow

1. Register download handler: `page.on('download', d => downloads.push(d))`
2. Navigate to `https://perkoon.com/{SESSION_CODE}?agent=true`
3. Accept transfer: wait for `[data-testid="transfer-accept"]`, then click it. This is the RECEIVE-side accept in the "Incoming Transfer" dialog (it appears once the sender's offer arrives) — distinct from the sender's session-creation gate `[data-testid="tos-accept"]`. Reject is `[data-testid="transfer-reject"]`. `?agent=true` picks the sink but does NOT auto-accept.
4. Wait: `page.waitForFunction(() => window.__perkoon?.transfer?.status === 'complete', null, { timeout: 600000 })`
5. Save: `await download.saveAs('./received/' + basename(download.suggestedFilename()))`

---

## CLI reference

| Flag | Description |
|------|-------------|
| `--json` | Machine-readable JSON events (always use for automation) |
| `--session <code>` | Join an existing session as sender (A2A agent-to-agent) |
| `--sender-key <key>` | Auth key for `--session` (provided by session creator) |
| `--password <pw>` | Password-protect the session (transfer is WebRTC/DTLS-encrypted regardless) |
| `--timeout <sec>` | Peer wait time (default: 300, use 1800 for sends) |
| `--output <dir>` | Save directory (default: ./received) |
| `--output -` | Stream to stdout (no disk write) |
| `--overwrite` | Replace existing files |
| `--quiet` | Suppress human-readable output |

## JSON event stream

Events appear in order on stdout when using `--json`. The sequence **differs by direction** — parse the set that matches the command you ran.

**`send`:**

| Event | Meaning | Key fields |
|-------|---------|------------|
| `file_ready` | File queued for send | `name`, `size` |
| `session_created` | Ready — share the link now | `session_code`, `share_url` |
| `waiting_for_receiver` | Session live, no peer yet | |
| `receiver_connected` | Peer joined | |
| `transfer_accepted` | Receiver accepted the transfer | |
| `webrtc_connected` | Direct P2P link established | |
| `progress` | Transfer in progress | `percent`, `speed`, `eta` |
| `transfer_complete` | Done | `duration_ms`, `speed` |

**`receive`:**

| Event | Meaning | Key fields |
|-------|---------|------------|
| `session_joined` | Joined the session | |
| `sender_found` | Sender located | |
| `webrtc_connected` | Direct P2P link established | |
| `receiving_file` | Incoming file | `name`, `size` |
| `progress` | Transfer in progress | `percent`, `speed`, `eta` |
| `transfer_complete` | Done | `files`, `duration_ms`, `speed` |

Either direction emits `error` (`message`, `exit_code`) on failure.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Bad arguments |
| 2 | File not found |
| 3 | Network/session error |
| 4 | Wrong password |
| 5 | Timeout — no peer joined |

## Rate limits

Session endpoints are rate-limited **per IP**, sliding 60-second window:

| Action | Limit |
|--------|-------|
| Create a session (send) | 10 / min |
| Join a session (receive) | 30 / min |
| Status checks | 20 / min |

Exceeding a limit returns HTTP `429` with a `Retry-After` value (seconds). On `/a2a`, every JSON-RPC POST counts against the **create** budget (10/min), regardless of skill.

**How this looks to you:** the CLI surfaces a 429 as a fast **`exit_code: 3`** (network/session error) *before* a `session_created` event. If a send fails fast with exit 3 after several rapid sessions, treat it as rate-limiting: back off ~30s and retry, don't hammer.

---

## Rules

1. ALWAYS use `--json` for parseable output
2. ALWAYS confirm the file path with the user before sending
3. Once `session_created` appears, share the URL with the user
4. ALWAYS use `--timeout 1800` for sends (30 min for the human to open the link)
5. ALWAYS use `--overwrite` for receives
6. ALWAYS monitor until `transfer_complete` or `error` — then **tell the user the result**
7. NEVER kill the process mid-transfer
8. The receiver does NOT need perkoon installed — the browser link works for everyone
9. Use pinned versions: `npx -y perkoon@0.4.5` — never use `@latest`
10. NEVER send files from sensitive directories (~/.ssh, ~/.gnupg, /etc) without explicit user approval

## Discovery endpoints

| URL | What it is |
|-----|-----------|
| `https://perkoon.com/.well-known/agent.json` | A2A agent card (machine-readable capabilities) |
| `https://perkoon.com/llms.txt` | Full agent integration guide |
| `https://perkoon.com/automate` | Human-readable automation docs |
| `https://www.npmjs.com/package/@perkoon/mcp` | MCP server package |
| `https://www.npmjs.com/package/perkoon` | CLI package |
