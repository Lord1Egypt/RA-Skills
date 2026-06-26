---
name: imans-claw
description: Use the Imans CLI from OpenClaw agents to query Imans workspace, catalog, and sales order data as JSON. Use when OpenClaw users ask about Imans products, variants, sales orders, workspace metadata, or CLI-based Imans automation.
homepage: https://github.com/imans-ai/imans-cli
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["imans"]},"install":[{"id":"brew","kind":"brew","formula":"imans-ai/tap/imans","bins":["imans"],"label":"Install imans (brew)"},{"id":"download","kind":"download","url":"https://github.com/imans-ai/imans-cli/releases/latest","bins":["imans"],"label":"Download imans release"}]}}
---

# Imans for OpenClaw

Use `imans` when an OpenClaw user asks for Imans workspace, catalog, product variant, sales order, order item, or classification data.

## OpenClaw Setup

- The `imans` binary must be on the host `PATH` where OpenClaw executes shell commands.
- If the agent runs in a sandbox or container, install `imans` inside that sandbox too.
- Verify the skill is loaded with `openclaw skills list`.
- Test the skill explicitly with `/skill imans-claw` or by asking for Imans product or order data.

## Imans Setup

- Install: `curl -fsSL https://imans.ai/install | bash`
- Homebrew: `brew install imans-ai/tap/imans`
- Verify: `imans version`
- Login interactively: `imans login`
- Login without prompts: `imans login --token-env IMANS_TOKEN` or `imans login --token-stdin < token.txt`
- Test auth: `imans auth test --quiet`

## OpenClaw Usage Rules

- Prefer `--json` so the agent can parse results reliably.
- Prefer `--all --json` for complete exports, but only when the user asks for full data.
- Use `--profile <name>` for a named workspace instead of changing the active profile.
- Keep chat responses compact; summarize results rather than dumping raw JSON into mobile or group channels.
- Ask for confirmation before exposing large order/customer datasets or running broad unfiltered exports.
- Never print or request raw API tokens in chat.

## Commands

- Workspace: `imans workspace get --json`
- Profiles: `imans profile list`
- Auth check: `imans auth test --quiet`
- Products: `imans products list --all --json`
- Product search: `imans products list --search "<query>" --json`
- Product details: `imans products get <id> --json`
- Variants: `imans product-variants list --product-id <product-id> --all --json`
- Sales orders by date: `imans sales-orders list --order-date-from <yyyy-mm-dd> --order-date-to <yyyy-mm-dd> --all --json`
- Sales orders by status: `imans sales-orders list --order-status <status> --json`
- Sales order details: `imans sales-orders get <id> --json`
- Sales order items: `imans sales-order-items list --order-id <order-id> --all --json`
- Classifications: `imans sales-order-classifications list --all --json`

## Response Pattern

1. Identify the needed resource and filters from the user request.
2. Run the narrowest `imans` command that answers the question.
3. Parse JSON locally in the agent when possible instead of showing raw output.
4. Summarize key fields, counts, anomalies, and next useful drill-downs.
5. Mention the profile used if the user works with multiple workspaces.

## Safety

- Treat Imans data as business-sensitive.
- Avoid `imans login --token <token>` because it can leak through shell history.
- Prefer `--token-env` or `--token-stdin` for automation.
- `--debug` is safe for auth headers, but only use it when troubleshooting.
- Exit code `3` means auth failed, `4` means insufficient scope, `5` means not found, `6` means network failure, and `7` means API server error.
