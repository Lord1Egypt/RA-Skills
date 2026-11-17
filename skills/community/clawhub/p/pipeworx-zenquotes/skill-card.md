## Description:

Fetches inspirational quotes from ZenQuotes, including random quotes, a daily quote, and batches of 50 quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add inspirational quotes to meetings, newsletters, quote-of-the-day widgets, notifications, motivational feeds, or journaling applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs mcp-remote@latest through npx, which can execute a mutable npm package locally.

Mitigation: Pin mcp-remote to a reviewed version or use a controlled dependency workflow before enabling the skill in environments with sensitive files, credentials, or business data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-zenquotes)
- [Pipeworx ZenQuotes pack](https://pipeworx.io/packs/zenquotes)
- [Pipeworx ZenQuotes MCP endpoint](https://gateway.pipeworx.io/zenquotes/mcp)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text or JSON quote responses, with Markdown guidance and JSON MCP configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples; MCP setup uses npx with mcp-remote to connect to the Pipeworx gateway.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
