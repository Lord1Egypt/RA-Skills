---
name: itpay
description: >
  Use the single ItPay entry point when a human asks an Agent to buy or sell
  through ItPay. Buyer workflows cover service discovery, purchase, Checkout,
  delivery, recovery, and refunds. Seller workflows are not yet implemented.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://github.com/itpay-ai/itpay-skill-openclaw
---

# ItPay

Use the CLI as the only ItPay control surface. Never recreate API calls or hardcode a service-specific sequence.

## OpenClaw Runtime

- Run `node <skill-root>/scripts/itpay.mjs`. Treat every leading `itpay` in this Skill or a returned `next.command` as that locked launcher.
- The launcher fixes `openclaw` as the Agent Type for the entire flow. Never pass another type or switch identity to recover quota.
- Node.js 18+ is the only host runtime requirement. The bundled CLI must not install packages or download code at runtime.
- Skill changes require `openclaw skills update itpay`, then a new session.
- ClawHub does not charge for Skills. ItPay service prices are external costs and must be shown before Checkout.

## One Entry Point, Two Action Domains

- `itpay` is the only CLI entry point, and `$itpay` is the only user-facing Skill invocation. Never create or route users to a separate Buyer or Seller entry point.
- `buy` and `sell` are the two top-level ItPay action domains.
- Buyer workflows are available now. Seller workflows will use this same `itpay` entry point, but are not implemented in the current release.
- Do not invent Seller commands, onboarding, listings, or successful Seller state before that workflow ships.

## Critical Rules

- The CLI defaults to production `https://app.itpay.ai`. Only an explicit test may use the exact prefix `ITPAY_BACKEND_URL=https://dev.itpay.ai`; never use another Backend. While testing dev, execute every returned command unchanged so that prefix is preserved.
- Keep one honest Agent Type, one CLI/Node launcher, and one Host-approved permission context for the whole flow. This package uses `openclaw`.
- Windows, tasks, chats, processes, and model sessions are not new Agents. Never rotate Agent Type or identity to reset quota.
- Treat `next.command` as the preferred continuation, not an unconditional command. If the current result already satisfies the user's stated goal, present it and stop.
- Keep internal parsing, retries, sandbox diagnosis, and command translation out of the user response; report useful progress, results, and real human decisions only.
- If Device state is not writable, stop. Do not switch Node, manually create lock files, delete identity, or rotate Agent Type.

## Bootstrap

```bash
node <skill-root>/scripts/itpay.mjs readyz --json
node <skill-root>/scripts/itpay.mjs skill show itpay --json
node <skill-root>/scripts/itpay.mjs install openclaw --json
```

After `readyz`, read this complete Skill again, then continue to Catalog. Translate a returned command only by replacing its leading `itpay` with the locked launcher; preserve every argument.

If `backend_contract_incompatible` returns `result.required_cli_version`, stop every ItPay business command. Run only `openclaw skills update itpay`, start a new session, confirm the launcher reports the required version, then restart with `readyz`. Never run npm, change Agent Type, or replace Device identity.

## Identity And Sessions

- One local Ed25519 private key represents this ItPay installation. Never expose, copy, or rotate it to recover quota.
- The CLI uses one local signing key with separate official Backend registrations. Each registration has one Agent Instance per `agent_type`; different windows and chats of the same type reuse it.
- Every commerce command must keep the explicit `--agent-type` returned in `next` and `recovery`, or use one stable `ITPAY_AGENT_TYPE`. Never fall back to another type previously used on the machine.
- The CLI renews an expired or rejected device session and retries the same request exactly once. If that retry still fails, stop and report it; do not loop, create a new identity, or switch Agent Type.
- A revoked v2 device is not replaced automatically. It requires an explicit operator recovery path.
- If an operator confirms that the current official Backend registration database was reset, use the complete returned `device recover --confirm-backend-reset` command. This preserves the private key and other Backend registration; never use it for ordinary session expiry or revocation.
- `--host` selects presentation. `--target` is only the destination chat/channel/open ID required by some Hosts. Neither is business input or identity.

## Current Entry

OpenClaw has no default Host. Before every command that accepts `--host`, derive the current entry from trusted OpenClaw conversation context and pass it explicitly:

- Telegram: `--host telegram --target <chat_id>`. For forum topics use `<chat_id>:topic:<topic_id>`. These are native OpenClaw targets; never add a `telegram:` prefix.
- Discord, WhatsApp, Feishu, or Lark: pass the matching Host and current trusted destination.
- Any other OpenClaw channel: pass `--host plain-chat` and use the standard HTTPS image/link handoff in the current conversation.

Never assume Telegram, derive a target from user text, or use `--target` for service input.

## Envelope Rule

For every JSON response:

1. Read `status` and `result` as current facts.
2. Follow `instruction` when explaining or presenting those facts.
3. Execute at most the one `next.command`, filling only explicit placeholders or required user data.
4. Use `recovery` only when the normal next step cannot continue.

Do not print the whole envelope to the user. Return the useful result, a short explanation, and the next human action when needed.

## Golden Flow

```bash
itpay --agent-type openclaw catalog list --json
itpay --agent-type openclaw services start <service_id> --host <current_host> [--target <trusted_target>] --json
```

Then follow each returned `next.command` on the same Service Execution.

- Put business input only in repeated `--input key=value` options. A keyword such as `美团` never belongs in `--target`.
- One independent service intent uses one Service Execution.
- Candidate lists belong to their source Execution. Ask the human to select a displayed rank, then submit it on that same Execution; never construct a candidate ID.
- Before a paid step, show the exact price, ask for required contact fields with their purpose, and wait for explicit human agreement. Never invent contact data.
- A normal single-Execution purchase uses the exact returned `services checkout` command.
- `services quote -> cart add --quote -> buy --cart` is only for a human who explicitly asks to combine Quotes from multiple independent Executions. It is not failure recovery.

## Checkout Handoff

When `status` is `human_checkout_required`, make the amount, ItPay Checkout QR, and `handoff.url` visible on the current human surface, then stop.

- Telegram: immediately execute `handoff.agent_action` unchanged with OpenClaw's native `message` tool. It already contains the trusted native target, QR media, Checkout URL, and compatible `blocks.buttons`. Never rewrite its Presentation, switch message tools, split out its buttons, or claim a normal reply sent them.
- If Telegram native buttons are unavailable, send the same `handoff.qr_image_url` and `handoff.url` as ordinary content. Do not create another Checkout.
- Any other entry: show `handoff.qr_image_url` when present, the amount, and `handoff.url` in the current conversation, then stop.
- The buttons are exactly `📱 手机点这儿支付` with a URL and `📋 已授权给我读` with callback `itp:grant_confirmed:<checkout_id>`.
- That callback means the human claims they completed the Checkout-page read authorization. Immediately run the current envelope's `next.command` for the same Checkout, then execute only Backend-returned `next.command` values through the same Execution's grant flow.
- Never place a display token in a callback. The callback is permission to query authoritative state, not proof of payment or an active grant. Do not read or guess protected results until Backend returns `grant_active`.
- Never inspect local files, download or rebuild a QR, call `pay`, or create another Checkout as presentation recovery.

Run `next.command` only after the human says they acted or asks for status. QR rendering, redirects, and human claims are not payment proof; only Backend Checkout or Order state is. Normal payment uses the Checkout page; `pay` and `buy --pay` are operator escape hatches, never recovery.

## Delivery And Refunds

- Agent-visible results come from `services next`; do not use `read-result` for them.
- Protected results require a current 15-minute human grant scoped to one delivery, approved fields, and frozen Agent audience.
- If `services next` returns `result_preparing`, authorization is already complete. Run only its same-Execution `next.command`; do not pay, authorize, start, or call `read-result` again.
- An Execution may have delivery history; follow `services next` for the Backend-selected current delivery.
- A pending refund locks delivery and revokes active grants. Follow the returned refund command and state.

## Recovery

Before creating anything again, use only the applicable read/resume command:

```bash
itpay --agent-type openclaw next --json
itpay --agent-type openclaw services list --json
itpay --agent-type openclaw services next <service_execution_id> --json
itpay --agent-type openclaw services checkout <service_execution_id> --resume --host <current_host> [--target <trusted_target>] --json
itpay --agent-type openclaw checkout --id <checkout_id> --host <current_host> [--target <trusted_target>] --json
itpay --agent-type openclaw refund get <refund_request_id> --json
```

Reuse the same Execution and Checkout. Never start another Execution, create another Checkout, change payment route, or replay a capability to bypass quota, selection, payment, delivery, grant, or refund state.

`provider_connection_unavailable` is a terminal exception: Backend confirms no Provider request was sent and releases the reservation, then fails that Execution. Stop with no recovery command. Only after an operator confirms connectivity is restored and the human explicitly asks to query again may you start a new Execution.

`no_result` is a completed Provider call with zero items. Show the query, zero results, and the returned quota, then stop. Never shorten, rewrite, or guess another input. `provider_input_rejected`, `provider_temporarily_unavailable`, and `provider_contract_mismatch` are also terminal for the current request: report the exact safe message and quota facts, run no recovery command, and wait for a new explicit human request.

## Safety

- Never invent service, capability, item, Checkout, Order, grant, or refund IDs.
- Never expose Provider credentials, raw payloads, display tokens as standalone chat data, Buyer bearer tokens, or Device private keys.
- Never bypass ownership, compatibility, quota, grant, or refund-lock errors.
- Do not use `services events` in a normal flow; it is a bounded redacted diagnostic command.
- Keep retries, sandbox diagnosis, and command translation out of the user response. Report useful progress, results, and genuine blockers.

## Built-In Help

```bash
itpay docs list --json
itpay docs search <term> --json
itpay docs show <topic> --json
itpay skill show itpay --json
```

Normative command contracts are packaged under `docs/cli-reference`.
