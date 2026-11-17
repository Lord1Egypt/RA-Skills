## Description:

Predict the likely gender associated with a first name with optional country-specific calibration via genderize.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to estimate likely gender distributions for first names, including country-specific calibration where an ISO 3166-1 alpha-2 country code is supplied. Typical uses include marketing personalization, demographic analysis, research on name-gender associations, and form pre-filling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First names and optional country codes are sent to a third-party Pipeworx genderize endpoint.

Mitigation: Avoid regulated, customer, or employee data unless the organization has approved that processing.

Risk: The setup uses an unpinned npm bridge that may execute mutable code.

Mitigation: Pin mcp-remote to a reviewed exact version or run it in a restricted environment.

## Reference(s):

- [Pipeworx Genderize Pack](https://pipeworx.io/packs/genderize)
- [Pipeworx Genderize MCP Endpoint](https://gateway.pipeworx.io/genderize/mcp)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-genderize)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON examples; tool responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the example call and uses an MCP remote setup for agent integration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
