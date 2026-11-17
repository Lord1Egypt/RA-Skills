## Description:

Queries OPD financial data APIs for China A-share listed company fundamentals, securities and industry classification, trading history, financial reports and indicators, financing activity, major events, shareholders, executives, equity, and governance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[originp-data](https://clawhub.ai/user/originp-data)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve OPD A-share company, market, finance, financing, event, shareholder, and governance data through a local Python command-line client. It is intended for data lookup and analysis workflows where users have an OPD API key and the required interface subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because API-key handling is weaker than the skill's stated safety boundary.

Mitigation: Install only after reviewing the skill and trusting OPD; use a restricted OPD key where possible, store it locally with appropriate file permissions, and rotate the key if it is shared in chat or logs.

Risk: The OPD API may return sensitive company contact, shareholder, salary, birth-date, or resume fields.

Mitigation: Request only the fields needed for the task, avoid broad default-field queries when sensitive fields are unnecessary, and avoid persisting or redistributing raw responses.

Risk: The skill depends on OPD subscriptions, rate limits, and externally supplied financial data.

Mitigation: Check subscription status and API errors before relying on results, respect the documented rate limit, and present returned data as OPD-sourced rather than independently verified facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/originp-data/skills/opd-data)
- [OPD API endpoint](https://api.originp.com)
- [OPD data portal](https://data.originp.com/)
- [Basic information catalog](references/catalog_basic.md)
- [Trading information catalog](references/catalog_trading.md)
- [Financial information catalog](references/catalog_finance.md)
- [Financing and allocation catalog](references/catalog_financing.md)
- [Major events catalog](references/catalog_events.md)
- [Equity and governance catalog](references/catalog_governance.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and an OPD_API_KEY; API queries are limited to subscribed OPD interfaces and may return sensitive company contact, shareholder, compensation, birth-date, or resume fields.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
