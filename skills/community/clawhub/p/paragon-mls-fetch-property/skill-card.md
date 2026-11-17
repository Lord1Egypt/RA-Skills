## Description:

Fetch a single property from Paragon MLS by MLS number and system ID, including parsed address, price, beds, baths, rents, taxes, and listing links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and real-estate analysis agents use this skill to retrieve and summarize one Paragon MLS listing by MLS number and system ID. It is intended for single-property lookups, not portfolio analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on unreviewed MCP code at a hardcoded local path.

Mitigation: Use only after auditing the external paragon-mls-mcp source, package metadata, lockfile, dependencies, build scripts, and generated dist/index.js.

Risk: The build script runs npm install and npm run build outside the reviewed package.

Mitigation: Prefer a release that includes the MCP source and lockfile inside the reviewed package or pins the external implementation to a verifiable revision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/paragon-mls-fetch-property)
- [Publisher profile](https://clawhub.ai/user/earlvanze)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and parsed property details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the configured paragon-mls MCP tool.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
