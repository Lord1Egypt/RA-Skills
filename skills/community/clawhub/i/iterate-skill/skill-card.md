## Description:

Automates multi-round code review and iteration with parallel dimension reviews, a defensive-programming mode, and cross-assistant installation and updates with SHA-256 verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingzhao-l](https://clawhub.ai/user/jingzhao-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to have an AI assistant review and improve a codebase through repeated review, fixes, and validation, or to complete incremental coding tasks with defensive checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence and reports gaps between its stated purpose and capabilities involving signing credentials, publishing, network access, and file changes. Its inspection coverage is partial.

Mitigation: Follow the security guidance: independently review credential handling, publishing, update, and sensitive-file behavior before installing. If proceeding, use a disposable project, withhold signing and publishing credentials until reviewed, and inspect proposed file changes and network or publishing destinations.

## Reference(s):

- [Iterate on ClawHub](https://clawhub.ai/jingzhao-l/skills/iterate-skill)
- [Agent Skills specification](https://agentskills.io/)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration]

**Output Format:** [Code edits, Markdown review reports, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review dimensions and iteration rounds are configurable; merge and push are opt-in.]

## Skill Version(s):

3.19.0 (source: release evidence, artifact/SKILL.md, artifact/pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
