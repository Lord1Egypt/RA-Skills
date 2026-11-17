## Description:

Analyzes public fund performance, risk-return fit, holdings, manager history, fees, and dividends using Investoday finance data, then produces a structured fund diagnosis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis agents use this skill to evaluate a public fund by name or 6-digit fund code across returns, risk, holdings, manager tenure, fees, dividends, and follow-up monitoring points. The output is reference analysis and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund analysis may be mistaken for personalized investment advice.

Mitigation: Present conclusions as reference analysis, confirm important findings against official fund disclosures, and consult a qualified advisor before making investment decisions.

Risk: Fund-name matching can be ambiguous when a user provides only a partial or common fund name.

Mitigation: Prefer a 6-digit fund code or ask the user to confirm the exact fund before running the full diagnosis.

Risk: Broad fund-analysis requests may trigger calls to the Investoday finance-data dependency.

Mitigation: Use the skill for specific public fund names or codes and review dependency behavior before installation or deployment.

## Reference(s):

- [Artifact Skill Definition](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/kenneth-bro/skills/investoday-fund-comprehensive-diagnosis)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown structured fund diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the investoday-finance-data dependency for public fund data; findings should be treated as reference analysis, not investment advice.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
