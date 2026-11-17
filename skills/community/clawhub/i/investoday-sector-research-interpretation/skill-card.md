## Description:

Interprets sector, industry, concept, and theme research reports using Investoday finance data, summarizing sell-side consensus, core theses, disagreements, opportunities, risks, and representative directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to turn a sector, industry, concept, or theme question into a structured research interpretation report grounded in recent Investoday research sentiment data. It is intended for research summaries and does not provide investment advice, price targets, position sizing, or trading timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance-related user queries are sent through the Investoday data dependency.

Mitigation: Install and use the skill only where routing those finance queries to Investoday data tools is acceptable.

Risk: Research summaries may be mistaken for investment advice.

Mitigation: Present outputs as research summaries only and preserve the skill's restrictions against buy or sell recommendations, price targets, position sizing, or trading timing.

Risk: Limited or sparse research data can make sector-level consensus unreliable.

Mitigation: Follow the skill's evidence rules by requiring repeated evidence, stating the 90-day time window, and saying when a dimension has insufficient data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-sector-research-interpretation)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language sector research report with sections for conclusion, research theses, consensus and disagreement, key directions, opportunities and risks, follow-up observations, and a summarized conclusion.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
