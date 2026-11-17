## Description:

Trivia questions from the Open Trivia Database, with 4,000+ questions across 24 categories and difficulty levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to fetch Open Trivia Database questions, list categories, and get category statistics for trivia games, quiz apps, team activities, and educational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an unpinned npm package automatically through mcp-remote@latest.

Mitigation: Pin mcp-remote to a reviewed exact version, run it in a restricted environment, and keep credentials or sensitive environment variables out of that process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-trivia)
- [Pipeworx trivia homepage](https://pipeworx.io/packs/trivia)
- [Pipeworx trivia MCP endpoint](https://gateway.pipeworx.io/trivia/mcp)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool calls can return trivia question text, answer choices, correct answers, categories, difficulty, and category statistics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
