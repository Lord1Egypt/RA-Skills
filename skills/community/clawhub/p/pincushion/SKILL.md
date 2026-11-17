---
name: pincushion
description: Turn stakeholder feedback into agent work packets. A human drops a visual pin on any live web page; your OpenClaw agent reads it via MCP (selector, screenshot, DOM snippet, thread, acceptance criteria), fixes it, and resolves it.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - npx
        - node
    primaryEnv: PINCUSHION_LICENSE_KEY
    envVars:
      - name: PINCUSHION_LICENSE_KEY
        required: false
        description: Pincushion license key for cloud sync (free tier included). Omit to run local-only; add it — or a .feedback/.license-key file — when a human should be able to drop pins on a deployed/staging site while your agent is running headless.
    emoji: "🧷"
    homepage: https://pincushion.io
---

# Pincushion for OpenClaw

Pincushion is the implementation-context layer for AI-native development. A stakeholder drops a visual **pin** on any web page. A pin isn't a feedback item — it's an **agent work packet**: the page URL, element selector, screenshot, viewport, DOM snippet, comment thread, likely files, and acceptance criteria. Your always-on OpenClaw agent reads those pins over MCP, implements the fix, and resolves them — closing the loop without a human ever opening an IDE.

This skill gets Pincushion running against **your** project and hands you the read → claim → fix → resolve loop. Follow the steps in order. Each is one command.

## Prerequisites

- Node.js (`node`/`npx` on PATH). Check: `node --version`. The MCP server runs via `npx pincushion-mcp` — no global install needed.

## 1. Register the Pincushion MCP server

Add the server to your OpenClaw config. Replace `/path/to/your/project` with the absolute path of the repo this agent works in:

```bash
openclaw mcp add pincushion \
  --command npx \
  --arg -y \
  --arg pincushion-mcp \
  --arg --project-dir \
  --arg /path/to/your/project \
  --arg --cloud-sync
```

This writes an `mcp.servers.pincushion` entry to `openclaw.json`. Reload so the tools register:

```bash
openclaw mcp reload && openclaw mcp list
```

You should see `pincushion` with its tools (`get_actionable_pins`, `claim_pin`, `fix_and_resolve`, …). If you prefer to paste config directly, `config-snippet.json` in this bundle is the exact `mcp.servers` block.

## 2. Authenticate (enables cloud sync)

The server runs **local-only with no key** — it will already read pins from the project's `.feedback/` directory. To let a human drop pins on a **deployed or staging site while your agent runs headless**, add a license key (free tier: 1 project, unlimited pins, no usage caps).

Pick whichever fits your host — **do not** rely on passing the key through the MCP `env` block: OpenClaw's env-safety filter only allowlists `*_API_KEY`-style names, and `PINCUSHION_LICENSE_KEY` can be stripped.

- **Host has a browser** (or supports device sign-in):
  ```bash
  npx pincushion-mcp login
  ```
  Opens sign-in and saves the key locally.

- **Headless VPS / Mac mini:** get a key from https://pincushion.io (free), then write it into the project so the server picks it up on start:
  ```bash
  echo "YOUR_LICENSE_KEY" > /path/to/your/project/.feedback/.license-key
  ```
  (Or export `PINCUSHION_LICENSE_KEY` on the **host process** — not via MCP env.)

## 3. Register the project and give a human the fastest path to a first pin

Register the project so pins on your live URLs sync back. From the agent, call the MCP tool:

- `configure_project` — pass your project name, your local dev URL, **and** your deployed/staging URL.

Then, because OpenClaw runs headless and your stakeholders won't be installing a Chrome extension, hand them the **no-install widget**. Paste this one line into your app's root layout/HTML and anyone who opens the site can drop a pin — no extension, no account:

```html
<script src="https://pincushion.io/widget/pin.js" data-project="YOUR_PROJECT_ID" defer></script>
```

`YOUR_PROJECT_ID` comes back from `configure_project`. The widget captures the same work-packet fields as the extension (selector, DOM snippet, viewport) and signs stakeholders in with Google for their avatar. This is the seamless path — a stakeholder's first pin in seconds.

## 4. Run the loop

Once pins exist, this is the core cycle. Prefer `get_actionable_pins` as your polling entry point:

1. `get_actionable_pins` — pins waiting on you (sent-to-agent, follow-ups, open reviews). For approved-work batches, use `implement_approved_pins` instead (groups pins into one-branch-per-page packets).
2. `claim_pin` — mark the pin `implementing` so no one double-works it.
3. Make the code change. Read the thread and use the element selector to grep the source.
4. `fix_and_resolve` — pass `commitSha` (`git rev-parse HEAD`), `branchName` (`git branch --show-current`), and `prUrl` if you opened one. The pin drops out of the stakeholder view; the commit is the record.

Being always-on, you can poll `get_actionable_pins` on your heartbeat and act on new pins as they land.

## Handy extras

- **Never seen Pincushion?** Call `start_quickstart_demo` for a ~60-second sandboxed read-pin → fix-code → resolve walkthrough. No browser, no account, writes nothing real. Finish with `resolve_quickstart_demo`.
- **Ask a clarifying question on a pin:** `add_agent_reply`.
- **Approve a pin for implementation:** `approve_pin` (only approved pins should be auto-implemented).
- **Share a read-only crit report** (numbered pins + threads + status, no install for viewers): `create_share_report`.
- **Notify a channel:** `configure_collaboration_integration` wires a Slack / Teams / Discord incoming webhook; defaults are low-noise (`pin_ready`, `mention`, `follow_up`).

## Troubleshooting

- **`pincushion` missing from `openclaw mcp list`:** run `openclaw mcp reload`; confirm `node`/`npx` are on PATH; check the `--project-dir` path is absolute and exists.
- **Pins don't sync from the deployed site:** you're running local-only — complete step 2 (license key) and make sure the project + its live URL are registered via `configure_project`.
- **License key ignored:** it was likely filtered from MCP `env`. Use `.feedback/.license-key` or set it on the host process instead.

Docs: https://pincushion.io/docs
