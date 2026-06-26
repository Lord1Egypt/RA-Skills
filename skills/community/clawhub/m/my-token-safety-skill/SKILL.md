# Token Safety Checker

Detects risks of BSC tokens (honeypot, mintable, taxes, holder distribution). Perfect for quick "rug pull" analysis.

## Usage

Trigger keywords: `check token`, `scan token`, `token audit`, `土狗检测`

### Example

User: `check token 0x55d398326f99059ff775485246999027b3197955`

Agent will reply with risk level and detailed metrics.

## Parameters

- `address` (required): BSC token contract address.

## Output

- Risk level (Critical/High/Medium/Low)
- Score (0-100+)
- Detailed breakdown: honeypot, mintable, buy/sell tax, owner percent, holder count, open source.

## Notes

Uses GoPlus Labs API (free). Only supports BSC chain (chainId=56).