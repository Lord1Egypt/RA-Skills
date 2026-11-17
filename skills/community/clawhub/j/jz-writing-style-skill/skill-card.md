## Description:

Reusable writing-style skill template that learns from a user's edits, extracts style rules, and updates SKILL.md so future drafts better match the user's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to customize an agent's writing style and capture recurring edits as reusable writing rules. It supports workflows where an agent drafts content, the user revises it, and helper scripts record the before-and-after text for later style improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts and final edits may be stored on disk and may contain sensitive or client material.

Mitigation: Use the skill only with non-confidential content unless redaction, retention limits, and explicit approval controls are added.

Risk: The improvement workflow may send draft and edit data through the configured LLM CLI.

Mitigation: Confirm the configured LLM command and data handling policy before running extraction on private or regulated content.

Risk: Auto mode can rewrite SKILL.md from generated proposals.

Mitigation: Review proposals and diffs before applying changes, and avoid unattended auto mode for production skills.

## Reference(s):

- [Writing Style Skill on ClawHub](https://clawhub.ai/jzocb/skills/jz-writing-style-skill)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated proposal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can store original and final draft text locally and can update SKILL.md after review or auto mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
