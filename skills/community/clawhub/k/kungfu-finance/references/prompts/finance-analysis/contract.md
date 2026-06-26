# Finance Analysis Prompt Contract

This prompt asset comes from:

- upstream backend source path `serverless-tianshan-api/src/handlers/analyse_diagnosis/prompt/finance_analysis_prompt.py`

It is stored in this skill repo as pure markdown only.

## Prompt Assets

- `finance_analysis_system.md`
- `finance_analysis_user_template.md`

## Required Template Variables

The user template requires these placeholders:

- `{INSTRUMENT_NAME}`
- `{INSTRUMENT_ID}`
- `{EXCHANGE_ID}`
- `{LATEST_DATE}`
- `{FINANCIAL_DATA}`
- `{QUARTERLY_YEARS}`
- `{ANNUAL_YEARS}`
- `{TODAY}`

## Expected Use

Use this prompt only for finance-analysis style reports.

Do not:

- mix it with unusual movement prompt assets
- load the original Python file at runtime
- rewrite the template text in JS

The intended flow is:

1. load structured finance data
2. render `finance_analysis_user_template.md` with the variables above
3. use `finance_analysis_system.md` as the system prompt
