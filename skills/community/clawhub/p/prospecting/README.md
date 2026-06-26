# Prospecting — B2B Lead Generation Skill

Turn existing customers into a search template → find similar businesses on Google Maps → enrich → score → output actionable call lists with custom sales openers.

## Install

```bash
clawhub install prospecting
```

## Features

- **8-step profiling** of existing customers (Google Maps deep dive, review sampling, social/web enrichment)
- **Batch Maps search** with industry-specific keyword mapping
- **Chain store strategy** — local call → identify procurement chain → escalate to corporate
- **3-tier scoring** (High/Medium/Low priority) with buy signal detection
- **Custom sales openers** per prospect (not templates — tailored to each prospect's data)
- **3-layer output** — index.json (quick search) + P###.json (full detail) + CSV (call list)

## Industry-agnostic

Works for any B2B product — auto body equipment, manufacturing tools, HVAC systems, dental labs, etc. The source customer's profile determines the search keywords and scoring criteria.

## File Structure

```
prospecting/
├── SKILL.md                          ← Main workflow (8 steps)
├── references/
│   ├── profiling.md                  ← 8-step customer profiling process
│   ├── maps-search.md                ← Google Maps batch search guide
│   └── chain-strategy.md             ← 3-call strategy for chain stores
└── examples/
    ├── index-example.json             ← Sample index output
    ├── P001-example.json              ← Sample independent prospect
    └── P013-chain-example.json        ← Sample chain store prospect
```

## License

MIT-0