## Description:

Search OneHome (CoreLogic) portal listings, get property details, photos, schools, saved searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and home buyers use this skill to work with OneHome portal listings shared by a real-estate agent, including saved groups, listing details, photos, school information, walkability, comparisons, and local mortgage calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OneHome tools can access private OneHome portal listings and buyer-specific data.

Mitigation: Install and use the skill only when the user intends to grant access to their OneHome portal data.

Risk: Magic-link tokens or bearer tokens may expose private portal access if shared or retained unnecessarily.

Mitigation: Avoid sharing or storing expired or unnecessary tokens, and refresh credentials when the health check indicates expiry.

Risk: Raw GraphQL requests can retrieve fields outside the structured tool workflow.

Mitigation: Prefer structured OneHome tools and use the raw GraphQL escape hatch only for specific needed fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/onehome-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured tool-call recommendations and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference private OneHome portal tokens and property data supplied by the user.]

## Skill Version(s):

0.12.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
