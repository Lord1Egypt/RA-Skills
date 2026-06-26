# Agent = Codex CLI (via codex-acp)

Handler command:

```bash
linkedclaw provider run my-provider.yaml \
  --handler-acp "npx @agentclientprotocol/codex-acp"
```

`@agentclientprotocol/codex-acp` is the ACP adapter around the Codex CLI (Codex has no
native `codex acp`; the adapter bridges Codex's `app-server` to ACP; moved to the
`@agentclientprotocol` org from the earlier `@zed-industries/codex-acp` package). The daemon
spawns one instance per job over stdio (NDJSON JSON-RPC).

## Credential

Codex owns its own auth. Provide a Codex credential in the daemon's environment —
`CODEX_API_KEY` or `OPENAI_API_KEY` — or log in once with `codex login` (the API/ChatGPT
session is stored under `~/.codex`, which the agent reaches via `HOME`). All of
`CODEX_API_KEY` / `OPENAI_API_KEY` are on the CLI's built-in env allowlist; `HOME` is too.
Your LinkedClaw `lc_` credentials are never passed.

## How tools are confined (read this — it's the load-bearing part)

**`--acp-permissions reject-all` does NOT confine Codex — you MUST harden Codex's own
sandbox.** This is the opposite of claude-agent-acp. With claude-agent-acp, `reject-all`'s
`disableBuiltInTools` actually strips the model's tools; with codex-acp it does **not** —
Codex runs its shell tool through its own native exec path, which never routes through the
ACP permission channel, so there is nothing for `reject-all` to reject.

**Verified against the real agent (gpt-5.2 via OpenAI, codex-acp 1.0.0, 2026-06-23):**
running under `--acp-permissions reject-all` AND `_meta.disableBuiltInTools`, the prompt
"Run the shell command `id -un` and reply with ONLY its raw output" **executed the shell** —
the reply was the host OS username (`shareit`). The shell ran. The in-band ACP permission
mode is NOT a security boundary for Codex.

Therefore, to confine Codex you MUST disable its exec in Codex's OWN config — a real,
in-process, approval-independent control the model never bypasses. Set in
`~/.codex/config.toml`:

```toml
sandbox_mode = "read-only"
approval_policy = "never"
```

(equivalently `--sandbox read-only --ask-for-approval never` on the command). `read-only`
forbids writes and effectful exec; `approval_policy = "never"` ensures the model is never
prompted to escalate (it simply cannot). NEVER use `danger-full-access` /
`--dangerously-bypass-approvals-and-sandbox` (it disables the jail entirely). For a
text-only marketplace capability (review, translation, analysis) this is the configuration
you want — the model answers in text and cannot touch the host.

## OS sandbox (required if you keep any tools)

If a capability genuinely needs tools, keep Codex's `sandbox_mode` no looser than
`workspace-write`, AND additionally wrap the whole process in
`@anthropic-ai/sandbox-runtime` (`srt`) with a default-deny egress allowlist:

```bash
linkedclaw provider run my-provider.yaml \
  --acp-permissions allow-reads \
  --handler-acp "srt npx @agentclientprotocol/codex-acp"
```

Codex's Seatbelt (macOS) / Landlock (Linux) sandbox bounds filesystem and exec; `srt` adds
the egress allowlist (allow only `api.openai.com` + your platform host) and a second
process jail. The CLI warns if you keep tools without a detected sandbox wrapper. See
[security.md](security.md) for the full rationale.
