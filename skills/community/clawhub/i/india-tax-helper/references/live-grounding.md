# Live grounding

This skill must prefer **runtime grounding** over static FY-sensitive memory.

## Golden rule
Do not trust embedded tax rates, due dates, threshold limits, or form applicability unless they are either:
1. verified in the current FY source manifest, or
2. fetched and checked during the current run.

## Search strategy
### First choice
Use official URLs already present in `references/fy-2026-27/source-manifest.json` when they fit the question.

### If more current context is needed
Use available web search tools (e.g. `web_search`) to query official sources:

```
web_search 'site:incometax.gov.in <topic>'
```

Examples:
- `web_search 'site:incometax.gov.in AIS TIS 26AS income tax department'`
- `web_search 'site:incometax.gov.in salaried individuals return applicable'`
- `web_search 'site:incometax.gov.in income tax returns downloads'`
- `web_search 'site:incometax.gov.in Form 12BB income tax'`
- `web_search 'site:incometax.gov.in Form 15G Form 15H income tax'`

### Then fetch the selected official page
Use `web_fetch` or another available reader to inspect the actual official page.

## Runtime verification checklist
Before giving a confident FY-sensitive answer, verify:
- correct FY / AY mapping
- resident salaried scope
- regime context (old/new)
- official or high-confidence source for rates/deadlines/forms
- whether the answer is conceptual, calculative, or compliance-sensitive

## What can stay static
These are safer to keep as skill guidance:
- workflow shape
- what documents usually matter
- what kinds of questions to ask
- which scripts to run
- fail-closed behavior

## What should usually be grounded live
- tax slabs / rebate / surcharge for a given FY
- due dates and filing windows
- ITR applicability changes
- changes to capital-gains treatment
- 15G / 15H conditions if FY-sensitive
- portal/form release status
