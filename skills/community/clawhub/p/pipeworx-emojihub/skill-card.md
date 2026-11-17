## Description:

Browse and fetch emojis by category or group - random picks, smileys, animals, food, flags, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch random emojis, browse emojis by category, or filter them by group for chat responses, picker components, games, creative prompts, and social media tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes mcp-remote from npm with an unpinned latest version.

Mitigation: Pin mcp-remote to a reviewed version before installation and review the package update path before enabling the skill.

Risk: The skill connects an agent to the Pipeworx remote MCP service.

Mitigation: Enable it only in environments where the Pipeworx service is acceptable, and run the MCP process with minimal filesystem and environment access.

Risk: Private data or credentials could be exposed to the MCP process if granted broad access.

Mitigation: Avoid passing secrets or private workspace data to the skill and scope agent permissions narrowly.

## Reference(s):

- [Pipeworx EmojiHub homepage](https://pipeworx.io/packs/emojihub)
- [Pipeworx EmojiHub MCP endpoint](https://gateway.pipeworx.io/emojihub/mcp)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-emojihub)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands]

**Output Format:** [Markdown with JSON and bash examples; MCP tool calls return emoji names, unicode characters, and HTML entities.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples and configures an MCP server through npx mcp-remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
