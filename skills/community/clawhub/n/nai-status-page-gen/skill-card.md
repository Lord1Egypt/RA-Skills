## Description:

Generate a lightweight static HTML status page for self-hosted services that checks health endpoints, ping, SSL certificates, and uptime history, then outputs a self-contained dark-theme HTML file that can be served locally or pushed to a GitHub Gist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure health checks for self-hosted services, generate uptime and certificate status data, and publish a lightweight static status page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring health checks can create persistent network traffic to configured services.

Mitigation: Limit checks to services you own or administer, set an appropriate schedule, and document how to disable the cron or LaunchAgent job.

Risk: Publishing the status page publicly can reveal service names, endpoints, availability, and operational patterns.

Mitigation: Prefer local or private hosting for internal services, and review generated content before using public Gist or other public hosting.

Risk: Shared /tmp paths in examples can be overwritten or read by other local users on multi-user systems.

Mitigation: Use per-user private output paths with restrictive permissions for check results and certificate data.

Risk: Running scheduled checks with elevated privileges can broaden the impact of compromised configuration or scripts.

Mitigation: Run the scheduler as an unprivileged user and keep the skill directory and service configuration writable only by trusted users.

## Reference(s):

- [status-page-gen Setup Guide](references/setup-guide.md)
- [ClawHub skill release page](https://clawhub.ai/newageinvestments25-byte/skills/nai-status-page-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated HTML status-page files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact scripts can write JSON check results, uptime history, and a self-contained HTML page.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
