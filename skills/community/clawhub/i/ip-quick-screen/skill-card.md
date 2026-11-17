## Description:

Screens company patent portfolios or patent-number lists for a quick IP due-diligence overview, including patent counts, technology distribution, preliminary quality indicators, and risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and diligence teams use this skill to run a fast first-pass review of a company's patent position or a supplied patent list. It helps decide whether deeper professional IP analysis is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, company names, patent numbers, and patent-family identifiers may be sent to an external public patent API.

Mitigation: Use the skill only when those lookups are acceptable in the deployment environment; avoid confidential deal targets or sensitive diligence strategy.

Risk: The generated patent screening is preliminary and may rely on delayed or incomplete public patent data.

Mitigation: Treat the report as a first-pass screen and have qualified IP or legal professionals review findings before making legal, valuation, or investment decisions.

Risk: Risk alerts such as expiry, citation, and legal-status signals are simplified indicators rather than definitive legal conclusions.

Mitigation: Verify important patents and risk flags against authoritative patent records and specialist analysis before acting on them.

## Reference(s):

- [USPTO PatentsView API endpoint](https://api.patentsview.org/patents/query)
- [ClawHub skill page](https://clawhub.ai/golngod/skills/ip-quick-screen)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [Markdown report with an optional JSON_OUTPUT block for structured summary data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs patent portfolio statistics, technology distribution, legal-status estimates, preliminary quality indicators, and risk-warning summaries; company searches are limited to a 100-patent API page.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact changelog mentions v1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
