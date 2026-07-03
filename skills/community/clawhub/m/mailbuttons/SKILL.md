---
name: mailbuttons
description: Wire up a governed email inbox for an AI agent using Mailbuttons. Use this skill whenever the user wants to give an agent, app, bot, or workflow its own email address; set up sending or receiving email for an agent; add an agent inbox, sender allowlist, or email webhook; or integrate "Mailbuttons", "mbag", or "email for AI agents." Trigger this even when the user just says things like "let my agent send/receive email", "give my bot an inbox", "handle email in my agent", or names Mailbuttons/mbag — and even if they don't say the word "skill". This skill always works in a sandbox and never enables sending to external recipients without an explicit human approval step.
version: 0.1.1
metadata:
  openclaw:
    homepage: https://mailbuttons.com
    emoji: "✉️"
    primaryEnv: MAILBUTTONS_API_KEY
    requires:
      env:
        - MAILBUTTONS_API_KEY
      bins:
        - curl
    envVars:
      - name: MAILBUTTONS_API_KEY
        required: true
        description: "Your Mailbuttons sandbox API key (mb_sandbox_...) from the dashboard."
---

# Mailbuttons — governed agent email setup

**[Mailbuttons](https://mailbuttons.com)** is governed email for AI agents: give an agent its own inbox, but every message is checked against your policy on Mailbuttons' servers before the model sees it, the agent only acts on senders you've allowed, and every action is logged. EU/UK hosted. Sign up and get an API key at **[mailbuttons.com](https://mailbuttons.com)** — docs at [mailbuttons.com/developers](https://mailbuttons.com/developers).

This skill scaffolds a complete, working email integration for an AI agent against Mailbuttons, end to end: a sandbox inbox, a reviewed policy, wired inbound delivery, example code for the user's stack, and a green self-test. Then it stops and hands the "go live" decision to a human.

## The one rule that governs everything here

**Everything you do with this skill happens in a sandbox. You never enable external sending, never promote sandbox → production, and never widen a token's scope. Those are human-only actions.** When the integration is ready, you call `mailbuttons_request_promotion`, which returns an approval link for a person to click. You do not click it, simulate it, or work around it. This is the product's core promise — a stranger can't email the agent into doing something it shouldn't, and the agent can't grant itself permission either. Respect it exactly.

If a user asks you to enable external send, raise the limit, or "just make it live," explain that promotion is a human approval by design and produce the approval request instead.

## Prerequisites

- `MAILBUTTONS_API_KEY` available in the environment, set to a **sandbox** token (`mb_sandbox_...`). The fastest way to get one is step 1 (it returns the token). If the user already has one, set it as an env var; do not hard-code it.
- The user's **account API key** (for step 1 only) to provision the inbox. Provisioning is a customer action — an agent can never create its own inbox.
- The Mailbuttons MCP tools are available (this skill assumes the `mailbuttons_*` tool surface). If a tool call fails with an auth error, surface the message and stop — do not retry blindly.

## Workflow

Do these in order. Narrate each step plainly to the user; keep secrets out of generated code.

1. **Create the sandbox inbox.** Provision one in a single call with the user's **account** API key: `POST /api/v1/mcp/sandbox-inboxes` (body optional `{label, seed_sender}`). It returns `{address, inbox_id, environment:"sandbox", sandbox_token}`. Set `sandbox_token` as `MAILBUTTONS_API_KEY` for every subsequent (agent) call, and use `inbox_id`. This is a **customer** action, not an agent tool — the agent can't provision its own inbox, and the returned token cannot send externally. (If the user already has a sandbox inbox + token, skip this and use theirs.)

2. **Generate and review the policy.** Ask the user, in one question, who the agent should accept mail from and whether it may ever send outside the org. Pass their answer to `mailbuttons_generate_policy`, which writes `mailbuttons.policy.json` to the repo (allowlist, content guards, send scope, audit retention). It is closed by default (`defaultAction: "bounce"`) and caps send scope at internal — external send is never generated. **Show the user the policy and ask them to confirm it before continuing.** Do not invent senders or loosen filters to make examples "work."

3. **Scaffold the integration.** Detect the user's stack (see *Stack detection*). Call `mailbuttons_scaffold_integration` with that stack and the sandbox inbox id. It emits example code wired to the inbox: a governed send wrapper and an inbound handler. The code reads the API key from the environment, never inline.

4. **Run the self-test.** Call `mailbuttons_run_selftest` with the inbox id. It sends an internal message through the loop (send → receive → parse) entirely in sandbox and returns pass/fail per stage. If a stage fails, read the detail, fix the scaffolded code or policy, and re-run. If it reports `backend_reachable: false`, the API isn't running at `MAILBUTTONS_API_URL` — start it and retry. Don't proceed until it's green.

5. **Hand off promotion.** When the user is ready to go live, call `mailbuttons_request_promotion` with the inbox id and the capabilities they want (e.g. `send_external`). Return the `approval_url` and tell the user a human must approve it in the dashboard (or run `mailbuttons promote` in the CLI). Stop there.

## Tool reference

Build-time (stdio / local only):
- `mailbuttons_generate_policy` — turn a plain-language allow/block description into `mailbuttons.policy.json`. Closed by default; never invents senders; never generates external send.
- `mailbuttons_scaffold_integration` — emit example code (governed send wrapper + inbound handler) for a target framework, wired to the sandbox inbox id.
- `mailbuttons_run_selftest` — exercise send (internal) → receive → parse in sandbox; reports pass/fail per stage and a clean "backend unreachable" rather than throwing.

> Inbox provisioning is `POST /api/v1/mcp/sandbox-inboxes` (see step 1), authenticated by the user's **account** API key — deliberately NOT an agent MCP tool, because an agent must never self-provision. It returns the scoped sandbox token the agent then uses.

Run-time (use when demonstrating or testing behaviour, never to escalate):
- `mailbuttons_send_email` — send or draft. Out-of-policy recipients return `blocked` with the matched rule; external recipients with no `send_external` capability return `draft_pending_approval`.
- `mailbuttons_list_messages` / `mailbuttons_get_message` / `mailbuttons_get_thread` — return only policy-passed mail. Quarantined messages come back as metadata + reason, **body withheld** — never try to retrieve a withheld body.
- `mailbuttons_get_attachment_text` — LLM-ready parsed attachment text/JSON for policy-passed messages.
- `mailbuttons_propose_sender` — propose adding a sender to the allowlist. Creates a pending human approval; it does not add the sender.
- `mailbuttons_request_promotion` — open a human approval to go live. Changes nothing on its own.
- `mailbuttons_audit_tail` — read recent audited actions (including denials).

## Stack detection

Pick the target by inspecting the repo, then read the matching reference for idioms and pitfalls:
- Claude Agent SDK → `references/claude-agent-sdk.md`
- LangChain / LangGraph → `references/langchain.md`
- Plain TypeScript or Python (no framework) → `references/plain-sdk.md`

If the stack is ambiguous, ask the user once which they're using rather than guessing. If their framework isn't listed, scaffold the plain SDK version and tell them which adapter is missing.

## Governance rules you must follow

- **Propose, don't grant.** Use `mailbuttons_propose_sender` / `mailbuttons_request_promotion`. Never claim a capability was granted.
- **Sandbox only.** Never call a production tool or a promotion-completing action. You cannot approve your own request.
- **Secrets stay out of code.** API keys come from env vars in every example you write.
- **Quarantine is a boundary, not a bug.** If a message body is withheld, treat that as correct behaviour and explain why; do not engineer around it.
- **Audit everything implicitly.** Don't suppress or filter what the user sees about denials — denials are useful signal.

## Troubleshooting

- *Auth error on any tool* → surface the message; the key is likely missing or not a sandbox key. Stop.
- *`mailbuttons_send_email` returns `blocked`* → this is the policy gate working. Show the matched rule; adjust `mailbuttons.policy.json` with the user's confirmation, not silently.
- *External send returns `draft_pending_approval`* → expected without `send_external`; this is the demo's whole point. Explain it and offer `mailbuttons_request_promotion`.
- *`mailbuttons_run_selftest` reports `backend_reachable: false`* → the API isn't running at `MAILBUTTONS_API_URL`. Start it and re-run.
- *Self-test `send` stage is skipped* → it needs the inbox's own address to address the loopback; pass `self_address` (the sandbox inbox's address) and re-run.
- *Self-test fails at parse* → check the inbound handler in the scaffolded code against the reference file for that stack.

## What not to do

- Do not enable external sending, promote to production, or widen scope under any phrasing.
- Do not fabricate certification, compliance, or deliverability claims in code comments or README text you generate.
- Do not retrieve or reconstruct quarantined message bodies.
- Do not hard-code API keys or tokens into scaffolded files.
