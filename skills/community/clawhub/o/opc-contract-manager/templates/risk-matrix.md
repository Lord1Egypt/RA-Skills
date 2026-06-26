# Risk Assessment Matrix

## Dual-Dimension Scoring

Each finding is scored on two independent dimensions:

### Severity (Legal / Financial Risk)

| Level | Indicator | Definition | Action |
|-------|-----------|------------|--------|
| **Critical** | :red_circle: | Existential risk — personal liability exposure, loss of core IP, or potential business shutdown | Do not sign. Resolve before proceeding. |
| **High** | :orange_circle: | Significant exposure — material financial loss, operational constraint, or difficult-to-reverse commitment | Strongly recommend negotiating. Escalate if counterparty refuses. |
| **Medium** | :yellow_circle: | Notable concern — unfavorable but manageable terms, or missing protections you should have | Worth raising. Accept only with offsetting concessions. |
| **Low** | :large_blue_circle: | Minor issue — slightly below ideal but within acceptable range for most business contexts | Note for awareness. Negotiate if convenient. |
| **Info** | :white_circle: | Observation — neutral finding or standard clause that merits awareness but no action | No action needed. |

### Negotiation Priority (Business Impact)

| Level | Definition | Guidance |
|-------|------------|----------|
| **Must negotiate** | This term directly impacts your cash flow, IP, liability, or ability to operate. Non-negotiable. | Do not sign without changes. Be prepared to walk away. |
| **Should negotiate** | This term is unfavorable and worth pushing on. Accept only if counterparty offers meaningful concessions elsewhere. | Raise in negotiation. Have a fallback position ready. |
| **Can accept** | This term is standard or low-impact. Acceptable as-is. Use as a concession chip if needed. | Accept or trade for something more important. |

### Why Two Dimensions?

Severity and priority are independent:

- **Medium severity + Must negotiate**: Payment terms of net-90. Not legally dangerous, but devastating for solo entrepreneur cash flow.
- **High severity + Can accept**: Standard mutual arbitration clause. High legal stakes in theory, but industry-standard and unlikely to change.
- **Critical severity + Must negotiate**: Uncapped personal indemnity. Both legally dangerous and must be changed.

## Matrix Template

| # | Finding | Severity | Priority | Clause | Best Ask | Fallback | Walk Away |
|---|---------|----------|----------|--------|----------|----------|-----------|
| {{n}} | {{finding}} | {{level}} | {{must/should/can}} | {{ref}} | {{best}} | {{fallback}} | {{threshold}} |

## Summary Statistics

| Severity | Count |
|----------|-------|
| Critical | {{n}} |
| High | {{n}} |
| Medium | {{n}} |
| Low | {{n}} |
| Info | {{n}} |

| Priority | Count |
|----------|-------|
| Must negotiate | {{n}} |
| Should negotiate | {{n}} |
| Can accept | {{n}} |

## Overall Risk Rating

Determined by:
1. **Highest severity finding** sets the floor
2. **Count of Must-negotiate items** adjusts upward
3. **Presence of escalation triggers** overrides to Critical

| Condition | Overall Rating |
|-----------|---------------|
| Any Critical finding | **Critical** |
| 2+ High findings OR 3+ Must-negotiate items | **High** |
| 1 High finding OR 1-2 Must-negotiate items | **Medium-High** |
| Medium findings only, few Must-negotiate items | **Medium** |
| Low/Info findings only | **Low** |
