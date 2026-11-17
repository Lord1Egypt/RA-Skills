## Description:

B2B prospecting and lookalike intelligence powered by Ocean.io, helping agents find similar companies, identify decision-makers, and export enriched prospect lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mokto](https://clawhub.ai/user/mokto)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, go-to-market, and business development teams use this skill to build B2B prospect lists, find lookalike accounts, identify relevant contacts, and export enriched company or people records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Ocean.io API token is configured in the MCP URL query string, which can expose credentials through logs, browser history, or copied configuration.

Mitigation: Use a limited or dedicated Ocean.io API token, avoid sharing resolved MCP URLs, monitor credit usage, and rotate the token after use in environments that may log URLs.

Risk: Search and export operations consume paid Ocean.io credits at 0.2 credits per returned or exported record.

Mitigation: Confirm record counts and estimated credit cost with the user before running searches or exports, and keep result limits scoped to the requested workflow.

## Reference(s):

- [Ocean Io on ClawHub](https://clawhub.ai/mokto/skills/ocean-io)
- [mokto publisher profile](https://clawhub.ai/user/mokto)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown tables, natural-language guidance, and download URLs for exported CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and export actions consume Ocean.io credits; the skill instructs agents to confirm estimated credit cost before searches or exports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
