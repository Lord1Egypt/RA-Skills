## Description:

NumbersAPI MCP - wraps numbersapi.com (free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users can connect this MCP skill to retrieve number, date, math, and random facts from NumbersAPI without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection command uses an auto-approved, unpinned npm package that may execute future package contents locally.

Mitigation: Pin mcp-remote to a reviewed exact version or run the MCP client in a restricted environment before installation.

## Reference(s):

- [Pipeworx NumbersAPI pack](https://pipeworx.io/packs/numbersapi)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-numbersapi)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text facts and JSON MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required; exposes number_fact, date_fact, math_fact, and random_fact tools.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
