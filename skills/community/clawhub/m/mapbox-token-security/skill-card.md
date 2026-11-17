## Description:

This skill gives security guidance for Mapbox access tokens, including scope management, URL restrictions, rotation strategies, secure storage, monitoring, and incident response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and security reviewers use this skill when creating, auditing, rotating, or responding to incidents involving Mapbox access tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested token revocation or rotation steps can disrupt production services if applied before dependencies are updated.

Mitigation: Review changes before applying them, create replacement tokens first, verify rollout, monitor for 24-48 hours, then revoke old tokens.

Risk: Incorrect token type, scopes, or URL restrictions can expose secret access or allow unauthorized token use.

Mitigation: Use public tokens only for client or mobile contexts, keep secret tokens server-side, grant least-privilege scopes, and restrict public tokens to expected domains.

## Reference(s):

- [Incident Response & Common Mistakes](references/incident-response.md)
- [Token Rotation & Monitoring](references/rotation-monitoring.md)
- [ClawHub Skill Page](https://clawhub.ai/mapbox/skills/mapbox-token-security)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; it does not access, collect, or modify credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
