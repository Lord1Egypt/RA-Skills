# predge-settlement-risk

A Simmer (ClawHub) skill that checks a Polymarket market's UMA settlement state on Polygon before an agent trades it. Observe-only: it returns a trade or skip decision and a size multiplier, and places no orders.

- API: `GET https://api.predge.io/v1/settlement-risk/<condition id | market id | slug>`, free, no key, signed with Predge's published ed25519 key.
- Skill entry point: `settlement_risk_check.py` (stdlib only; `certifi` and `cryptography` are used when installed).
- Docs for agents: [SKILL.md](./SKILL.md). Risks: [DISCLAIMER.md](./DISCLAIMER.md). Sample run: [DEMO.md](./DEMO.md).

## Files

| file | what |
|---|---|
| `SKILL.md` | skill card rendered on simmer.markets/skills |
| `clawhub.json` | registry config (`simmer-sdk` in `requires.pip` lists it on Simmer) |
| `config.json` | gate tuning: `block_on_caution`, `watch_size_factor`, `block_resolved` |
| `settlement_risk_check.py` | fetch, verify, gate, CLI |
| `examples/*.json` | real signed records: disputed twice (UMA vote), clean, proposal in challenge window, resolved after two disputes |
| `tests/` | `python -m pytest tests -q`; add `PREDGE_LIVE=1` to also hit the live API |

## Test

```bash
pip install pytest cryptography certifi
python -m pytest tests -q
PREDGE_LIVE=1 python -m pytest tests -q
```

## Publish

```bash
npx clawhub@latest login                                  # GitHub sign-in, or --token clh_...
npx clawhub@latest publish . --slug predge-settlement-risk --version 0.1.0
npx clawhub@latest inspect predge-settlement-risk         # expect Moderation: CLEAN
```

Simmer lists ClawHub skills that require `simmer-sdk` within about 6 hours: check `https://api.simmer.markets/api/sdk/skills`.

## License

MIT-0 (ClawHub default).
