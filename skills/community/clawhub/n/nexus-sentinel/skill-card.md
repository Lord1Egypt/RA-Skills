## Description:

Nexus Sentinel is an autonomous SRE agent skill for monitoring server health, rotating logs, diagnosing service failures, coordinating guarded recovery, and preparing configuration backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:


## Use Case:

Developers and SRE operators use this skill to inspect service health, summarize operational status, diagnose Docker or PM2 service errors, and propose controlled recovery or backup actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect files, services, backups, and outbound notifications in an SRE environment.

Mitigation: Limit deployment to controlled SRE environments with approved services, paths, destinations, and explicit review before cleanup, restart, backup, or external notification actions.

Risk: Log-derived content or configuration backups could expose sensitive information through cloud backup or WhatsApp notification paths.

Mitigation: Require explicit approval and apply redaction plus content-based secret detection before sending logs, notifications, or backup content externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrnsmh/skills/nexus-sentinel)
- [README](artifact/README.md)
- [Artifact Metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and JSON-like status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference host service logs, environment configuration, backup paths, and outbound notification settings.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
