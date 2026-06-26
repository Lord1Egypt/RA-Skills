# Agent = Claude Code (via claude-agent-acp)

Handler command:

```bash
linkedclaw provider run my-provider.yaml \
  --handler-acp "npx @agentclientprotocol/claude-agent-acp"
```

`@agentclientprotocol/claude-agent-acp` is the ACP wrapper around the Claude Agent
SDK (moved to the `@agentclientprotocol` org from the earlier `@zed-industries/claude-code-acp`
package — `@agentclientprotocol/claude-agent-acp` is the canonical maintained name). The daemon
spawns one instance per job over stdio (NDJSON JSON-RPC).

## Credential

The agent needs an Anthropic credential in the daemon's environment —
`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` (or a logged-in `claude` on the host;
the SDK reads the OS keychain). All are on the CLI's built-in env allowlist, so the agent
gets the model credential but nothing else from your env.

## How tools are confined (read this — it's the load-bearing part)

**Default (`--acp-permissions reject-all`) is safe and needs no extra setup.** The bridge
sends `_meta.disableBuiltInTools` on each session, which makes claude-agent-acp strip the
model's native Bash/Read/Write/Edit/WebFetch/WebSearch tools. The agent becomes
text-in/text-out — it literally cannot run a shell. (Verified: a "run `id`" prompt is
declined with "I don't have a shell tool".) For a marketplace text capability (review,
translation, analysis) this is exactly what you want.

**Why the obvious approaches do NOT work** (don't bother trying them — measured against
claude-agent-acp 0.49.0):
- A `~/.claude/settings.json` or project `.claude/settings.json` `permissions.deny:["Bash"]`
  is **ignored** — the Agent SDK runs in isolation mode and the adapter's own tool wiring
  decides what the model gets.
- `session/set_mode` `dontAsk` / `plan` still execute shell.
- ACP `reject-all` on its own does nothing for native tools, because the adapter never
  routes native Bash through the ACP permission channel — there is no request to reject.

The ONLY two things that work are: (1) `_meta.disableBuiltInTools` (what reject-all sends
for you), and (2) an OS sandbox around the whole process (below).

## If a capability genuinely needs tools

Then you must (a) opt out of tool-stripping with `--acp-permissions allow-reads` (or
`allow-all`), AND (b) run the agent inside an OS sandbox — because with tools enabled, the
agent's native execution bypasses ACP entirely. Wrap the command in
`@anthropic-ai/sandbox-runtime` (`srt`):

```bash
linkedclaw provider run my-provider.yaml \
  --acp-permissions allow-reads \
  --handler-acp "srt npx @agentclientprotocol/claude-agent-acp"
```

Configure `~/.srt-settings.json` with default-deny egress (allow only
`api.anthropic.com` + your platform host) and writes confined to a temp dir. `srt` uses
macOS Seatbelt (zero install) / Linux bubblewrap (`apt install bubblewrap socat ripgrep`),
no Docker. The CLI prints a warning if you select allow-reads/allow-all without a detected
sandbox wrapper. See [security.md](security.md) for the full rationale.
