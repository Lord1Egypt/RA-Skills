## Description:

COVID-19 statistics — global totals, per-country breakdowns, historical trends, and vaccination data from disease.sh

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current and historical COVID-19 statistics, compare country-level data, and inspect vaccination totals through the Pipeworx disease MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes statistics queries through the Pipeworx gateway.

Mitigation: Install only if sharing those queries with the Pipeworx gateway is acceptable.

Risk: The MCP configuration runs an unpinned npm package with mcp-remote@latest.

Mitigation: Pin mcp-remote to a reviewed version or run it in a restricted environment before use.

## Reference(s):

- [Pipeworx disease homepage](https://pipeworx.io/packs/disease)
- [Pipeworx disease MCP endpoint](https://gateway.pipeworx.io/disease/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-disease)
- [Publisher profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include COVID-19 statistics retrieved through the remote Pipeworx disease MCP endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
