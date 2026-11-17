## Description:

Creates leader AI skills that analyze authorized workplace material to simulate leadership style, support upward-management planning, and generate career or replacement-path guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and career-focused users use this skill to build a local leader profile from authorized workplace materials, then request leadership simulation, upward communication advice, and career-growth planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect sensitive workplace messages, documents, meetings, and credentials.

Mitigation: Use only data you are authorized to access, avoid private-chat or OAuth collection without explicit organizational and affected-person authorization, and avoid storing real tokens or private communications until credential storage and retention controls are fixed.

Risk: Local file operations may create, update, roll back, or delete leader-skill directories using user-provided slugs and paths.

Mitigation: Run in an isolated workspace, review slugs and output paths before execution, keep backups, and do not use deletion or rollback commands until path containment and deletion safeguards are verified.

Risk: Leader profiling and replacement-path guidance can be misused for harassment, defamation, privacy invasion, or unfair workplace conduct.

Mitigation: Use the skill only for lawful personal learning, self-improvement, and career development; do not spread unverified negative claims or use outputs for malicious attacks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/skills/leader-skill)
- [Publisher profile](https://clawhub.ai/user/zhuqingsonga)
- [Artifact metadata homepage](https://github.com/zhuqingsonga/create--leader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated local skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English/Chinese responses; may write leader profile files under local leaders/{slug} directories after user confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; source skill frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
