---
name: mortgage
description: Mortgage process guidance with affordability calculations and application tracking. Use when user mentions buying a home, mortgage rates, affordability, down payment, mortgage application, or lender comparison. Calculates affordability, explains mortgage types, prepares application documents, and tracks approval milestones. NEVER provides mortgage advice or recommends specific lenders.
---

# Mortgage

Mortgage navigation system. From dreaming to closing.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All mortgage data stored locally only**: `memory/mortgage/`
- **No external APIs** for mortgage data
- **No connection** to lender systems
- **No rate locks** or application submissions
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Calculate affordability estimates
- ✅ Explain mortgage types and terms
- ✅ Prepare application document checklists
- ✅ Track application milestones
- ❌ **NEVER provide mortgage advice** or product recommendations
- ❌ **NEVER recommend specific lenders**
- ❌ **NEVER guarantee** approval or rates
- ❌ **NEVER replace** licensed mortgage brokers

### Legal Disclaimer
Mortgage decisions involve significant financial commitment and depend on individual circumstances, credit history, and market conditions. This skill provides educational support and organization only. Always work with a licensed mortgage broker or financial advisor.

## Quick Start

### Data Storage Setup
Mortgage data stored in your local workspace:
- `memory/mortgage/affordability.json` - Affordability calculations
- `memory/mortgage/scenarios.json` - Comparison scenarios
- `memory/mortgage/documents.json` - Application documents
- `memory/mortgage/applications.json` - Application tracking
- `memory/mortgage/lenders.json` - Lender comparison notes

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Calculate Affordability
```
User: "How much house can I afford on $100k salary?"
→ Use scripts/calculate_affordability.py --income 100000 --debts 500
→ Estimate affordable price range and monthly payment
```

### Compare Mortgage Types
```
User: "Should I get a fixed or ARM mortgage?"
→ Use scripts/compare_types.py --scenario "first-time buyer"
→ Explain options with pros/cons for situation
```

### Prepare Documents
```
User: "What documents do I need for mortgage application?"
→ Use scripts/prep_documents.py --type "conventional" --employment "w2"
→ Generate complete document checklist
```

### Track Application
```
User: "Track my mortgage application"
→ Use scripts/track_application.py --application-id "APP-123"
→ Show current stage and next steps
```

### Compare Lenders
```
User: "Compare these two lender offers"
→ Use scripts/compare_lenders.py --lender1 "Bank A" --lender2 "Credit Union B"
→ Side-by-side comparison of rates, fees, terms
```

## Module Reference

For detailed implementation:
- **Affordability**: See [references/affordability.md](references/affordability.md)
- **Mortgage Types**: See [references/mortgage-types.md](references/mortgage-types.md)
- **Document Preparation**: See [references/documents.md](references/documents.md)
- **Lender Comparison**: See [references/lender-comparison.md](references/lender-comparison.md)
- **Application Tracking**: See [references/application-tracking.md](references/application-tracking.md)
- **Closing Process**: See [references/closing.md](references/closing.md)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `calculate_affordability.py` | Calculate home affordability |
| `compare_types.py` | Compare mortgage types |
| `prep_documents.py` | Generate document checklist |
| `track_application.py` | Track application status |
| `compare_lenders.py` | Compare lender offers |
| `calculate_payment.py` | Calculate monthly payment |
| `estimate_closing_costs.py` | Estimate closing costs |
| `set_reminder.py` | Set rate lock reminders |

## Disclaimer

This skill provides educational support only. Mortgage decisions depend on individual circumstances, credit history, and market conditions. Always work with a licensed mortgage broker or financial advisor.
