# Polymarket Brain — Discord Output Format v1.1

## Table Format for Discord

```
## 🧠 POLYMARKET BRAIN — GEOPOLITICAL ANALYSIS SUMMARY

**News Source:** 2026-03-17-cnbc-geopolitics
**Analysts:** geopolitics-expert (Iran-Hormuz conflict), the-fed-agent v1.0.2 (USD macro)

---

| Market | Resolution Date | Market Odds | Expert Probability | Recommendation |
|--------|----------------|-------------|-------------------|----------------|
| Will Iranian regime fall by June 30? | June 30, 2026 (~3.5 mo) | 28% Yes | 15% | ✅ **Strong No** — IRGC institutional depth makes collapse unlikely (Pathway 3: 3%) |
| US x Iran ceasefire by December 31 | Dec 31, 2026 (~9.5 mo) | 73% Yes | 65% | ⚠️ **Fair/Lean No** — Aligns with "Forced Ceasefire" scenario (40% by 3-6mo, 65% by year-end) |
| Iran x US/Israel conflict ends by December 31 | Dec 31, 2026 (~9.5 mo) | 84% Yes | 70% | ⚠️ **Slight Overpricing** — Possible but forever war risk (35% indefinite continuation) |
| US forces enter Iran by December 31 | Dec 31, 2026 (~9.5 mo) | 61% Yes | 35% | ✅ **Strong No** — Ground invasion requires massive mobilization; air campaign likely sufficient |
| Iran leadership change by December 31 | Dec 31, 2026 (~9.5 mo) | 62% Yes | 50% | ⚖️ **Fair Value** — Possible through negotiation or attrition (Pathway 2: 30%) |
| Oil to exceed $120 before June 2026 | June 30, 2026 (~3.5 mo) | 52% Yes | 60% | 📈 **Slight Underpricing** — If Hormuz stays closed (50% prolonged attrition), $120+ likely |

---

### Analyst Data Sources

| Analyst | Output | Key Metrics |
|---------|--------|-------------|
| **geopolitics-expert** | Iran-Hormuz conflict analysis | 80% forever war, 50% prolonged attrition, Brent $101/bbl |
| **the-fed-agent v1.0.2** | USD macro + Fed policy | 35-40% recession risk, Hold rates Q2, dovish pivot H2 |

---

**Market Odds:** Real-time data from Polymarket API (30-70% balanced odds filter)

**Expert Probability & Recommendation:** Derived from geopolitics-expert and the-fed-agent v1.0.2 analysis frameworks

---

### Market Links

1. [Iranian regime fall by June 30](https://polymarket.com/event/will-the-iranian-regime-fall-by-the-end-of-2026)
2. [US-Iran ceasefire by December 31](https://polymarket.com/event/us-iran-nuclear-deal-before-2027)
3. [Iran conflict ends by December 31](https://polymarket.com/event/iran-x-us-israel-conflict-ends-by-2026)
4. [US forces enter Iran by December 31](https://polymarket.com/event/will-the-us-invade-iran-before-2027)
5. [Iran leadership change by December 31](https://polymarket.com/event/iran-leadership-change-2026)
6. [Oil >$120 before June 2026](https://polymarket.com/event/oil-exceeds-120-before-june-2026)
```

---

## Key Format Changes

| Element | Previous | New v1.1 |
|---------|----------|----------|
| **Output Structure** | List format | Markdown table |
| **Recommendation Icons** | None | ✅ ⚠️ 📈 ⚖️ |
| **Expert Probability** | Separate section | Inline in table |
| **Rationale** | Long paragraphs | Concise parenthetical |
| **Market Links** | Embedded in rows | Separate section |
| **Analyst Attribution** | Implicit | Explicit table |

---

## Discord Webhook Payload

```json
{
  "embeds": [
    {
      "title": "🧠 Polymarket Brain — Geopolitical Analysis Summary",
      "color": 5865F2,
      "fields": [
        {
          "name": "News Source",
          "value": "2026-03-17-cnbc-geopolitics",
          "inline": true
        },
        {
          "name": "Analysts",
          "value": "geopolitics-expert + the-fed-agent v1.0.2",
          "inline": true
        }
      ]
    }
  ]
}
```

---

## Implementation Notes

1. **Table Rendering:** Discord markdown tables use pipe `|` syntax
2. **Emoji Icons:** ✅ (Strong No), ⚠️ (Fair/Lean), 📈 (Underpricing), ⚖️ (Fair Value)
3. **Probability Alignment:** Expert probability from analyst frameworks (geopolitics-expert termination scenarios, the-fed-agent v1.0.2 policy paths)
4. **Concise Rationale:** Parenthetical references to specific framework pathways/scenarios
