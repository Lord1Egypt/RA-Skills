# Staking Concepts

Key concepts for understanding INDY token staking on the Indigo Protocol.

## What is INDY Staking?

INDY is the governance token of the Indigo Protocol. By staking INDY tokens, users:

1. **Earn rewards** — receive a share of protocol fees (in ADA) proportional to their stake
2. **Participate in governance** — staked INDY grants voting power on protocol proposals
3. **Support the protocol** — staking locks INDY, reducing circulating supply

## Staking Position Lifecycle

1. **Open** — Lock INDY tokens to create a staking position
2. **Earn** — Accumulate ADA rewards over time from protocol fees
3. **Adjust** — Increase or decrease the staked amount at any time
4. **Close** — Withdraw all staked INDY and claim accumulated rewards

## Reward Distribution

Protocol fees (from CDP operations, liquidations, etc.) flow into the staking reward pool. Rewards are distributed proportionally:

```
Your Reward Share = (Your Staked INDY / Total Staked INDY) × Total Rewards
```

The `distribute_staking_rewards` tool triggers the on-chain distribution of pending rewards. Anyone can call this — it benefits all stakers.

## INDY Token

| Property | Value |
|----------|-------|
| Token name | INDY |
| Decimals | 6 |
| 1 INDY | 1,000,000 smallest units |
| Max supply | Fixed (set at protocol launch) |

## Governance Voting Power

Staked INDY grants voting power on:
- **Temperature checks** — preliminary community sentiment polls
- **Formal governance polls** — on-chain votes for protocol parameter changes
- **Protocol upgrades** — changes to smart contracts and mechanisms

Voting power is proportional to the amount of INDY staked.
