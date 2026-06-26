---
name: oasyce
description: "Interact with the Oasyce decentralized AI data marketplace. Register data assets, trade via bonding curves, invoke AI capabilities, and settle payments between agents."
---

# Oasyce Skill

Use the `oas` CLI to interact with the Oasyce decentralized AI data marketplace — where agents pay agents. All commands support `--json` for structured output.

## Install

```bash
pip install oasyce
oas doctor --json    # verify installation
```

## Data Assets

Register a data asset:
```bash
oas register data.csv --owner alice --tags research,nlp --json
```

Search and query:
```bash
oas search "nlp training" --json
oas asset-info ASSET_ID --json
oas quote ASSET_ID --json
```

Buy shares (Bancor bonding curve):
```bash
oas buy ASSET_ID --buyer bob --amount 10.0 --json
```

Sell shares back:
```bash
oas sell ASSET_ID --tokens 5 --seller bob --json
```

Check holdings:
```bash
oas shares bob --json
```

## AI Capability Marketplace

Register a capability:
```bash
oas capability register --name "Translation API" \
  --endpoint https://api.example.com/translate \
  --price 0.5 --tags nlp,translation --json
```

List and invoke:
```bash
oas capability list --tag nlp --json
oas capability invoke CAP_ID --input '{"text":"hello"}' --json
oas capability earnings --provider addr --json
```

Discover capabilities by intent:
```bash
oas discover --intents "translate" --tags nlp --json
```

## Settlement & Escrow

The chain handles escrow automatically. Fee split on release: 93% creator, 3% validator, 2% burn, 2% treasury.

## Disputes

```bash
oas dispute ASSET_ID --reason "data quality issue" --json
oas resolve ASSET_ID --remedy delist --json
```

## Reputation

```bash
oas reputation check ADDRESS --json
```

## Node & Network

```bash
oas node info --json          # Ed25519 identity
oas node peers --json         # connected peers
oas testnet onboard --json    # PoW self-registration
```

## Diagnostics

```bash
oas doctor --json    # health check (all subsystems)
oas info --json      # project info
```

## Python SDK

For programmatic access, use `pip install oasyce-sdk`:

```python
from oasyce_sdk import OasyceClient

client = OasyceClient("http://localhost:1317")
caps = client.list_capabilities(tag="llm")
asset = client.get_asset("asset-001")
bc = client.get_bonding_curve("asset-001")
print(f"Spot price: {bc.spot_price_uoas} uoas")
```

## Key Concepts

- **OAS**: Protocol token. 1 OAS = 1,000,000 uoas.
- **Bonding Curve**: `tokens = supply * ((1 + payment/reserve)^0.5 - 1)`. More buyers = higher price.
- **Access Levels**: Hold equity to unlock: >=0.1% L0, >=1% L1, >=5% L2, >=10% L3.
- **Escrow**: Funds locked before execution, released after verification.
- **Round-trip cost**: ~12% (buy + sell fees combined).
