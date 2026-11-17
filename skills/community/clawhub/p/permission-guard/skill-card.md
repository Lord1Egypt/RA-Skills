## Description:

Permission Guard provides layered permission checks for agent shell commands, including dangerous command blocking, rule priority, auto-mode allowlists, denial tracking, and secret detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinnzen](https://clawhub.ai/user/sinnzen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to design or review agent permission policies that classify shell commands, block dangerous patterns, ask for confirmation, and track repeated denials before command or file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance-only permission logic may be treated as a replacement for enterprise or platform controls.

Mitigation: Keep enterprise and platform permission controls authoritative, and review any local permission rules before installation.

Risk: Broad auto-mode allowlists or bypass mode can permit commands without enough user review.

Mitigation: Restrict bypass mode to tests, and keep destructive, network, install, and privileged commands behind ask or deny rules.

Risk: Permission classification examples may be copied into local policy without environment-specific review.

Mitigation: Validate dangerous-command, secret-detection, and allowlist rules against the target environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinnzen/skills/permission-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only output; no bundled executable code or tool integration was provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
