## Description:

Guild Knowledge helps OpenClaw agents manage experience documents by reading Guild docs, searching current information, and comparing stored guidance with newer alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiy416](https://clawhub.ai/user/pipiy416)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to keep project experience documents useful while making technical decisions. It prompts agents to consult relevant Guild documents, search for current information, compare older guidance with newer options, and propose document updates that require user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate automatically on broad phrases and may read local Guild documents or send task-related search queries externally.

Mitigation: Narrow or disable auto-triggers, use explicit /guild commands where possible, and require confirmation before web searches or changes to Guild documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipiy416/skills/guild-knowledge)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bilingual Chinese and English guidance, comparisons, command examples, and update recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guild document changes require user approval; web searches and auto-triggered workflows should be reviewed before use.]

## Skill Version(s):

1.0.1 (source: server release, frontmatter, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
