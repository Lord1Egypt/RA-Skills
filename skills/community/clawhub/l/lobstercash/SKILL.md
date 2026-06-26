---
name: lobstercash
description: 'Use this skill when the user wants to spend money, make purchases, send crypto, pay for APIs, browse websites for shopping, complete checkout, or manage an AI agent''s payment wallet. Covers buying products online with credit cards (with browser-automated checkout when available, or driven by the agent''s own browser tooling otherwise), sending tokens, paying for x402 protocol APIs, checking balances, depositing funds, browsing available services, and signing on-chain transactions — all with secure guardrails, and appropriate human controls. Trigger on any spending, wallet, or shopping intent: "buy this", "pay for that", "send tokens", "how much do I have", "what can I buy", "top up my wallet", "get a card", "set up payments", "find me something to buy", "complete the checkout", or "browse that site" — even if the user doesn''t mention "lobster", "crypto", or "Solana" directly.'
metadata:
  version: "0.0.16"
---

# Lobster Cash CLI Skill

The Lobster Cash CLI (`lobstercash`) gives AI agents payment tools — a blockchain wallet, virtual cards for buying anything online, optional cloud browser automation for browsing sites and completing checkout, and x402 protocol support for paying APIs — all with human approval in the loop. Use `lobstercash <command> --help` for full flag details on any command.

## Installation

Install globally:

```bash
npm install -g @crossmint/lobster-cli
```

After installation, all commands are available via the `lobstercash` binary.

## Steps to use this skill

### 1. Version check (automatic)

The CLI automatically checks for updates on every API call. If an update notice appears in the command output, tell the user and offer to run `npm update -g @crossmint/lobster-cli`. If the notice says the update is **required**, you must also update the skill from https://www.lobster.cash/install before continuing. Do not run separate version-check commands.

### 2. Select lobstercash agent to use

Every lobstercash command operates on the **active agent**. Before doing anything else, make sure the right agent is selected.

```bash
lobstercash agents list
```

Then follow this decision tree:

1. **You see yourself in the list and it says `(active)`** → You're good. Move on.
2. **You see yourself in the list but it's NOT active** → Run `lobstercash agents set-active <agentId>` with the matching ID, then move on.
3. **No agent matches you** (or the list is empty) → Register a new one. Read the [agents reference](references/agents.md) for how to register one.

**How to recognize yourself:** Match by name. If you are Claude Code, look for an agent named "Claude Code" or similar. Same for Cursor, Codex, Gemini, etc. If you aren't sure, ask the user which agent to use.

### 3. Route based on the user's intent

Determine which scenario applies and follow the corresponding section:

- **A) Buy something online** (product, subscription, domain, service) → [Buy something online](#a-buy-something-online)
- **B) Pay for a paid API endpoint** (x402 protocol) → [Pay an API with x402](#b-pay-an-api-with-x402)
- **C) Anything else** (check balance, send crypto, view status, link wallet, browse examples) → [Other actions](#c-other-actions)

---

## A) Buy something online

Use when the user wants to purchase a product, subscription (not yet but comming soon), domain, or any item from an online store. The flow is the same either way: discover the product and price, size a virtual card, then drive checkout in a browser. What changes is **who drives the browser** for this install. Run:

```bash
lobstercash config get browser-enabled
```

- `browser-enabled: true` → Lobster Cash's built-in browser automation (`purchase explore` / `purchase run`) drives the merchant site for you. Follow [references/purchase-flow.md](references/purchase-flow.md).
- `browser-enabled: false` → Lobster Cash's built-in browser automation is **not** available for this install. Do not run `purchase explore` or `purchase run`. Follow [references/purchase-flow-byo.md](references/purchase-flow-byo.md) — the same flow, but you (the agent) drive the merchant site using whatever browser-automation tooling you already have available in this environment (your IDE's browser tool, an MCP browser server, OpenClaw, etc.), and use `cards reveal` to get the credentials to enter at checkout.

If `browser-enabled: false` and you have **no** browser-automation tooling available in this environment, tell the user you can't drive the browser yourself and offer to run the checkout manually: you'll get the card credentials with `cards reveal` and walk them through entering them at the merchant's checkout page themselves.

---

## B) Pay an API with x402

Use when the user wants to call a paid API endpoint that uses the x402 payment protocol. The CLI handles the payment negotiation automatically: the server returns HTTP 402, the CLI pays with USDC from the agent wallet, and the server returns the content.

### Step 1: Ensure the wallet has funds

```bash
lobstercash status
```

Route based on the result:

- **Wallet configured + has enough funds** → proceed to step 2.
- **Wallet configured + insufficient funds** → run `lobstercash crypto request --amount <needed> --description "<description>"` to top up, show the approval URL, wait for user confirmation, then proceed.
- **Wallet not configured** → run `lobstercash crypto request --amount <needed> --description "<description>"` (bundles wallet creation + funding). Show the approval URL, wait for user confirmation, verify with `lobstercash status`, then proceed.

The `--description` must explain what the agent will spend the funds on — derive it from the user's task, not generic filler like "top up wallet".

See [crypto request reference](references/crypto-request.md) for the full crypto request flow.

### Step 2: Fetch the paid endpoint

```bash
lobstercash crypto x402 fetch <url>
```

For POST requests add `--json '{"key": "value"}'`. For custom headers add `--header "Authorization: Bearer <token>"`.

### Step 3: Report the result

Report what the API returned (the `body` field), not the payment mechanics. Only mention the payment if the user asks.

If the fetch fails, add `--debug` and run again. See [x402 reference](references/x402.md) for output format and common failures.

---

## C) Other actions

For everything else — checking balances, sending crypto, viewing wallet status, linking a wallet, or browsing examples — use the matching command from the Quick Reference below and read the corresponding reference file for details.

**Run the command, report its output.** For read-only commands (`crypto balance`, `status`, `examples`), execute them directly and report what they say. Do not pre-check status and construct your own summary — the CLI output already handles unconfigured states with clear messaging. If a command fails with exit code 2 (wallet not set up), tell the user and offer to run `lobstercash setup` or the appropriate setup-bundling command.

Common actions:

- **Check balance:** `lobstercash crypto balance` → [balance reference](references/balance.md)
- **Send tokens:** `lobstercash crypto send --to <addr> --amount <n> --token usdc` → [send reference](references/send.md)
- **View wallet status:** `lobstercash status` → [status reference](references/status.md)
- **Browse examples:** `lobstercash examples` → [examples reference](references/examples.md)
- **Link wallet / configure agent (setup only):** `lobstercash setup` → [setup reference](references/setup.md). Use when the user says "configure", "set up", "link wallet", or similar — and isn't trying to make a purchase.
- **Sign/submit a transaction:** `lobstercash crypto tx create` → [tx reference](references/tx.md)

For crypto operations (`crypto send`, `crypto tx create`), always run `lobstercash status` first to confirm the wallet is configured and has sufficient funds. If not, use `lobstercash crypto request --amount <needed> --description "<description>"` to fund it — see [crypto request reference](references/crypto-request.md).

## Quick Reference

```bash
lobstercash agents register --name "<name>" --description "<desc>" --image-url "<url>"  # register a new agent
lobstercash agents list                                          # list all agents
lobstercash agents set-active <agentId>                          # set active agent
lobstercash config get browser-enabled                           # check which browser drives online purchases (used in Section A)
lobstercash examples                                             # browse working examples
lobstercash status                                               # check status & readiness & wallet address
lobstercash setup                                                # link agent to wallet (no purchase needed)
lobstercash crypto balance                                       # check balances
lobstercash crypto send --to <addr> --amount <n> --token usdc    # send tokens
lobstercash crypto x402 fetch <url>                              # pay for API
lobstercash crypto request --amount <n> --description "<desc>"    # request crypto funding / top up (bundles wallet setup)
lobstercash crypto tx create|approve|status                      # low-level transaction management
lobstercash cards request --amount <n> --description "<desc>"     # request virtual card (single-use; subscriptions/--period coming soon)
lobstercash cards list                                           # list cards (includes card-id, phase, mandates) — used in both purchase flows to check for a reusable card
lobstercash cards reveal --card-id <id> --merchant-name "..." --merchant-url "https://..." --merchant-country US  # checkout credentials (used by the BYO browser flow, and for manual checkout)
```

The `purchase explore` and `purchase run` commands exist only when `browser-enabled: true` is configured — see the relevant purchase-flow reference for usage.

## Output Contract

- All commands produce human-readable output to stdout.
- Errors go to stderr as plain text.
- Exit 0 = success. Exit 1 = unexpected error. Exit 2 = wallet not set up (use `cards request` or `crypto request` to set up).

## Decision Tree

- Read [examples](references/examples.md) if the user wants to browse working examples, or has no specific task yet
- Read [status](references/status.md) if the user asks about agent status or payment readiness
- Read [balance](references/balance.md) if the user wants to check token balances
- Read [purchase-flow](references/purchase-flow.md) if the user wants to buy something online and `browser-enabled: true` — full flow using Lobster Cash's built-in browser automation
- Read [purchase-flow-byo](references/purchase-flow-byo.md) if the user wants to buy something online and `browser-enabled: false` — same flow but the agent drives the browser with its own tooling
- Read [purchase](references/purchase.md) if you need flag-level reference for `purchase explore` / `purchase run` (browser-enabled only)
- Read [cards request](references/cards-request.md) if the user wants to create a new virtual card for a purchase
- Read [crypto request](references/crypto-request.md) if the user wants to request USDC, top up their wallet, or fund a crypto operation
- Read [cards](references/cards.md) if the user needs to list existing cards, reveal credentials, or check whether a card can be reused for a purchase
- Read [send](references/send.md) if the user wants to send tokens to an address (Crypto Path)
- Read [x402](references/x402.md) if the user wants to pay for an API via x402 protocol (Crypto Path)
- Read [tx](references/tx.md) if the user needs to sign or submit a transaction from an external tool (Crypto Path)
- Read [setup](references/setup.md) if the user wants to link the agent to a wallet without making a purchase
- Read [agents](references/agents.md) if the user wants to register, list, or set the active agent

## Anti-Patterns

- **Skipping the browser availability check before an online purchase:** Don't assume which purchase flow applies. When the user wants to buy something online, always run `lobstercash config get browser-enabled` first (Section A) before deciding which purchase-flow reference to load. The flag determines whether to use `purchase explore` / `purchase run` or to drive the browser yourself with `cards reveal` for credentials.
- **Calling `purchase explore` / `purchase run` when `browser-enabled: false`:** Those commands require the built-in browser automation. If the flag is `false`, follow [references/purchase-flow-byo.md](references/purchase-flow-byo.md) instead.
- **Running crypto commands without checking status first:** Always run `lobstercash status` before `crypto send`, `crypto x402 fetch`, or `crypto tx create`. If the wallet isn't configured or has insufficient funds, the command will fail with a confusing error. Check first, fund if needed, then execute.
- **Running setup when the user wants to buy something:** If the user wants to make a purchase, don't run `setup` first — use `cards request` or `crypto request` which bundle setup automatically. Only use `lobstercash setup` when the user explicitly wants to link the agent to their wallet without buying anything.
- **Re-running setup when the agent is already configured:** If `lobstercash status` shows the wallet is already configured, do not generate a new setup session. The existing configuration is valid. Only start a fresh setup if the user explicitly tells you their current configuration is broken and needs to be regenerated.
- **Asking the user for info the CLI can fetch:** Check balance before sending. Check status before acting. Read command output before asking questions.
- **Running write commands in loops:** One attempt, read the result, then decide. Read operations (`crypto balance`, `status`, `examples`) are idempotent and safe to repeat. Write operations (`crypto send`, `cards request`) are not.
- **Ignoring terminal status:** A pending transaction is not a success. All write commands now wait for on-chain confirmation by default.
- **Polling for HITL approval:** When a command returns an approval URL, the user must tell you they approved. Do not auto-poll.
- **Running commands before registering an agent:** Always ensure an agent exists via `lobstercash agents list` before running any other command. If you need to work with a different agent, use `lobstercash agents set-active`.
- **Asking the user which chain to use:** Agents default to Base silently. Do not ask "which chain do you want?" at registration — just register on Base. Only pass `--network solana` if the user has explicitly told you they need Solana, or when the context clearly implies the agent must operate on Solana (e.g. they already hold USDC on Solana, or the integration they want is Solana-only). Chain is fixed per agent; switching later means registering a new one.
- **Recommending cards for crypto-only integrations:** If the integration only uses crypto, don't suggest a virtual card.
- **Requiring USDC for card-supported integrations:** Virtual cards are backed by credit cards, not USDC. Don't tell the user to "add funds" when the integration accepts cards.
- **Treating x402/send/tx as separate user flows:** They all go through the same Crypto Path. The only split is credit card vs crypto.
- **Suggesting `crypto request` or `cards request` when the user just wants to connect:** If the user wants to check balance, run a crypto command, or simply link their wallet — without topping up or creating a card — guide them through `lobstercash setup` first. Don't jump to `crypto request` or `cards request` unless the user actually wants to fund the wallet or make a purchase.
- **Jumping to readiness checks before showing options:** Show what's available first (via `examples`), then check payment readiness only when the user wants to try one.
- **Assuming an integration's payment method:** Never guess whether a flow uses cards or crypto. Run `lobstercash status` and read the payment methods output before choosing a path.
