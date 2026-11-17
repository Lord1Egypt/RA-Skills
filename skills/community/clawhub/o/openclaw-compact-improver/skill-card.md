## Description:

Improves OpenClaw 4.2 /compact prompts by producing structured conversation summaries when users report poor compression, incomplete summaries, lost context, weak /compact formatting, or ask to improve compact prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicshliu](https://clawhub.ai/user/nicshliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to improve OpenClaw conversation compaction by applying a structured summary template that preserves requests, files, errors, pending tasks, current work, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent compact-prompt changes can alter OpenClaw behavior more broadly than intended.

Mitigation: Review the prompt before installation, apply it only where compact behavior should change, and keep a rollback path for the original OpenClaw configuration.

Risk: The summary template asks for user messages, file paths, and code snippets to be retained verbatim, which can expose secrets, private information, or proprietary code.

Mitigation: Use redaction controls or avoid the verbatim-message template for sensitive conversations.

## Reference(s):

- [Compact Prompt Template](references/compact-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/nicshliu/skills/openclaw-compact-improver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command and prompt-template blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compact-summary prompt guidance and configuration-oriented instructions for OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
