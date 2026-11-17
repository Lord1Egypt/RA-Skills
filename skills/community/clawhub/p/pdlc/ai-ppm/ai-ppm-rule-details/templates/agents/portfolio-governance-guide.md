<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
<!-- BEGIN AI-PPM AGENT GUIDE SECTION -->

## AI-PPM: Portfolio Governance Agent (PGA__)

### What It Checks

The Portfolio Governance Agent validates that your portfolio management discipline is being maintained. It runs 16 automated checks across 4 categories:

| Category | Checks | What It Validates |
|----------|:------:|-------------------|
| **Portfolio Currency** | PC1–PC4 | Is the register fresh? Is data current? Are reviews happening on schedule? |
| **Governance Completeness** | GC1–GC4 | Does every project have proper governance records? Decisions? Authorizations? |
| **Decision Quality** | DQ1–DQ4 | Do decisions have rationale? Are review dates set? Any overdue reviews? |
| **Health Monitoring** | HM1–HM4 | Is the dashboard current? Are anomalies being actioned? Are retirements recorded? |

### How to Use

1. Type `PGA__` in any chat prompt
2. The agent scans your portfolio artifacts
3. Produces a pass/warn/fail report with recommended actions
4. Address failures first, then warnings

### Recommended Cadence

| Frequency | Context |
|-----------|---------|
| Monthly | Regular governance hygiene |
| Before quarterly review | Ensure data is ready for strategic assessment |
| After gap (>4 weeks without portfolio activity) | Catch up on governance debt |
| After portfolio changes (new project, retirement) | Verify records are complete |

### Interpreting Results

- **All green (16/16 pass):** Portfolio governance is healthy. Maintain cadence.
- **Warnings only:** Minor attention needed — typically stale data or approaching review dates.
- **Failures present:** Governance gap exists — address before next portfolio decision.

### Common Failure Patterns

| Pattern | Likely Cause | Fix |
|---------|-------------|-----|
| PC checks failing | Haven't run Stage 7 (ingestion) recently | Run a portfolio sync session |
| GC checks failing | Projects were admitted informally (no PGD record) | Create governance records retroactively |
| DQ checks failing | Decisions made without rationale | Update PGD records with reasoning |
| HM checks failing | Dashboard not regenerated after ingestion | Run Stage 8 |

<!-- END AI-PPM AGENT GUIDE SECTION -->
