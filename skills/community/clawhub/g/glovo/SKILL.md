---
name: Glovo
slug: glovo
version: 1.0.0
homepage: https://clawic.com/skills/glovo
description: Navigate Glovo in a live browser session to compare stores, manage carts, and reach checkout safely before ordering.
changelog: Initial release with live-browser ordering flow, checkout guardrails, and issue recovery for Glovo orders.
metadata: {"clawdbot":{"emoji":"🛵","requires":{"bins":[],"config":["~/glovo/"]},"os":["darwin","linux","win32"],"configPaths":["~/glovo/"]}}
---

## When to Use

User needs Glovo specifically, not generic delivery advice. Use this when the task depends on the user's real Glovo session, saved addresses, live store availability, current promos, cart state, groceries, pharmacy, or food ordering inside Glovo.

Choose this skill when the next step is to browse stores, compare delivery options, prepare a cart, verify checkout details, or help recover from Glovo-specific issues such as unavailable items, address friction, or late delivery. If the task is platform-agnostic, route to `food-delivery`.

## Architecture

Memory lives in `~/glovo/`. If `~/glovo/` does not exist, run `setup.md`. See `memory-template.md` for structure and starter fields.

```text
~/glovo/
|-- memory.md       # Activation defaults, browser mode, and ordering boundary
|-- addresses.md    # Approved delivery addresses and area caveats
|-- stores.md       # Preferred stores, cuisines, fees, and repeat winners
|-- orders.md       # Recent orders, substitutions, and issue history
`-- incidents.md    # Payment failures, missing items, support outcomes, and fixes
```

## Quick Reference

Load only the smallest file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Live browser navigation flow | `browser-flow.md` |
| Checkout safety and confirmation rules | `checkout-guardrails.md` |
| Failure patterns and recovery order | `issue-recovery.md` |

## Requirements

- A browser session where the user is already signed in to Glovo is strongly preferred.
- Any browser reading, clicking, typing, or screenshot capture must use a host-provided browser automation path that the user has already approved in the current environment.
- Saved addresses, payment methods, and account credentials should stay inside the user's own browser or Glovo app.
- Explicit approval is required before controlling the user's daily browser session, changing delivery addresses, clearing or replacing an existing cart, or placing any live order.
- If the skill activates without explicit current-thread approval for browser control, stay in planning mode and do not inspect the live session.

If live Glovo access is unavailable, stay in planning mode and prepare the exact browse or checkout steps instead of pretending the order is ready.

## Control Modes

This skill supports three levels of intervention:

- **Browse mode**: inspect home, categories, stores, ETAs, minimums, fees, and promos without changing cart state.
- **Draft cart mode**: open stores and prepare a candidate cart when the user clearly asked to build an order draft.
- **Live checkout mode**: review checkout details and place the order only after explicit confirmation in the current conversation.

Do not blur the boundary between browsing and ordering. A live Glovo session has real addresses, real payment methods, and real purchase consequences.

## Data Storage

Persistent local notes in `~/glovo/` are optional. If the user does not want local storage, operate statelessly and do not create or write that folder.

When local notes are allowed, keep only durable operating context in `~/glovo/`:
- whether the skill may reuse the daily browser profile or should stay read-only
- preferred addresses, neighborhoods, and delivery caveats approved by the user
- favorite stores, order patterns, and substitution preferences
- issue history worth reusing, such as stores that frequently miss items or promos that never apply

Do not store account passwords, payment card data, one-time verification codes, or full receipts with sensitive payment details.

## Core Rules

### 1. Reuse the Real Session Only When the User Actually Wants That
- Prefer the user's already signed-in Glovo browser session when live state matters.
- This skill does not grant browser access by itself; it only uses an already-approved browser control path from the host environment.
- Ask before activating, switching tabs, typing, clicking, or capturing screenshots from the daily browsing profile.
- If the user only wants strategy, stay out of the real session and explain the flow instead.

### 2. Lock the Delivery Address Before Comparing Stores
- Glovo availability, ETA, fees, and promos depend on the active address.
- If no address is set, solve that first before treating any store card or category as meaningful.
- Do not assume an address is correct because the user is logged in; verify what Glovo is actively using.

### 3. Read the Store State Before Touching the Cart
- Confirm store name, delivery ETA, minimum order, delivery fee, service fee, and promo state before adding items.
- Re-read the page after every navigation or major action.
- If the cart already contains items, stop and clarify whether to preserve, edit, or replace it.

### 4. Separate Drafting From Live Purchase
- Building a candidate cart is not the same as placing an order.
- Before any live checkout step, summarize the store, items, substitutions, address, ETA, fees, total, tip, payment method, and notes.
- Place the final order only after explicit approval in the current thread.

### 5. Compare Like for Like, Not Just Headline Price
- For Glovo ordering decisions, compare item totals, fees, ETA, minimums, promo eligibility, and substitution risk together.
- A cheaper subtotal can still be worse after fees or slower delivery.
- If the user wants optimization, show the real total and the tradeoff, not only the food price.

### 6. Keep Memory About Preferences, Not Secrets
- Save reusable address choices, favorite stores, cuisine habits, substitution preferences, and known problem stores.
- Keep short notes about what worked, what arrived late, and what needed support.
- Never store full payment data, raw support transcripts, or copied personal verification details.

### 7. Handle Post-Order Issues as Their Own Workflow
- Missing items, wrong items, courier delay, cancellation, and refund paths need their own verification loop.
- Start with the exact order state visible in Glovo before proposing compensation or support steps.
- Record the durable lesson after the issue is resolved so the same store or pattern is easier to handle next time.

## Glovo Traps

- Treating the home page as actionable before an address is set -> store availability and fees are unreliable.
- Opening a live browser session and clicking immediately -> wrong tab, wrong cart, or wrong address.
- Assuming the cheapest visible store card is the best option -> fees, ETA, and minimum order can reverse the decision.
- Modifying a non-empty cart without checking whether it contains unfinished items -> accidental cart damage.
- Applying coupons or replacing substitutions at the last second without rechecking totals -> order summary drift.
- Treating the final checkout button as reversible -> it can create a real paid order.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://glovoapp.com | Addresses, search terms, cart state, checkout data, and account session cookies inside the user's own browser session | Browsing, cart preparation, checkout, and issue handling |
| Glovo app deep links or mobile handoff opened by the user | Store, cart, and checkout intent data | Native app continuation when browser flow is not enough |

No other data should be sent externally unless the user explicitly opens additional payment, map, or support surfaces during the Glovo workflow.

## Security & Privacy

**Data that leaves your machine:**
- addresses and search terms entered into Glovo
- cart and checkout data sent through the user's Glovo session
- support or issue details the user explicitly submits to Glovo

**Data that stays local:**
- optional Glovo operating notes in `~/glovo/`, only if the user wants persistent memory
- preferences, address labels, and known-good store patterns approved by the user

**This skill does NOT:**
- ask for Glovo passwords in chat
- store payment card numbers or one-time verification codes
- place live orders without explicit confirmation in the current thread
- claim a cart or checkout is correct without re-reading the actual Glovo page

## Trust

By using this skill, data is sent to Glovo through the user's own browser or app session.
Only install and run it if you trust Glovo with your address, cart, payment, and order data.

## Scope

This skill ONLY:
- helps control Glovo ordering safely through a live browser or app handoff
- structures browse, draft-cart, live-checkout, and issue-recovery workflows
- keeps durable notes for addresses, stores, preferences, and recurring issues

This skill NEVER:
- claim a live Glovo state it cannot verify
- promise stock, ETA, or promo validity without checking the current page
- store secrets or raw payment data in its own memory files
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `food-delivery` - Broader ordering logic when the user is not locked to Glovo.
- `maps` - Validate delivery geography, area fit, and route realism around the chosen address.
- `safari` - Control the user's real Safari session when Glovo is open there.
- `applescript` - Build safer macOS browser-control snippets when the workflow needs exact Apple Events.
- `shopping` - Compare fees, promos, and real checkout value instead of impulse ordering.

## Feedback

- If useful: `clawhub star glovo`
- Stay updated: `clawhub sync`
