# Memory Template - Post-Labor Economics

Create `~/post-labor-economics/memory.md` with this structure:

```markdown
# Post-Labor Economics Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## System Context
<!-- Geography, institution level, and scope -->
<!-- Time horizon and political constraints -->

## Transition Thesis
<!-- Main mechanism: automation, demographics, ecology, ownership, productivity -->
<!-- What the user currently believes is changing -->

## Portfolio Preferences
<!-- Preferred policy instruments and excluded instruments -->
<!-- Financing assumptions the user accepts -->

## Indicators and Thresholds
<!-- Metrics tracked by user and target ranges -->
<!-- Trigger conditions for policy adjustment -->

## Scenarios in Play
<!-- Base case, upside, downside assumptions -->
<!-- Most likely failure modes -->

## Notes
<!-- Durable observations only -->

---
*Updated: YYYY-MM-DD*
```

## portfolios.md Template

Create `~/post-labor-economics/portfolios.md`:

```markdown
# Policy Portfolios

## YYYY-MM-DD - [Portfolio Name]
Objective: ...
Baseline security: ...
Work coordination: ...
Ownership and bargaining: ...
Financing: ...
Risks: ...
Status: draft | tested | adopted | retired
```

## indicators.md Template

Create `~/post-labor-economics/indicators.md`:

```markdown
# Indicators Dashboard

## YYYY-MM-DD
Employment rate: value / target
Median real wage: value / target
Labor income share: value / target
Household insecurity index: value / target
Public service access index: value / target
Automation gain capture rate: value / target
Notes: ...
```

## scenarios.md Template

Create `~/post-labor-economics/scenarios.md`:

```markdown
# Scenario Register

## Scenario A - Managed Transition
Assumptions: ...
Signals: ...
Policy response: ...

## Scenario B - Dual Economy Drift
Assumptions: ...
Signals: ...
Policy response: ...
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default state | Keep collecting context and updating assumptions |
| `complete` | Stable decision frame | Refresh only when major shocks appear |
| `paused` | User wants minimal depth | Provide concise outputs with existing context |
| `never_ask` | User rejected setup prompts | Stop setup prompts and use current context only |
