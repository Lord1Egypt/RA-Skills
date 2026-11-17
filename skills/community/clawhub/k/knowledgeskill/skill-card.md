## Description:

Records document summaries, user-selected topic categories, and original links into a fixed WeCom smart sheet knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuan1221](https://clawhub.ai/user/tangsuan1221)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and knowledge workers use this skill to archive document names, concise summaries, source links, and user-confirmed categories into a WeCom smart sheet knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent records to a fixed enterprise WeCom smart sheet.

Mitigation: Use it only with a WeCom sheet you control or trust, and confirm the destination before each write.

Risk: The documented shell-command pattern can include user-controlled titles, URLs, categories, and summaries.

Mitigation: Avoid executing raw shell commands with unescaped user input; prefer structured tool calls or validate and escape fields before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuan1221/skills/knowledgeskill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise summaries, category-confirmation prompts, WeCom smart sheet write commands, and completion messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
