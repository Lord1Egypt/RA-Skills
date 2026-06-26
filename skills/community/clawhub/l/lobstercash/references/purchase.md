# Purchase — `purchase explore` and `purchase run` reference

Reference for the two CLI commands that drive Browser Use checkout.

For the end-to-end purchase flow (when to call which command, how to size a card, how to fork on existing cards), see Section A "Buy something online" in [`SKILL.md`](../SKILL.md). This file is a pure flag and behavior reference.

## `lobstercash purchase explore`

Free price-discovery pass. Browser opens, finds the product on the merchant's site, calculates the total (incl. shipping/tax), and parks on the cart. The browser session stays alive so a follow-up `purchase run --explore-id` picks up immediately.

```bash
lobstercash purchase explore \
  --description "<full natural-language request>" \
  --merchant-country <XX>
```

### Flags

- `--description` (required) — full natural-language request: product, merchant or merchant URL, address, contact, and any user preferences. See [Writing a good description](#writing-a-good-description) below.
- `--merchant-country` (required) — ISO 3166-1 alpha-2 country code for the browser proxy region (e.g. `US`, `GB`, `DE`).
- `--explore-id <id>` — resume an existing session to poll status or supply an answer to a `needs_user_input` prompt.
- `--answer "<text>"` — used together with `--explore-id` to answer a `needs_user_input` question.

## `lobstercash purchase run`

Runs the automated checkout. Two modes:

- **With `--explore-id`** (preferred): reuses the parked browser session from a prior `purchase explore`. `--merchant-name`, `--merchant-url`, and `--merchant-country` are read from the explore record and are not required.
- **Without `--explore-id`** (single-phase): see [Single-phase purchase](#single-phase-purchase-no-explore) below — `--merchant-name`, `--merchant-url`, and `--merchant-country` are required.

```bash
lobstercash purchase run \
  --card-id <card-id> \
  --explore-id <explore-id> \
  --description "<same description as explore>" \
  --max-total <rounded>
```

### Flags

- `--card-id` (required) — the order intent ID of the virtual card to charge. From `lobstercash cards list` (`card-id=...`).
- `--explore-id <id>` — reuse a prior `purchase explore` session. When set, merchant flags become optional.
- `--description` (required) — same description used in `purchase explore` (or a superset). The server uses it verbatim.
- `--max-total "<amount>"` — maximum total including tax and shipping. **The order is placed automatically as long as the cart stays at or under this number** — there is no review-and-confirm step. Decline if the cart exceeds this.
- `--constraint "<text>"` — repeatable extra constraint (e.g. `--constraint "no third-party seller"`).
- `--shipping-json '{...}'` / `--contact-json '{...}'` — typed shipping/contact context. Usually unnecessary because the description carries this info.
- `--merchant-name "<name>"`, `--merchant-url "<https://...>"`, `--merchant-country <XX>` — required only when `--explore-id` is **not** set.
- `--purchase-id <id>` — resume an existing run session to poll status or supply an answer.
- `--answer "<text>"` — used together with `--purchase-id` to answer a `needs_user_input` question.

## Single-phase purchase (no explore)

If you already know the exact price and the canonical merchant URL, you can call `purchase run` directly without `--explore-id`:

```bash
lobstercash purchase run \
  --card-id <orderIntentId> \
  --merchant-name "<merchant name>" \
  --merchant-url "https://merchant.com" \
  --merchant-country <XX> \
  --description "<full purchase request and every known user preference>"
```

In this mode `--merchant-name`, `--merchant-url`, and `--merchant-country` are required because there is no prior explore record to read them from.

## Local development mock card

When the web app is running with `NODE_ENV=development`, you can pass `--card-id dev-mock-card` to bypass Crossmint card credentials and inject a non-chargeable test card:

```bash
lobstercash purchase run \
  --card-id dev-mock-card \
  --explore-id <explore-id> \
  --description "Test checkout automation against local mock card." \
  --max-total 50
```

The mock card is for local browser automation only. Real merchants will not charge it and may reject it.

## Writing a good description

The `--description` is authoritative — Browser Use reads it verbatim. Pack everything into one natural-language string:

- product request, merchant, budget, quantity
- shipping address, email, phone (if available)
- size, color, fit, brand, material, or other variant choices
- delivery constraints and shipping preferences
- previous answers from the user
- exclusions like "no subscription" or "avoid third-party sellers"

Example:

```bash
lobstercash purchase explore \
  --description "Buy the best-rated black athletic crew socks on Amazon, size M, one pack only, no subscription. Ship to: Jane Doe, 500 5th Ave, New York NY 10110, US. Email: jane@example.com." \
  --merchant-country US
```

## Resuming and polling sessions

Both commands return a session ID (`exploreId` or `purchaseId`) and may return one of three non-terminal statuses (see [Output statuses](#output-statuses)). The browser session stays alive in the background between calls.

To **answer a `needs_user_input` prompt**, ask the user the returned question (and any options), then resume the same session with `--answer`:

```bash
# During explore:
lobstercash purchase explore --explore-id <id> --answer "<user answer>"

# During run:
lobstercash purchase run --purchase-id <id> --answer "<user answer>"
```

Required-choice prompts can repeat. Never invent answers.

To **poll a `running` session**, re-run the command with the ID and no `--answer`:

```bash
lobstercash purchase explore --explore-id <id>
lobstercash purchase run --purchase-id <id>
```

## Output statuses

- `running` — Browser Use is still working. Re-run the command with the session ID to poll.
- `needs_user_input` — agent reached a required choice it cannot make on its own (size, paid shipping, missing field, etc.). Ask the user and resume with `--answer`.
- `completed`
  - `explore`: price found and the browser is parked on the cart, ready to be reused by `purchase run --explore-id`.
  - `run`: order placed (or the cart was over `--max-total` and the agent declined — check the result summary).
- `failed` — report the failure reason and ask the user how to proceed.

## Explore session expiry fallback

If the explore session expires between phases (rare), `purchase run --explore-id` falls back to a fresh browser session and uses the discovered product URL from the explore record to navigate directly. The purchase still works, just slightly slower.
