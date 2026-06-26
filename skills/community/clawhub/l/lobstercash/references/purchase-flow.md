# Buy something online (browser-automated purchase flow)

This reference describes the end-to-end flow for buying products online with a virtual card and Lobster Cash's built-in Browser Use automation. It applies when **`browser-enabled: true`** for this CLI install (see [SKILL.md](../SKILL.md) Section A). If `browser-enabled: false`, follow [purchase-flow-byo.md](purchase-flow-byo.md) instead — same end-to-end flow, but you drive the merchant browser yourself.

Use when the user wants to purchase a product, subscription, domain, or any item from an online store. Purchases are **always browser-automated** via `purchase run` — Browser Use navigates the merchant's site, fills the checkout form, and stops at final review (or submits, when explicitly authorized).

The flow is: discover the real product and price first, then size a virtual card to that price (or reuse an existing one), then run the automated checkout.

## Step 1: Gather info from the conversation

Check what you already know from prior turns before asking:

- shipping address
- contact email
- phone (if the merchant might require it)
- product preferences (size, color, brand, quantity, exclusions)

Only ask the user for fields you don't already have. If they say a field isn't needed (e.g. "no phone" or "digital product, no address"), believe them and skip it. Never re-ask for info already in the conversation.

## Step 2: Discover the product and price (`purchase explore`)

**Ensure the wallet is set up first.** `purchase explore` and `purchase run` require an active wallet session and will exit with code 2 if one isn't configured — unlike `cards request` / `crypto request`, they do **not** bundle setup. Run `lobstercash status`:

- **Wallet configured** → continue.
- **Wallet not configured** → run `lobstercash setup`, share the approval URL with the user, and wait for them to confirm they approved before continuing. Don't try to bundle setup via `cards request` here — at this point you don't yet know the price, so you can't size the card correctly.

Pack everything into one natural-language `--description` and run explore. Share the live view URL with the user so they can watch.

```bash
lobstercash purchase explore \
  --description "<product, merchant or URL, shipping address, email, preferences>" \
  --merchant-country <XX>
```

Handle the response:

- `completed` → record `exploreId` and the discovered total, move on to Step 3.
- `needs_user_input` → ask the user the returned question, resume with `--explore-id <id> --answer "..."`.
- `running` → re-poll with `--explore-id <id>`.

**Never invent product URLs or category paths from training data.** Explore navigates the merchant's UI for you — that's the whole point. If the user didn't specify a merchant, do a web search first to ground the description in a real one (e.g. "best running socks to buy online" or "running socks site:nike.com").

For full flag list, description-writing guidance, resume/poll syntax, and output status definitions, see [purchase reference](purchase.md).

## Step 3: Check for an existing usable card (fork)

Before creating a new card, list current cards and look for one that already covers this purchase.

```bash
lobstercash cards list
```

> **Note:** Subscription / recurring cards are coming soon — for now every card is single-use. The matching rules below already account for this; period-based matching will become relevant once subscriptions ship.

Each card (order intent) carries these fields you can compare against:

- `phase` — only `active` is usable
- `mandates[type=maxAmount].value` — the spending cap (in `details.currency`, default USD)
- `mandates[type=maxAmount].details.period` — currently always absent (single-use). Will be `weekly | monthly | yearly` when subscriptions launch.
- `mandates[type=description].value` — what the user approved the card for (e.g. "AWS credits", "RHCP enamel pins")
- `mandates[type=prompt].value` — original natural-language request (richer context than description)
- `mandates[type=consumer].details.email` — consumer email scope (only matters if multi-user)

Fields **NOT** to rely on:

- **Remaining balance** — `cards list` only exposes the limit, not how much has been spent. Once subscription cards ship we won't be able to tell if this period's budget is already drained; trust the limit and let the merchant decline if exceeded.
- **Whether the card has already been charged** — single-use cards can't be reused once they've been charged successfully, but `cards list` doesn't expose charge history. If the card looks unused (no purchase you initiated against it), assume it's available; otherwise request a new one.
- `agentId` / `paymentMethodId` — internal bindings, not user-facing match signals.

A card is **usable for this purchase** when **all** of the following are true:

1. `phase === active`
2. `maxAmount.value >= rounded total` (rounded up to the nearest $5)
3. `maxAmount.details.currency` matches the purchase currency (typically `USD`)
4. The card hasn't already been used. Today every card is single-use, so a card you (or a previous turn) already charged successfully is no longer usable. _(Coming soon: when subscription cards launch, `maxAmount.details.period` will need to match the requested cadence — single-use purchase → no period; recurring purchase → same period.)_
5. `description` (and `prompt` if present) is **semantically compatible** with the purchase. The user approved the card for a specific purpose — do not reuse a card whose description targets a different merchant or product category. Example: an existing "AWS credits" card must not be reused for "RHCP enamel pins". A generic description like "online shopping" can cover broader purchases — use judgment.

Fork:

- **Match found** → skip Step 3b and Step 4. Reuse its `card-id` and jump straight to **Step 5**. Tell the user briefly: "Reusing your existing $X card for [description]."
- **No match** → continue to Step 3b.

See [cards reference](cards.md) for the full `cards list` output format and field semantics.

## Step 3b: Request a new virtual card sized to the discovered total

Round the discovered total **up** to the nearest $5 so a small price drift at checkout doesn't decline the card (e.g. $47.23 → $50, $31.75 → $35). Tell the user the rounded amount and why.

```bash
lobstercash cards request --amount <rounded> --description "<short product name>"
```

Cards are currently single-use only. **Subscription / recurring cards are coming soon** — when they ship you'll be able to add `--period <weekly|monthly|yearly>` for recurring purchases. Until then, omit `--period` (or rely on the default) and request a fresh card per purchase.

This command bundles wallet setup if needed. See [cards request reference](cards-request.md) for output format.

## Step 4: Get user approval

The `cards request` command outputs an `approvalUrl`. Show it to the user:

> To create this card I need your approval. Open this link:
>
> [approvalUrl]
>
> Come back here when you've approved it.

**Do not proceed until the user confirms they approved.** Do not poll. After they confirm, run `lobstercash cards list` once to verify the new card is `active`, then continue.

## Step 5: Complete the purchase (`purchase run`)

Reuse the explore session — the browser is already parked on the cart, so the purchase agent picks up immediately without re-searching.

```bash
lobstercash purchase run \
  --card-id <card-id> \
  --explore-id <explore-id> \
  --description "<same description as explore>" \
  --max-total <rounded>
```

Share the live view URL with the user so they can watch the checkout. The agent will place the order automatically as long as the cart total stays at or below `--max-total`. Size `--max-total` to match what the user has approved.

Handle the response the same way as explore: `completed` → done; `needs_user_input` → ask and resume with `--purchase-id <id> --answer "..."`; `running` → re-poll with `--purchase-id <id>`.

For all run flags (`--constraint`, `--shipping-json`, `--contact-json`), the single-phase fallback (no `--explore-id`), and local `dev-mock-card` testing, see [purchase reference](purchase.md).

## Browser-related commands (Quick Reference)

```bash
lobstercash purchase explore --description "<...>" --merchant-country <XX>                        # discover product + price (Step 2)
lobstercash purchase run --card-id <id> --explore-id <id> --description "<...>" --max-total <n>   # automated browser checkout (Step 5)
lobstercash cards reveal --card-id <id> --merchant-name "..." --merchant-url "https://..." --merchant-country US  # checkout credentials (manual sites only — not part of the standard buy flow)
```

## Browser-related references

- Read [purchase](purchase.md) for full flag reference, single-phase fallback, dev-mock-card, description-writing tips, and resume/poll syntax
- Read [cards request](cards-request.md) for creating a new virtual card for a purchase (Step 3b)
- Read [cards](cards.md) for listing existing cards and checking whether one can be reused (Step 3)

## Anti-patterns (browser flow specific)

- **Running `purchase explore` / `purchase run` before the wallet is set up:** Both purchase commands require an active wallet session and exit with code 2 otherwise — they do **not** bundle setup. Always run `lobstercash status` first; if the wallet isn't configured, run `lobstercash setup` and wait for user approval before calling `purchase explore`. (`cards request` and `crypto request` are different — they _do_ bundle setup, so don't run `setup` separately ahead of those.)
- **Hallucinating product URLs or paths:** Never guess URLs beyond the root domain — `/w/socks`, `/category/socks`, `/shop/socks` are all guesses, and URL structures change. Don't bake guessed paths into the `purchase explore --description`. Either give explore the merchant homepage (e.g. `nike.com`) and let Browser Use navigate the site's own UI, or ground the description with a real URL pulled from web search results.
- **Placing orders without user authorization:** `purchase run` always submits the order if the cart stays at or under `--max-total`, with no human approval at the review screen. Don't call it until the user has explicitly authorized this purchase, and size `--max-total` to match what they approved — it's the only guard against unexpected charges.
- **Skipping `purchase explore` and going straight to `purchase run`:** Always discover the real product and price first so you can size the card to the actual total. The single-phase `purchase run` fallback (no `--explore-id`) only applies when the user has already given you the exact price and a real merchant URL — see [purchase reference](purchase.md).
- **Requesting a new card without checking `cards list` first:** Always run `lobstercash cards list` after `purchase explore` and check whether an `active` card already covers this purchase (matching amount, currency, period, and purpose — see Step 3). Reusing a usable card avoids spamming the user with another approval link.
- **Reusing a card whose description doesn't fit the purchase:** The user approved each card for a specific purpose. Don't reuse an "AWS credits" card to buy enamel pins — request a new card scoped to the new purpose instead.
- **Forgetting to share the live view URL:** Both `purchase explore` and `purchase run` return a live view URL. Always pass it to the user so they can watch the browser, especially before they confirm a final-review screen or answer a `needs_user_input` prompt.
- **Guessing answers to `needs_user_input`:** When `purchase explore` or `purchase run` returns `needs_user_input`, the agent has reached a required choice it can't make on its own (size, paid shipping speed, missing address field, etc.). Ask the user with the returned question and options, then resume the _same_ session with `--explore-id` / `--purchase-id` and `--answer`. Never invent an answer.
