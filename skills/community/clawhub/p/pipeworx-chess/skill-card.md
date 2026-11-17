## Description:

Chess.com player profiles, game stats, match archives, and leaderboards from the public API

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, coaches, and chess community tool builders use this skill to retrieve public Chess.com player profiles, ratings, monthly game archives, and leaderboards without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses a remote MCP gateway and downloads mcp-remote at runtime with an unpinned latest version.

Mitigation: Install only after reviewing the remote MCP gateway and npm package; prefer pinning mcp-remote to a reviewed version.

Risk: The MCP client may have access to local files, environment variables, or credentials depending on how it is run.

Mitigation: Run the MCP client with least-privilege access and avoid exposing unnecessary local files, environment variables, or credentials.

## Reference(s):

- [Pipeworx Chess homepage](https://pipeworx.io/packs/chess)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets; tool responses contain public Chess.com data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No authentication is required for the Chess.com public API data described by the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
