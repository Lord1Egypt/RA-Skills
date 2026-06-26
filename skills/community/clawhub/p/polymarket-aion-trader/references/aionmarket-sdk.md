# Aionmarket SDK Reference

This note captures only SDK method names that are explicitly shown in the Aionmarket documentation pages reviewed for this skill.

## SDK Import And Client Setup

The docs show Python examples using `aion_sdk` and `AionMarketClient`:

```python
from aion_sdk import AionMarketClient

client = AionMarketClient(
    api_key="YOUR_AGENT_API_KEY",
    base_url="https://pm-t1.bxingupdate.com/bvapi",
)
```

## Documented Methods

### Wallet credential check

```python
status = client.check_wallet_credentials(wallet)
```

Use this before trying to register wallet credentials again.

### Wallet credential registration

```python
result = client.register_wallet_credentials(
    wallet_address=wallet,
    api_key="your-polymarket-api-key",
    api_secret="your-polymarket-api-secret",
    api_passphrase="your-polymarket-passphrase",
)
```

This is the documented SDK path for Polymarket live wallet setup.

### Briefing / market heartbeat

```python
briefing = client.get_briefing(
    venue="polymarket",
    include_markets=True,
    user="0xYOUR_WALLET",
)
```

The docs recommend briefing as the regular polling call for risk alerts and candidate markets.

## Important Limitation

In the docs reviewed for this skill, a Polymarket trade submit helper name was not explicitly shown in SDK form. Do not invent one such as `client.place_trade(...)` unless the installed SDK or the official docs confirm it.

When the user asks for execution and the SDK submit helper cannot be verified, use the documented REST endpoint `POST /markets/trade` with a signed `order` payload.

## How To Use In This Skill

- Prefer SDK for wallet readiness and briefing.
- Keep REST fallback for register-agent, explicit market context lookup, and trade submit.
- If you need to verify whether the installed SDK exposes more helpers, inspect the local package or official docs before using them.
