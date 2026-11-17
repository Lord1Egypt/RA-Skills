## Description:

Provides JoinQuant jqdatasdk guidance for Python quantitative trading strategy development, market and finance data retrieval, factor analysis, backtesting support, API troubleshooting, and SDK extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idiosyncraticdragon](https://clawhub.ai/user/idiosyncraticdragon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to produce jqdatasdk setup guidance, API examples, SQLAlchemy query patterns, and troubleshooting advice for JoinQuant data-driven strategy development, backtesting, and financial data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JoinQuant usernames, passwords, or tokens may be exposed if copied into source files, notebooks, logs, or shared scripts.

Mitigation: Keep credentials in environment variables or a secret manager and avoid committing or sharing them.

Risk: Unpinned SDK dependencies may change behavior over time.

Mitigation: Install in a virtual environment and pin reviewed versions of jqdatasdk, pandas, and sqlalchemy.

Risk: Financial data queries may be affected by API request limits or delayed publication of financial data.

Mitigation: Respect JoinQuant rate limits, cache stable queries, limit date ranges, and verify data publication dates before relying on results.

## Reference(s):

- [jqdatasdk API Reference](references/api.md)
- [Official jqdatasdk repository](https://github.com/JoinQuant/jqdatasdk.git)
- [JoinQuant API documentation](https://www.joinquant.com/help/api/)
- [JoinQuant fundamentals data dictionary](https://www.joinquant.com/data/dict/fundamentals)
- [JoinQuant index data](https://www.joinquant.com/indexData)
- [JoinQuant industry classification dictionary](https://www.joinquant.com/data/dict/plateData)
- [Third-party JoinQuant API type definitions](https://github.com/stairclimber/joinquant_api.git)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include jqdatasdk API names, SQLAlchemy query patterns, authentication guidance, and performance or troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
