---
name: pg-status
description: Use when checking ProxyGate status — balance, usage, listings, tunnel health, earnings, seller profile, or job status. Make sure to use this skill whenever someone mentions "check balance", "proxygate status", "my usage", "my earnings", "what's my balance", "how much have I spent", "my listings", "settlement history", or wants any kind of status overview.
---

# ProxyGate Status

Quick status checks for buyers and sellers.

## Buyer status

```bash
proxygate balance                              # USDC balance (total, pending, available, cooldown)
proxygate usage                                # recent request history
proxygate usage -s weather-api -l 10           # filtered by service, last 10
proxygate usage --from 2026-03-01 --json       # date range, machine-readable
proxygate settlements -r buyer                 # cost breakdown (total requests, cost, fees, net)
proxygate settlements -s maps-api --from 2026-03-01   # filtered
```

## Seller status

```bash
proxygate listings list                        # active listings (ID, service, status, RPM, price)
proxygate listings list --table                # human-readable table
proxygate listings docs <id>                   # view docs for a listing
proxygate settlements -r seller                # earnings (total requests, earnings, fees, net payout)
proxygate settlements --from 2026-03-01 --to 2026-03-14
proxygate balance                              # earned balance
```

## Job status

```bash
proxygate jobs list --status claimed           # jobs you've claimed
proxygate jobs get <job-id>                    # full job details + submission status
```

## SDK

```typescript
import { ProxyGateClient } from '@proxygate/sdk';

const client = await ProxyGateClient.create({
  keypairPath: '~/.proxygate/keypair.json',
});

const { balance, available, pending_settlement } = await client.balance();
const usage = await client.usage({ service: 'weather-api', limit: 10 });
const settlements = await client.settlements({ role: 'seller', from: '2026-03-01' });
const { listings } = await client.listings.list();
const profile = await client.sellerProfile('wallet-address');
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Balance 0 | Deposit: `proxygate deposit -a <amount>` — see `pg-buy` |
| Proxy returns 503 | Listing paused or seller tunnel down |
| "Unauthorized" | Run `proxygate login` to reconfigure — see `pg-setup` |
| Tunnel disconnects | Check `proxygate dev` logs, verify local port is open |
| Gateway unreachable | Verify URL: `https://gateway.proxygate.ai` |

## Related skills

| Need | Skill |
|------|-------|
| First-time setup | `pg-setup` |
| Buy API access | `pg-buy` |
| Sell API capacity | `pg-sell` |
| Job marketplace | `pg-jobs` |
| Check status | **This skill** |
| Update CLI/SDK | `pg-update` |
