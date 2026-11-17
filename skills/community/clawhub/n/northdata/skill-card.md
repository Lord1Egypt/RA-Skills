## Description:

NorthData helps agents use the NorthData CLI or MCP server to look up German company registry, ownership, representative, financial, publication, and person records while controlling API credit spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p-meier](https://clawhub.ai/user/p-meier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to choose safe NorthData lookup workflows for German company research, ownership and management checks, financial review, publications, person records, and scoped lead searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NorthData lookups may spend paid API credits, especially when search result limits are high.

Mitigation: Start with free suggest, reference, and billing checks; dry-run billed calls; keep limits low; require explicit approval for higher-cost searches.

Risk: The skill can retrieve business and person records from NorthData.

Mitigation: Use the guidance for targeted, necessary lookups and review retrieved records before relying on them.

## Reference(s):

- [NorthData API docs](https://github.com/northdata/api)
- [ClawHub skill page](https://clawhub.ai/p-meier/skills/northdata)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses free checks, dry-runs, low result limits, and explicit approval before higher-cost searches.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
