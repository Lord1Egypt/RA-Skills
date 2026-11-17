## Description:

Fetch Bible verses, passages, and random scripture from bible-api.com with multiple translations supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Bible verses, retrieve passages, or request random scripture for devotional apps, Bible study tools, newsletters, social posts, and conversational reference checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm package at startup.

Mitigation: Pin mcp-remote to a reviewed version or run the skill through a controlled install process.

Risk: The remote MCP setup has more local execution authority than the simple API lookup task requires.

Mitigation: Use least-privilege sandboxing and limit environment access before installation or deployment.

## Reference(s):

- [Pipeworx Bible pack](https://pipeworx.io/packs/bible)
- [Pipeworx Bible MCP endpoint](https://gateway.pipeworx.io/bible/mcp)
- [ClawHub skill listing](https://clawhub.ai/brucegutman/skills/pipeworx-bible)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns verse text with translation, book, chapter, and verse metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
