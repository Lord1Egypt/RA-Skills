# MEV Patterns on Base L2

## Known Attack Types

### Sandwich Attacks
**Pattern:** Attacker sees victim's swap → frontrun with same-direction swap → victim executes at worse price → attacker backruns to close position.

**Indicators:**
- Large swap in mempool (> $5K)
- Bot cluster activity (multiple similar txs)
- Attacker gas price > victim gas price
- Victim slippage > 0.5%

### Frontrunning
**Pattern:** Attacker copies victim's transaction idea with higher gas price.

**Common targets:**
- Token launches
- NFT mints
- Oracle updates
- Governance votes

### Backrunning
**Pattern:** Attacker follows victim's large trade to benefit from price impact.

## Bot Signatures on Base

MEV bots often use:
- Flash loans for capital (Aave V3)
- Specialized router contracts
- Very high gas prices (1-10 gwei)
- Multiple transactions in single block

## Protection RPCs

| Service | URL | Cost |
|---------|-----|------|
| Flashbots Protect | https://rpc.flashbots.net | Free |
| MEV Blocker | https://rpc.mevblocker.io | Free |
| Merkle (private) | https://rpc.merkle.io | Free tier |

## Detection Accuracy

Our scanner uses heuristics:
- Gas price analysis: ~80% accurate
- Pattern matching: ~70% accurate
- False positive rate: ~15%

For high-value transactions (> $1K), consider using all protection layers.
