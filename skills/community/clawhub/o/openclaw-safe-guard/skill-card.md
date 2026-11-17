## Description:

Provides static security scanning for OpenClaw skills, checking permission risks, suspicious code patterns, dependency risks, and producing Chinese-language risk assessment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansengu11](https://clawhub.ai/user/ansengu11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit installed or candidate OpenClaw skills before use, with emphasis on permissions, network access, shell behavior, dependencies, and review recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read installed OpenClaw skill directories, which may expose sensitive data embedded in other skills.

Mitigation: Run it as a non-root user in an isolated environment and review which skill directories are available before scanning.

Risk: The skill contacts GitHub and may clone public repositories into temporary local storage.

Mitigation: Use network access only where GitHub lookups are expected, and inspect or clean temporary workspace data after use.

Risk: Server security evidence flags a comparison command that can be steered outside declared skill directories and copy readable files into predictable /tmp locations.

Mitigation: Avoid the compare command with untrusted skill names until path validation and mktemp-based temporary directories are fixed.

Risk: Non-interactive mode can skip confirmation prompts before scanning.

Mitigation: Avoid OPENCLAW_NONINTERACTIVE=true unless the execution environment and target inputs have already been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ansengu11/skills/openclaw-safe-guard)
- [Publisher profile](https://clawhub.ai/user/ansengu11)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown security assessment report with tables, risk scoring, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English interface text; scans are static and depend on installed command-line tools.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
