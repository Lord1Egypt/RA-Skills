# Trade Request Template

Ask the user for the missing fields below before attempting a live order.

## Credentials

- Aionmarket API key:
- Wallet address:
- Polymarket API key:
- Polymarket API secret:
- Polymarket API passphrase:
- Wallet private key for local signing, or pre-signed order object:

## Market

- Market condition ID:
- Market question:
- Outcome: `YES` or `NO`
- Token ID, if already known:

## Execution

- Order side inside signed order: `BUY` or `SELL`
- Order size:
- Price:
- Limit or market mode:
- Order type: `GTC`, `FOK`, `GTD`, or `FAK`
- Order version, if known: `1` or `2`
- Wallet owner field, if known:
- Expiration time, if needed:
- Reasoning text:

## Safety Checks

- Is this simulation or live trading?
- Has the wallet already been registered with `/wallet/credentials`?
- Should I verify market context before submit?
- Should I check positions or open orders after submit?
