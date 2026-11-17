## Description:

Read Bluesky profiles, posts, feeds, followers, and threads via the AT Protocol -- 8 tools, mostly public endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to read public Bluesky profiles, posts, feeds, followers, follows, and threads, and to search posts when they provide their own Bluesky credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authenticated post-search flow places a Bluesky app password in a gateway URL.

Mitigation: Avoid putting app passwords in URLs; rotate any password already exposed this way and prefer safer credential handling before use.

Risk: Requests are sent through the third-party Pipeworx gateway.

Mitigation: Use the public-read tools only when sending requests through Pipeworx is acceptable for the intended data and workflow.

Risk: The MCP client example runs mcp-remote@latest through npx.

Mitigation: Pin and review the MCP helper package version before adding the configuration to an agent client.

## Reference(s):

- [Pipeworx Bluesky Pack](https://pipeworx.io/packs/bluesky)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-bluesky)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx Bluesky MCP Endpoint](https://gateway.pipeworx.io/bluesky/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes eight Bluesky tools; most use public endpoints, while post search requires user-provided Bluesky credentials.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
