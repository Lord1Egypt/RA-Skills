## Description:

Finds emerging AI models, products, and repositories, then builds a keyword priority table using search-volume and trend estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyansen](https://clawhub.ai/user/zhuyansen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find recent AI products, models, and repositories, then decide which related keywords merit a page or tool. They can also supply names for keyword research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid research uses API credentials and sends queries to external providers; the instruction review does not cover the downloaded executable.

Mitigation: Review the pinned package before supplying keys, choose the accounts and sites to query, and approve the estimated cost before each paid run.

Risk: TrustMRR leads are subject to terms that forbid republishing the data.

Mitigation: Keep TrustMRR leads for internal research and exclude their product details from public reports.

## Reference(s):

- [New Term Radar on ClawHub](https://clawhub.ai/zhuyansen/skills/new-term-radar)
- [Example source configuration (v0.6.0)](https://github.com/zhuyansen/new-term-radar/blob/v0.6.0/config.example.json)
- [AIsa API key](https://go.aisa.one/yansen-zhu)
- [Optional GoAnyAPI key](https://goanyapi.com/r/ga-95708898fb)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown report and JSON keyword data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes keyword priority tables and source caveats.]

## Skill Version(s):

0.6.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
