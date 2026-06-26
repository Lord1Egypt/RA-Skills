# Cards Request — Virtual Card for Purchases

Request a virtual card backed by the user's credit card. This is the fastest payment path — no USDC or wallet funding needed. If the wallet isn't configured yet, this command bundles setup automatically.

## Command

```bash
lobstercash cards request --amount <amount> --description "<description>" --period <period>
```

## What you need before running

Extract from context — do not ask if already clear:

- `amount`: how much to load in USD (e.g. `25.00`)
- `description`: what the card will be used for (e.g. `"AWS credits"`)
- `period`: billing period for the mandate — **required**, one of `weekly`, `monthly`, `yearly`. If the user doesn't specify, ask them.

If the user said "I need a card for $25 for AWS" you already have both.

## Reading the output

The output contains:

- `agentId`: the agent this card is for
- `amount`: the requested amount
- `period`: the billing period (`weekly`, `monthly`, or `yearly`)
- `description`: what the card is for
- `approvalUrl`: the URL the user must open to approve
- `setupSessionId`: present if wallet setup was bundled (first-time use)

## After running

Show the approval URL to the user:

> To create this card I need your approval. Open this link:
>
> [approvalUrl]
>
> Come back here when you've approved it.

Do not proceed until the user confirms they have approved.

## After user approves

Run `lobstercash cards list` to verify the card was created. Then proceed with the user's task — see `references/cards.md` for listing, revealing credentials, and checkout.

## Gotchas

- Virtual cards do NOT require USDC — they're backed by the user's credit card
- If the wallet isn't configured, setup is bundled automatically — do not run `lobstercash setup` first
- Only use this when the integration supports `card` payments — do not recommend for crypto-only integrations
- Write operation — do not retry automatically or if the user declines
