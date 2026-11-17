## Description:

Captures learnings, errors, and corrections in markdown logs so agents can preserve fixes, feature requests, and recurring workflow improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q262045312-ui](https://clawhub.ai/user/q262045312-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record command failures, user corrections, missing capabilities, and better approaches into structured learning files for later review or promotion into project memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning logs and promoted memory can persist incorrect, sensitive, or overbroad guidance into future agent context.

Mitigation: Keep logs project-local, redact secrets and personal data, and require explicit human approval before promoting entries into instruction or workspace memory files.

Risk: Global or broad hook configuration can inject reminders or error-detection context outside the intended project scope.

Mitigation: Prefer project-level hooks, avoid global hooks unless needed, and use narrow hook matchers with reviewed script paths.

Risk: Captured command output, user corrections, or API failure details may contain sensitive operational information.

Mitigation: Review learning entries before sharing or committing them, and remove credentials, personal data, and unnecessary environment details.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional hook/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning log entries and setup guidance; no direct API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
