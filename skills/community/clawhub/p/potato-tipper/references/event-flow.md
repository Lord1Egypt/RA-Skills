# Follow → Tip event flow (debug reference)

This is a practical debugging reference for the **Tip-on-Follow** transaction.

## High-level

When a user gets a new follower and a tip is sent, you should expect a cascade of events across:
- LSP26 Follower Registry
- LSP7 $POTATO token
- Sender 🆙 (Universal Profile)
- Recipient 🆙 (Universal Profile)
- PotatoTipper contract

## Canonical order (from `LEARN.md`)

When a follow triggers a tip, events are emitted in this order:

0. `Follow` (LSP26) — emitted by the LSP26 Follower Registry
1. `OperatorAuthorizationChanged` (LSP7) — allowance decreases when PotatoTipper spends budget
2. `Transfer` (LSP7) — operator transfer from user 🆙 → follower 🆙
3. `UniversalReceiver` — on sender 🆙 (user), typeId = LSP7 "TokenSent"
4. `UniversalReceiver` — on recipient 🆙 (follower), typeId = LSP7 "TokenReceived"
5. `PotatoTipSent` — emitted by PotatoTipper
6. `UniversalReceiver` — on sender 🆙 (user), typeId = LSP26 "NewFollower"

## Practical debugging tips

- If you see (0) but not (2): the tip likely did not happen (eligibility/settings/budget failure).
- If (2) happens but (4) reverts: follower is not a valid 🆙 / does not implement LSP1 properly.
- If (2) reverts: likely budget insufficient or token/operator permissions missing.
- PotatoTipper returns human-readable `returnedData` in the sender 🆙 `UniversalReceiver` event; use that message to classify errors.

