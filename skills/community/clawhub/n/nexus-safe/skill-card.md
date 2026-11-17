## Description:

Nexus Safe provides local system health monitoring, diagnostic log retrieval, and policy-controlled Docker or PM2 service restarts without runtime outbound network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to inspect local host health, review Docker or PM2 service logs, and perform constrained service recovery when local policy allows it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service recovery can report a restart as successful even when the underlying Docker or PM2 restart fails.

Mitigation: Keep recovery disabled unless explicit allowlists are configured, verify service health after any restart, and treat recovery audit entries as incomplete until restart failures are surfaced.

Risk: The skill executes local Docker and PM2 commands against named services.

Mitigation: Run it only in an isolated, trusted environment with a pinned psutil dependency and narrow service allowlists.

## Reference(s):

- [Nexus Safe on ClawHub](https://clawhub.ai/mrnsmh/skills/nexus-safe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local status, log, and recovery commands when enabled by environment policy.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata; artifact files state 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
