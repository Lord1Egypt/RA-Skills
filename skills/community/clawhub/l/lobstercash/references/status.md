# Status

Check agent setup state, wallet balances, and virtual cards in one call. Auto-triggers wallet setup if needed.

## Command

```bash
lobstercash status
```

## Output varies by state

The command returns different fields depending on how far along the setup is.

### Not linked (`authorized: false`)

The agent hasn't been linked to a human's acount yet. Output only includes `agentId`, `wallet.configured: false`, and `authorized: false`. No balances, cards, or `dashboardUrl`.

Next step: run `lobstercash cards request --amount <n> --description "<desc>"` or `lobstercash crypto request --amount <n> --description "<desc>"` — both handle wallet linking automatically.

### Linked (`authorized: true`)

The agent is linked to a human's account. Output includes all fields:

- `wallet.configured: true`
- `wallet.address` — the agent's wallet address on its chain (`0x…` on Base, base58 on Solana)
- `authorized: true`
- `balances` — token balances (USDC plus the chain's native token)
- `cards` — virtual cards with phase (`active`, `requires-payment-method`, etc.)
- `ready` — `true` if the agent can pay (has USDC > 0 OR an active virtual card)
- `dashboardUrl` — link for the user to manage payments

## Gotchas

- Virtual cards do not require USDC — they are backed by the user's credit card. Don't tell the user to "add funds" when using cards.
- Only crypto operations (`crypto send`, `crypto x402 fetch`) require a configured wallet with USDC.
- Always show the actual `dashboardUrl` — never say "go to the dashboard" without the link.
