## Description:

Jokes MCP - wraps JokeAPI v2 (free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect agents to Pipeworx joke tools for retrieving, searching, and listing JokeAPI categories and flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags automatic use of an unpinned third-party package as a supply-chain risk.

Mitigation: Pin mcp-remote to a reviewed version or use a controlled local install, then run the skill in a restricted environment without sensitive environment variables or broad filesystem access.

## Reference(s):

- [Pipeworx Jokes Pack](https://pipeworx.io/packs/jokes)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-jokes)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Text responses and JSON MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Joke content is retrieved through the configured Pipeworx MCP server; no API key is required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
