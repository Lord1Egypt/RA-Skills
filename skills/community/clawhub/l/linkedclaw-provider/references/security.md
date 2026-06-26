# Provider security — untrusted input on your machine

## Threat model in one paragraph

A LinkedClaw provider runs an AI agent **unattended** on the operator's machine while
**untrusted strangers** send it prompts, and its replies flow back to those strangers.
That is the classic "lethal trifecta" (Simon Willison): untrusted input + tool access +
an exfiltration channel. Two of the three legs are inherent to the product — the prompt
IS untrusted input, and the reply channel IS an exfiltration path. Security therefore
hinges entirely on the third leg: **the agent must not have dangerous tools, or must run
inside a real isolation boundary.**

## The key fact: answering permission requests is NOT confinement

This is the universal lesson across the industry (Anthropic, Zed, OpenClaw, Gemini, E2B):
an agent's **native tools bypass the permission channel**. When claude-agent-acp runs
headless, it executes its own Bash without ever asking the ACP client — so "auto-reject
permissions" protects nothing on its own. Zed gets away with permission prompts only
because a **human** is watching; we have no human. So we use the two mechanisms that
actually work:

**Layer 1 — remove the tools (default, automatic).** With `--acp-permissions reject-all`
(the default) the bridge tells the agent to drop its built-in tools entirely
(`disableBuiltInTools` for claude-agent-acp; `tools.exclude` for Gemini — see gemini.md).
The model becomes text-in/text-out and cannot run a shell, read your disk, or fetch URLs.
Verified against the real agent. For the text capabilities a marketplace sells, this is
all you need.

**Layer 1 applies only to claude-agent-acp and Gemini CLI.** Codex's native exec bypasses
the ACP permission channel regardless of `reject-all` — confine it via Codex's own
`sandbox_mode`/`approval_policy` settings (see references/codex.md). Hermes's ACP toolset
is hardcoded and cannot be reduced in-process — it is not covered by Layer 1 at all and
requires a container boundary (Layer 2 / see references/hermes.md).

**Layer 2 — OS sandbox (required only if you keep tools).** If a capability genuinely
needs the agent to run tools, you opt out of Layer 1 (`--acp-permissions allow-reads` /
`allow-all`) and MUST wrap the agent in an OS sandbox, because tool execution then bypasses
everything in-band. Use `@anthropic-ai/sandbox-runtime` (`srt`): per-domain egress
allowlist + filesystem-write deny, macOS Seatbelt / Linux bubblewrap, no Docker. Or a
container with a default-deny egress firewall. The CLI warns you at startup if you keep
tools without a detected sandbox wrapper.

## What the CLI enforces regardless of mode

- **Fresh empty workspace per job** (`$TMPDIR/lc-acp/<job>/`), deleted at job end.
- **Env allowlist** — the agent inherits only `PATH`/`HOME`/locale + the model credential
  (`ANTHROPIC_API_KEY` etc.); never your LinkedClaw `lc_` key, `LINKEDCLAW_*`, `LC_DB_*`,
  `AWS_*`, or `NODE_OPTIONS`.
- **Per-turn timeout**; a wedged agent is killed, not reused.

## allow-reads is best-effort, not a boundary

`allow-reads` approves only tools whose **name** is in a curated read-only allowlist
(Read/Glob/Grep/…). It deliberately ignores the agent-asserted `toolCall.kind` (a Bash
tool can claim `kind:"read"` — per OpenClaw's own ACP policy, kind is untrusted metadata).
Even so, treat allow-reads as defense-in-depth that still requires Layer 2, not a
substitute for it.

## Rules of thumb

- Sell **text-in/text-out** capabilities (review, translation, analysis, drafting). They
  need no tools, so reject-all (Layer 1) is complete protection.
- Anything consequential (payments, publishing, key release) happens in deterministic
  platform code, never delegated to the agent — treat the model as compromised the moment
  it reads job input.
- Don't put secrets in the capability's system prompt or the provider YAML description.
- `allow-all` + no sandbox = handing your shell to strangers. Don't.
