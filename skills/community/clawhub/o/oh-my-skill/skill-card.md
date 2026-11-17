## Description:

Automatically captures successful multi-step agent workflows and drafts them into reusable skill files with optional desensitization of session text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill after complex completed workflows to preserve a repeatable process as a new reusable skill. It is most relevant when the workflow involved multiple tool calls, planning, verification, and structured output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to inspect recent session context, which can expose private data if used on sensitive conversations.

Mitigation: Use it only on sessions suitable for persistence, run the desensitization step, and avoid sessions containing secrets or private information.

Risk: Generated skills become persistent reusable agent instructions and may preserve weak scoping or incorrect guidance.

Mitigation: Review the complete generated SKILL.md before leaving it in an active skills directory.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and generated skill file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent SKILL.md files and optional supporting script, reference, or asset files.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
