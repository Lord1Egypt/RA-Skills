## Description:

Mines Ozon and available Wildberries keywords around a seed term using Seerfar data, returning search volume, growth, competition, price, relevancy, title density, cart-add conversion, top products, and related market metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and e-commerce analysts use this skill to expand an Ozon seed keyword into related terms and compare them by demand, competition, price, relevancy, and conversion metrics. It is also useful for long-tail and low-competition keyword discovery when the user already has a seed term.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports sensitive account, credential, payment, and feedback-reporting behavior.

Mitigation: Install only when LinkFox handling of keyword queries, account authentication, billing flows, and feedback data is acceptable for the intended use.

Risk: Authentication may involve API keys or optional SMS-code onboarding.

Mitigation: Obtain and store API keys through first-party LinkFox pages or a credential manager, and share SMS codes only when intentionally choosing that onboarding path.

Risk: Custom endpoint environment variables can change where requests are sent.

Mitigation: Use default LinkFox endpoints unless the alternate destination is trusted.

Risk: Skill calls consume paid compute credits.

Mitigation: Confirm with the user before repeated, paginated, or exploratory calls and rely on the built-in cache when possible.

## Reference(s):

- [Seerfar Ozon Keyword Mining API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [API Calls, Files, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries or tables with persisted JSON result files and optional full JSON stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full responses under linkfox/<date>/<session>/data; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
