## Description:

US FDA open data - adverse drug event reports, drug labeling/package inserts, and food recall enforcement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and safety reviewers use this skill to query public FDA datasets for adverse drug event reports, drug labeling/package inserts, and food recall enforcement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the MCP configuration can run mutable npm code through npx.

Mitigation: Review the skill before installing and prefer a pinned mcp-remote version or a controlled/self-hosted setup.

Risk: Health-related search terms may be sent to a third-party gateway.

Mitigation: Avoid sending patient identifiers, secrets, proprietary research terms, or other sensitive health-related information through the skill.

## Reference(s):

- [Pipeworx FDA Pack](https://pipeworx.io/packs/fda)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-fda)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FDA search guidance and MCP configuration; direct examples require curl.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
