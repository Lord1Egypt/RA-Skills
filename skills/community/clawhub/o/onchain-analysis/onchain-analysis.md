# SKILL: onchain-analysis

## Purpose
Interpret blockchain data strategically: identify patterns, detect anomalies, map flows, and surface risk signals — data-backed only.

## When to Use
- Wallet/contract behavior seems suspicious or unclear
- You need to understand fund flows before a decision
- Investigating market behavior, insider movement, or protocol health

## Inputs
- `wallet_data` (optional): addresses + labels + balances
- `contract_data` (optional): contract address + ABI/artifacts + known roles
- `transactions` (required): tx list or tx ids/hashes
- `chain` (optional): chain + timeframe

## Steps
1. Normalize inputs:
   - ensure chain/time window is explicit
   - ensure transactions are uniquely identified
2. Identify patterns:
   - recurring counterparties
   - periodic deposits/withdrawals
   - concentration and dispersion patterns
3. Detect anomalies:
   - sudden large transfers
   - new counterparties with high volume
   - unusual contract interactions
4. Map flows:
   - sources → sinks
   - intermediate hops
   - aggregator/bridge interactions (label as such)
5. Evaluate intent as hypotheses:
   - propose 1–3 plausible explanations
   - attach confidence and what evidence would change it
6. Produce action-oriented output:
   - risk signals
   - what to verify next

## Validation
- Include tx hashes / block references when possible.
- Distinguish facts from hypotheses.
- If data is incomplete, state the missing pieces explicitly.

## Output
- `insights` (facts + patterns)
- `risk_signals`
- `opportunities` (only if supported by data)
- `hypotheses` (with confidence)
- `next_checks`

## Safety Rules
- Data-backed only; no “mind reading” claims.
- Do not assist illicit activity or evasion.

## Example
Input: 200 txs for one wallet over 30 days.
Output: “High concentration into 2 addresses; one new counterparty accounts for 70% volume; verify entity labels + bridge usage.”

