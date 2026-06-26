# Browser Flow - Glovo

Use this flow when Glovo is being controlled through the user's real browser session.

## Read First

1. Confirm the active tab is actually Glovo.
2. Read the visible title, URL, account state, and active address.
3. If the address is missing, solve that before browsing stores.

## Main Flow

1. Home:
   - verify the account is signed in
   - verify the active city or address state
   - decide whether the user wants food, groceries, pharmacy, or convenience
2. Discovery:
   - browse category cards or use search
   - compare store ETA, minimum, fee, and promo state
   - open only the most relevant 1-3 stores
3. Store:
   - verify store name, ETA, fees, and any minimum order
   - read menu sections before adding items
   - if the store is closed or low-signal, back out early
4. Cart:
   - inspect existing cart state before changing it
   - add or edit only what the user asked for
   - re-check substitutions, notes, and promo effects after every major edit
5. Checkout:
   - read the full summary page
   - stop for explicit confirmation before the final live order action

## Verification Loop

- After every navigation, re-read the page or capture a screenshot.
- Never assume a click worked because the tab stayed open.
- If the visible state is ambiguous, refresh the read before the next action.

## Practical Notes

- Glovo often gates meaningful browsing behind an active address.
- The real total can change after delivery fee, service fee, promo, and tip.
- A saved browser session is useful, but it also raises the risk of accidental live actions.
