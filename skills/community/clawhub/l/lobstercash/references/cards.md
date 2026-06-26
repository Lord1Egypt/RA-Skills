# Virtual Cards

Request, list, reveal credentials for checkout, and inspect virtual cards on the agent wallet.

## What virtual cards are

Virtual cards are temporary, scoped payment cards generated from the user's saved card on file using Visa Intelligent Commerce and Mastercard Agent Pay. They work like disposable debit cards with a fixed spending limit — the card cannot be charged beyond the amount the user approved when creating it.

Key properties:

- **Privacy-preserving:** The user's real card details (number, CVC, expiry) are never shared with the agent. The agent only ever sees the virtual card credentials, which are separate from the card on file.
- **Scoped balance:** Each virtual card has a hard spending cap set at creation time. Once that limit is reached, the card declines further charges. This protects the user from overspending.
- **Human approval required:** Creating a virtual card always requires the user to approve via a link. The agent cannot create or fund a card without explicit human consent.

**Naming:** The API calls these _order intents_; the CLI and plugin expose them as _virtual cards_. Each card has a stable id: `orderIntentId`. For `lobstercash cards reveal`, pass that value as `--card-id`.

---

## Requesting a new card

> **Note:** Subscription / recurring cards are **coming soon**. For now every card is single-use — request a fresh one per purchase. The `--period` flag still exists in the CLI but should be omitted until subscriptions ship.

### What you need before running

Two pieces of information — extract from context, do not ask if already clear:

- `amount`: maximum USD that can be spent on this virtual card (e.g. `25.00`). Other currencies will be supported soon.
- `description`: what the card will be used for (e.g. `"AWS credits"`).

If the user said "I need a card for $25 for AWS" you already have both. Do not ask about period today — it has no effect until subscription cards launch.

### Command

```
lobstercash cards request \
  --amount <amount> \
  --description "<description>"
```

`--period <weekly|monthly|yearly>` is reserved for the upcoming subscription cards feature; omit it for now.

### Reading the output

The output contains:

- The requested amount and description
- An approval URL the user must open to approve the card request

### After running

Show the approval URL to the user:
"To create this card I need your approval. Open this link:

[approvalUrl]

Come back here when you've approved it."

Do not proceed until the user confirms they have approved.

### After user approves

Run: `lobstercash cards list`.

Find the card with matching description (see `card-id=...` on each line). Report to user:
"Your card is ready"

And then proceed with what you were doing.

### If the command fails (exit code 1)

Show the error message from stderr.

### What NOT to do

- Do not retry automatically if the user says they declined.
- Do not explain how virtual cards work unless asked.

---

## Listing existing cards

This command shows card metadata (description, limit, phase, and card ID) — not payment credentials. To get the actual card number, CVC, and expiry for checkout, use `cards reveal` (see below) with the `card-id` from this output.

### Command

```
lobstercash cards list
```

### Reading the output

One line per card:

```
  <description>  $<amount> <currency> limit  [<phase>]  card-id=<orderIntentId>
```

Use `card-id` as `--card-id` when running `lobstercash cards reveal`. In OpenClaw, the same value is `orderIntentId` on each item in `lobster_order_intents` → `details.orderIntents`.

Possible phase values:

- `active` — card is ready to use; credentials can be revealed for checkout
- `requires-payment-method` — no valid card on file; the user must add or update their payment method at lobster.cash/dashboard before this card can activate
- `requires-verification` — the user's bank requires additional authentication (e.g. 3D Secure); they must complete verification in the browser at the approval link
- `expired` — card is no longer valid; the user needs to request a new one

### When to use

- After the user approves a card request — to confirm the card is `active` and get its `card-id`
- When the user asks "do I have any cards"
- To check the status of a specific card
- **Before creating a new card for a purchase** — always list first and check whether an existing card can be reused (see "Reusing an existing card" below). This is Step 3 of the buy flow in `SKILL.md`.

### Reporting to the user

List only `active` cards unless the user asks for all.
Say: "You have [n] active card(s): [description] with a $[amount] limit."

### Reusing an existing card

When you're about to create a new card for a purchase, run `cards list` first and check whether one already covers the purchase. Reusing a card avoids spamming the user with another approval link.

> **Note:** Cards are single-use today (subscription cards coming soon). A card you already charged successfully cannot be reused — request a new one. The `period` rule below is forward-looking for when subscriptions ship.

Each item carries these mandate fields:

- `phase` — only `active` is usable.
- `mandates[type=maxAmount].value` — the spending cap.
- `mandates[type=maxAmount].details.currency` — currency (default `USD`).
- `mandates[type=maxAmount].details.period` — currently always absent (single-use). Will be `weekly | monthly | yearly` when subscriptions launch.
- `mandates[type=description].value` — what the user approved it for.
- `mandates[type=prompt].value` — richer original natural-language request (when present).
- `mandates[type=consumer].details.email` — consumer email scope.

Do **not** match on:

- **Remaining balance** — only the cap is exposed; once recurring cards launch we won't be able to see what's already been spent in the current period. Trust the cap and let the merchant decline if exceeded.
- **Whether the card has been charged** — `cards list` doesn't expose charge history. If you (or a previous turn) already used the card for a purchase, treat it as spent and request a new one.
- `agentId` / `paymentMethodId` — internal bindings, not match signals.

A card is **usable for a given purchase** only when **all** of the following hold:

1. `phase === active`.
2. `maxAmount.value >= rounded total` (rounded up to the nearest $5).
3. `maxAmount.details.currency` matches the purchase currency.
4. The card hasn't already been used. Today every card is single-use, so any card already charged successfully is no longer usable. _(Coming soon: when subscription cards ship, `maxAmount.details.period` will need to match the cadence — single-use → no period; recurring → same period.)_
5. `description` (and `prompt` if present) is **semantically compatible** with the purchase. Don't reuse an "AWS credits" card for "enamel pins" — request a new card scoped to the new purpose. A generic description like "online shopping" can cover broader purchases — use judgment.

If none match, fall back to `cards request`.

---

## Revealing card credentials (checkout)

Use when the user needs the **full card number, CVC, and expiry** to complete a purchase (e.g. paste into a merchant checkout). Only works for cards in **`active`** phase.

### OpenClaw plugin

Use tool `lobster_card_reveal` with:

- `cardId` — same as `orderIntentId` from `lobster_order_intents` (`details.orderIntents[].orderIntentId`)
- `merchantName`, `merchantUrl`, `merchantCountryCode` (ISO 3166-1 alpha-2, e.g. `US`) — describe where the card will be used
- Optional `products` — array of `{ name, price, quantity }` if the API requires it

### CLI

```
lobstercash cards reveal \
  --card-id <orderIntentId> \
  --merchant-name "<name>" \
  --merchant-url "<https://...>" \
  --merchant-country <XX>
```

### What you need from context

Extract from the user or the purchase flow — do not invent merchant details:

- **Card id:** from `lobstercash cards list` (`card-id=...` on the line) or `lobster_order_intents` → `details.orderIntents[].orderIntentId`.
- **Merchant:** real store name, canonical site URL, and country code for that merchant.

### Reading the output

The command prints card number, expiration (month/year), CVC, and credential expiry time. Treat this output as highly sensitive.

### Security and UX

- Treat revealed values like a physical card: do not log them unnecessarily or paste into untrusted channels.
- Confirm the user is ready to check out before revealing.
- If reveal fails (e.g. wrong phase), re-check `lobstercash cards list` for `phase === active`.
