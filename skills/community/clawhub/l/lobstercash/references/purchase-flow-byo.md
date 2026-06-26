# Buy something online — bring-your-own browser flow

This is the purchase flow when **`browser-enabled: false`** (see [SKILL.md](../SKILL.md) Section A). It is the same end-to-end flow as [purchase-flow.md](purchase-flow.md), with one difference: **you (the agent) drive the merchant browser using whatever browser-automation tooling you already have available** in this environment (your IDE's browser tool, an MCP browser server, OpenClaw, Playwright/Puppeteer access, etc.). Lobster Cash still provides the virtual card, the user-approval flow, and `cards reveal` for credentials at checkout — it just doesn't drive the browser.

If you have **no** browser-automation tooling available in this environment, stop and offer to run the checkout manually with the user — you'll get the card credentials with `cards reveal` and walk them through entering them at the merchant's checkout page themselves.

The flow: discover the real product and price first (with your browser), size a virtual card to that price (or reuse an existing one), get user approval, then complete checkout (with your browser, using credentials from `cards reveal`).

## Step 1: Gather info from the conversation

Check what you already know from prior turns before asking:

- shipping address
- contact email
- phone (if the merchant might require it)
- product preferences (size, color, brand, quantity, exclusions)

Only ask the user for fields you don't already have. If they say a field isn't needed (e.g. "no phone" or "digital product, no address"), believe them and skip it. Never re-ask for info already in the conversation.

## Step 2: Discover the product and price (your browser tool)

Use **your own browser tooling** to navigate the merchant's site, locate the product the user wants, add it to the cart (or get to a quote/total page), and capture the **final total** including tax and shipping. You need a real, current total so the next step can size the virtual card correctly.

While you work, share progress with the user — what site you're on, what you found, when you've reached the cart total. They should be able to follow along.

What you must come away with before moving on:

- The product (name, variant/size/color if applicable, quantity)
- The merchant (real store name, canonical URL, country)
- The cart total in USD (or the purchase currency)
- A way to resume checkout later — keep your browser session/tab parked on the cart, or note the cart URL / re-buildable cart so you can return to it after card approval

If you don't know which merchant the user wants, do a web search first to ground yourself in a real merchant — don't guess URLs from training data. Same rule as the native flow: navigate the site's UI, don't bake guessed paths like `/category/socks` into anything.

If the merchant requires the user to sign in or answer a question that you can't decide on your own (size, paid shipping speed, etc.), pause and ask the user — don't invent answers.

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

- **Remaining balance** — `cards list` only exposes the limit, not how much has been spent.
- **Whether the card has already been charged** — single-use cards can't be reused once they've been charged successfully, but `cards list` doesn't expose charge history. If the card looks unused (no purchase you initiated against it), assume it's available; otherwise request a new one.
- `agentId` / `paymentMethodId` — internal bindings, not user-facing match signals.

A card is **usable for this purchase** when **all** of the following are true:

1. `phase === active`
2. `maxAmount.value >= rounded total` (rounded up to the nearest $5)
3. `maxAmount.details.currency` matches the purchase currency (typically `USD`)
4. The card hasn't already been used. Today every card is single-use, so a card you (or a previous turn) already charged successfully is no longer usable.
5. `description` (and `prompt` if present) is **semantically compatible** with the purchase. Don't reuse a card whose description targets a different merchant or product category.

Fork:

- **Match found** → skip Step 3b and Step 4. Reuse its `card-id` and jump straight to **Step 5**. Tell the user briefly: "Reusing your existing $X card for [description]."
- **No match** → continue to Step 3b.

See [cards reference](cards.md) for the full `cards list` output format and field semantics.

## Step 3b: Request a new virtual card sized to the discovered total

Round the discovered total **up** to the nearest $5 so a small price drift at checkout doesn't decline the card (e.g. $47.23 → $50, $31.75 → $35). Tell the user the rounded amount and why.

```bash
lobstercash cards request --amount <rounded> --description "<short product name>"
```

Cards are currently single-use only. Subscription / recurring cards are coming soon — until then, omit `--period` (or rely on the default) and request a fresh card per purchase.

This command bundles wallet setup if needed. See [cards request reference](cards-request.md) for output format.

## Step 4: Get user approval

The `cards request` command outputs an `approvalUrl`. Show it to the user:

> To create this card I need your approval. Open this link:
>
> [approvalUrl]
>
> Come back here when you've approved it.

**Do not proceed until the user confirms they approved.** Do not poll. After they confirm, run `lobstercash cards list` once to verify the new card is `active`, then continue.

## Step 5: Complete the purchase (your browser tool + `cards reveal`)

Now the card is ready and the cart is parked. Two sub-steps:

### 5a — Reveal the card credentials

```bash
lobstercash cards reveal \
  --card-id <card-id> \
  --merchant-name "<merchant name>" \
  --merchant-url "<canonical merchant URL>" \
  --merchant-country <XX>
```

This prints the card number, expiry month/year, and CVC for that specific merchant. **Treat the output as highly sensitive.** Do not log or paste it anywhere outside of the merchant's checkout form. Do not share these details with the user; just use them yourself in the browser.

See [cards reveal section in cards reference](cards.md#revealing-card-credentials-checkout) for full flag details and security notes.

### 5b — Drive checkout with your browser tool

Return your browser to the parked cart (or rebuild it from the cart URL captured in Step 2) and complete the checkout form using the user's shipping/contact info from Step 1 and the revealed card details from Step 5a.

**Stop before final submit.** Reach the order-review screen and pause. Then ask the user to confirm: "Cart total is $X. Card ending in <last 4>. Shipping to <address>. Ready for me to place the order?" Only submit once the user has explicitly authorized this exact submission.

If the merchant total at checkout exceeds the card's hard cap, the card will decline. Don't try to charge more than the card limit — request a new card sized to the new total instead.

If the merchant asks for something you can't answer on your own (size choice, shipping option that costs extra, missing address field), pause and ask the user. Don't invent answers.

After the order is submitted, share the confirmation details (order number, total charged, ETA if shown) with the user.

## Anti-patterns (BYO browser flow)

- **Calling `purchase explore` or `purchase run`:** They require `browser-enabled: true`. In this flow you drive the browser yourself.
- **Skipping price discovery:** Always discover the real product and price (Step 2) before requesting a card. Without it you can't size the card and the merchant will decline.
- **Hallucinating product URLs or paths:** Same rule as the native flow — never guess URLs beyond the root domain. Either start from the merchant homepage and let your browser tool navigate the site's own UI, or ground yourself in a real URL pulled from web search results.
- **Placing orders without user authorization:** The card's hard cap is a backstop, not a green light. Always stop at the order-review screen and ask the user to confirm before submitting.
- **Requesting a new card without checking `cards list` first:** Always run `lobstercash cards list` after Step 2 and check whether an `active` card already covers this purchase. Reusing a usable card avoids spamming the user with another approval link.
- **Reusing a card whose description doesn't fit the purchase:** The user approved each card for a specific purpose. Don't reuse an "AWS credits" card to buy enamel pins — request a new card scoped to the new purpose.
- **Sharing revealed card details with the user or logs:** `cards reveal` output is sensitive. Use the values in the merchant's checkout form, then forget them. Don't echo them back to the user.
- **Guessing merchant questions you can't answer:** Same as the native flow — when you hit a required choice you can't make on your own (size, shipping option, missing address field), pause and ask the user. Don't invent answers.
- **Pretending you have a browser tool when you don't:** If this environment has no browser-automation tooling available, don't bluff your way through Step 2 or Step 5. Stop and offer the user a manual checkout instead — get the credentials with `cards reveal` and walk them through entering them at the merchant's checkout themselves.
