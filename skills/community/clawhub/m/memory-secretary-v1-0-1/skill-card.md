## Description:

记忆秘书 manages and analyzes local OpenClaw memory files, providing memory quality checks, repeated-task detection, success-case extraction, work-pattern analysis, smart reminders, and shareable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhm2084](https://clawhub.ai/user/yhm2084)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local memory files, avoid repeated work, identify reusable successful cases, analyze recurring work patterns, generate reminders, and produce reports for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw memory files and writes derived reports.

Mitigation: Install only in workspaces where the agent is allowed to inspect memory contents, and review generated reports before sharing them.

Risk: The packaged tests can execute Python files from paths outside the package.

Mitigation: Run tests only in an isolated workspace or after reviewing and correcting test paths.

Risk: The installation documentation encourages using a force flag to bypass security warnings.

Mitigation: Do not use the force flag as a substitute for review; rely on scanner results, source review, and workspace isolation before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhm2084/skills/memory-secretary-v1-0-1)
- [Publisher profile](https://clawhub.ai/user/yhm2084)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python usage examples and structured local analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local workspace memory files and writes derived reports under the workspace memory area.]

## Skill Version(s):

1.0.1 (source: evidence.release.version, artifact/SKILL.md, artifact/README.md, artifact/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
