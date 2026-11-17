# AI-POLC Extensions

**Purpose:** Optional capabilities that add specialized depth to specific stages. Extensions are NOT deferred scope — they are capabilities that only some products/contexts need.

---

## Extension Architecture

Each extension has two files:
- `{name}.opt-in.md` — Lightweight detection prompt (always scanned at stage entry)
- `{name}.md` — Full rules (loaded only when user confirms activation)

---

## Available Extensions

| Extension | Stage | Trigger | What It Adds |
|-----------|:---:|---------|-------------|
| Advanced Discovery | 4 | "OKRs" / "JTBD" / "hypothesis testing" | OKR hierarchy, JTBD framing, opportunity scoring |
| Full Traceability | 10 | "full traceability" / compliance context | Audit-grade matrix with outcome tracing |
| Full Risk Register | 9 | "full risk management" / high uncertainty | Scoring, response plans, risk owners, review cadence |
| Value & Metrics Engine | 16 | "track value" / "measure outcomes" | KPIs, benefits realization, cost-of-delay, experiments |
| Full Product Docs | 12 | "PRD" / "feature brief" | PRD templates, feature briefs, wiki governance |
| Quality Review | Post-5 | "check quality" / quality issues detected | Automated quality scanning of epics/stories |
| MVP/MMP Mature | 7 | "define next version scope" on mature product | Re-activates MVP/MMP framework for next major version |

---

## Activation Rules

1. At stage entry, scan for extension triggers in:
   - User's current message
   - Context factors (e.g., Compliance = Heavy → suggest Full Traceability)
   - Depth level (Comprehensive → suggest relevant extensions)
2. If trigger detected, load the `.opt-in.md` file
3. Present activation prompt to user
4. If user confirms → load full extension file and apply
5. Record activation in `polc-state.md` Active Extensions list

---

## Composition Rules

- Multiple extensions can be active simultaneously (no conflicts by design)
- Extensions are additive — they add artifacts/checks, never remove core ones
- Extension output goes in the same folders as core output (not separate extension folders)
- Extension state is tracked in `polc-state.md`
