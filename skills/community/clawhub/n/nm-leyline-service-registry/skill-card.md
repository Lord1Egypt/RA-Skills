## Description:

Registers external services with health checks, quotas, and a usage logger for per-call cost and sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers managing several external services use this skill for configuration, health checks, quota tracking, failover patterns, and session-aware usage logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags undeclared local command execution and access to agent configuration logs.

Mitigation: Review command construction and local file access before use; restrict execution and log access to what the integration needs.

Risk: Session data and selected files may be handled by external service providers.

Mitigation: Review provider data handling and avoid sending sensitive files or session data unless authorized.

Risk: The security scan was partial because a referenced local path was missing.

Mitigation: Review the missing path and rerun a complete security scan before relying on the assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-service-registry)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands, JSON]

**Output Format:** [Markdown with Python, YAML, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and templates may require adaptation to the target service CLI and environment.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
