## Description:

Magneto Skill Master guides agents through locating, downloading, auditing, adapting, installing, and verifying external Agent Skills from GitHub or Gitee for WorkBuddy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yehuzi2026](https://clawhub.ai/user/yehuzi2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to install external Agent Skills through a structured workflow that audits source repositories, adapts skill format, installs dependencies, and reports installation status and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to fetch and install third-party skill repositories with broad local changes.

Mitigation: Use it only when intentionally installing a specific external repository, and confirm the target repository, commit, files to copy, dependencies, and script execution before proceeding.

Risk: Dependency installation or script execution from untrusted requirements can affect the local environment.

Mitigation: Review files before execution and use a disposable or managed environment with pinned dependencies before running install commands.

Risk: The security evidence classifies the release as suspicious because it teaches broad local changes and weakened sandboxing.

Mitigation: Do not let the skill disable sandboxing or run package installation on untrusted inputs without explicit user approval and a full file review.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yehuzi2026/skills/magneto-skill-master)
- [Audit patterns](artifact/references/audit_patterns.md)
- [Run script template](artifact/references/run_script_template.sh)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source, audit conclusions, install path, dependency status, and usage tips after installation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
