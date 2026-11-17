## Description:

Local OpenClaw workflow skill for operating Xiaohongshu / RED through a local MCP server and mcporter, including search, note detail retrieval, comments, replies, image publishing, video publishing guidance, reusable shell scripts, and publish templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomilizhipeng](https://clawhub.ai/user/xiaomilizhipeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and OpenClaw users use this skill to search Xiaohongshu content, inspect notes and comments, manage comments or replies, and prepare or publish Xiaohongshu posts through a local MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Xiaohongshu posts and submit comments or replies from an authenticated account.

Mitigation: Review every generated post or comment before execution and use private visibility for test publishes.

Risk: The local MCP service uses persistent Xiaohongshu login and browser session data.

Mitigation: Install only when the Docker image publisher is trusted and restrict access to the persisted cookie and browser-profile volumes.

Risk: The Docker image reference is not pinned to a reviewed digest.

Mitigation: Pin the container image to a reviewed digest before production or sensitive-account use.

Risk: Untrusted text or identifiers passed into helper scripts may be unsafe until JSON serialization is reviewed.

Mitigation: Avoid passing untrusted inputs to the scripts and review or fix JSON argument construction before broad use.

## Reference(s):

- [Setup](references/setup.md)
- [OpenClaw Xiaohongshu MCP on ClawHub](https://clawhub.ai/xiaomilizhipeng/skills/openclaw-xiaohongshu-mcp)
- [xiaomilizhipeng publisher profile](https://clawhub.ai/user/xiaomilizhipeng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local MCP tools that return Xiaohongshu search results, note details, comments, or publish responses.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
