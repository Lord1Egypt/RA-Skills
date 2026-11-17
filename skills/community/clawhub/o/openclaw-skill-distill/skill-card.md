## Description:

Strip any local project into a clean, publishable agent skill by scanning for hardcoded paths and secrets, scaffolding standard structure, and validating before publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchangxu1989-openclaw](https://clawhub.ai/user/yuchangxu1989-openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to turn an existing local project into a generalized, publishable ClawHub skill. It helps scan for local traces, scaffold a standard skill directory, validate publishing requirements, and prepare for a manual publish step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan output can expose secrets, local paths, or other sensitive project details in terminal or agent logs.

Mitigation: Run scans only on projects whose contents may be shown in logs, avoid live .env files, and replace sensitive values with placeholders before scanning.

Risk: Scaffolding can write files outside the intended local skill directory if the requested skill name contains path components.

Mitigation: Use a simple skill name without slashes or path traversal, and manually inspect the scaffolded directory before publishing.

Risk: The publish step can release an insufficiently reviewed skill.

Mitigation: Require explicit confirmation before running clawhub publish and review validation results, generated files, and checklist items first.

## Reference(s):

- [Skill Distill checklist](artifact/references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/yuchangxu1989-openclaw/skills/openclaw-skill-distill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash commands and shell-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local scan findings, scaffolded skill files, validation results, and publish-readiness guidance.]

## Skill Version(s):

0.2.0 (source: server release metadata, created 2026-04-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
