## Description:

Self-Improving Skill helps agents record AI drafts and human-approved final versions, extract recurring edits as improvement rules, and update a target SKILL.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to improve writing-style or similar agent skills by pairing AI-generated originals with human-final versions, producing reviewable improvement proposals, and applying selected changes to target skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is openly self-modifying and automatic mode can persist LLM-generated changes to other SKILL.md files.

Mitigation: Avoid cron or auto mode unless changes receive human diff review before deployment; keep backups enabled and use rollback when needed.

Risk: Original and final drafts are retained locally and may be submitted to the configured LLM provider during rule extraction.

Mitigation: Use the skill only with content approved for local storage and provider submission; define retention and redaction rules for logs.

Risk: A configured LLM command can influence generated improvement proposals and applied skill changes.

Mitigation: Restrict IMPROVE_LLM_CMD to trusted commands and pin installation dependencies before scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzocb/skills/jz-self-improving-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts create JSONL logs, markdown proposals, backups, and updated SKILL.md files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [observe.py stores original and final drafts locally; improve.py may call a configured LLM CLI and can write changes to a target SKILL.md.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
