---
name: proxima-vps-setup
description: Set up, repair, or document a Proxima deployment on a remote Ubuntu VPS with a non-root Electron runtime, virtual desktop GUI, loopback-only VNC/noVNC/REST exposure, and SSH-stdio MCP access for local IDEs like Antigravity, Windsurf, Zed, or Claude Desktop. Use when a user asks to install Proxima on a VPS, expose the GUI safely, make REST reachable through SSH tunnels, configure `proxima-mcp`, or troubleshoot remote MCP/GUI connectivity.
---

# Proxima VPS Setup

Use this skill to stand up or repair a Proxima-on-VPS deployment end to end.

## Core rules

- Run Proxima as a dedicated non-root Linux user, normally `proxima`.
- Bind GUI, VNC, noVNC, REST, and internal IPC to loopback unless the user explicitly asks for a different exposure model.
- Prefer SSH tunnels and SSH stdio transport over public TCP listeners.
- Do not treat `curl http://localhost:3210/...` on the user's laptop as valid unless an SSH tunnel exists.
- Do not open VNC, noVNC, REST, or MCP directly to the public internet by default.
- Verify every layer after changing it: service status, listening ports, local curl, then remote tunnel behavior.
- Warn clearly that Proxima carries meaningful operational risk and should not be recommended on a primary personal machine.

## Workflow

1. Confirm the host assumptions and whether Proxima is already installed.
2. Read `references/security-and-architecture.md` before making user-facing safety claims.
3. Read `references/server-setup-runbook.md` and apply the server-side setup or repair steps.
4. Read `references/local-access-and-mcp.md` when configuring SSH tunnels or local IDE MCP clients.
5. Read `references/troubleshooting.md` if REST, GUI, VNC, or MCP does not work as expected.
6. Validate the final state with real checks, not assumptions.

## Output expectations

When reporting status, keep it compact and include:
- whether `proxima-app.service` is active
- whether `127.0.0.1:3210`, `127.0.0.1:5902`, `127.0.0.1:6081`, and `127.0.0.1:19222` are listening when expected
- whether local VPS `curl http://127.0.0.1:3210/v1/models` works
- whether `ssh -T <alias> proxima-mcp` works from the user side
- what still blocks completion, if anything

## References

- Read `references/security-and-architecture.md` first for risk framing, binding model, and model-routing caveats.
- Read `references/server-setup-runbook.md` for package install, systemd services, config files, wrapper creation, and validation.
- Read `references/local-access-and-mcp.md` for SSH config, tunnels, and IDE MCP config snippets.
- Read `references/troubleshooting.md` for the common failure modes and exact fixes.
