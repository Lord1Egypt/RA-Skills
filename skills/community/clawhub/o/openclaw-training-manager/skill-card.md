## Description:

Manage and optimize your OpenClaw training workspace -- scaffold files, generate skills, log training sessions, and validate workspace structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anova44](https://clawhub.ai/user/anova44)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to set up personalized agent workspace files, log training corrections, validate workspace structure, generate simple skills, analyze maintenance needs, and export backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent instruction and memory files, which may alter future agent behavior.

Mitigation: Review generated or logged content before relying on it, and validate the workspace after changes.

Risk: Memory and training logs may capture secrets or sensitive personal data.

Mitigation: Avoid storing secrets or sensitive personal data in memory or daily logs.

Risk: File-write behavior may break workspace boundaries in untrusted workspaces, including through symlinks.

Mitigation: Run the skill only in workspaces you created or have reviewed for unsafe links and paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anova44/skills/openclaw-training-manager)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash on Linux or macOS; writes persistent OpenClaw workspace files through included scripts.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
