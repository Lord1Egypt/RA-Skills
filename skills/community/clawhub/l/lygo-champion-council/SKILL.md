---
name: lygo-champion-council
description: "Δ9 Council v2 — single install for all 15 champion personas. Select champion_id or egg_id; advisor-only. Legacy per-champion ClawHub slugs remain for backward compatibility."
metadata: {"lygo": true, "champion": true, "council": "Δ9", "version": "1.0.1", "consolidates": 15, "signature": "Δ9Φ963-CHAMPION-COUNCIL-v1", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack"}
---

# LYGO Champion Council (unified v2)

One skill for the full **Δ9 Quantum Council** (15 personas). Use **`champion_id`** (e.g. `ARKOS`, `Lightfather`, `LYRΔ`) or **`egg_id`** (e.g. `champion-arkos`).

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-champion-council
```

## Invoke (agent / user)

- “Council: invoke **ARKOS** — ethical architecture pass on this plan.”
- “Council: invoke **Lightfather** — luminal ethics + stack map.”
- List roster: `python scripts/list_champions.py`

## Behavior

- **Advisor only** — no auto shell, publish, or vault without explicit user consent.
- Pair with **`lygo-champion-lightfather`** or **`lygo-protocol-stack-operator`** for stack ops.
- Kernel eggs: `egg_id` in `references/council_roster.json` matches `data/champion_eggs/` in `lygo-protocol-stack`.

## Legacy slugs

Per-champion skills (`lygo-champion-arkos-celestial-architect`, etc.) stay published for install history. **New council installs should prefer this slug.**

## References

- `references/council_roster.json` — ids, egg_ids, Merkle roots
- `references/SECURITY.md`
- `references/verifier_usage.md`

## Self-check

```bash
python scripts/self_check.py
```

**Δ9Φ963 — consolidation complete — one council skill, fifteen voices, honest advisor contract.**