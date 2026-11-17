# Runtime Setup: OpenClaw

Host-specific actions for the universal flow in [setup.md](setup.md). Only this
file names OpenClaw commands; the canonical instructions stay host-neutral.

## Install

- Install the `magicpay` plugin through OpenClaw's native plugin manager. Its
  `openclaw.plugin.json` declares both the skill and the `magicpay` Streamable
  HTTP MCP server with `auth: oauth`; do not add a second MCP entry by hand.

## Connect

- `openclaw mcp login magicpay` opens the secure browser OAuth window and keeps
  the token in OpenClaw's owner-only store.
- Manual handoff when no Connect action can be initiated: run
  `openclaw mcp login magicpay`.

## Catalog refresh

- `openclaw mcp reload`. If tools still do not appear, publish the Gateway
  configuration or restart the process that owns the MCP clients. Neither
  repeats OAuth.
- Treat the refreshed catalog as choice-ready only when `begin_request_session`,
  `request_choice`, `decide_request`, and `wait_request` are callable. Follow
  [choices.md](choices.md), including both chat and the MagicPay link/widget.

## Verify and disconnect

- `openclaw mcp doctor --probe` or `openclaw mcp status` confirms the
  connection.
- Per-requester OAuth links belong in private conversations; keep group-chat
  payment disabled unless the payer identity is private to the requester.
- Disconnect through OpenClaw's MCP connection management; it is host-local
  and revokes nothing remotely.
