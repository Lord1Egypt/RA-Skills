## Description:

Palo Alto Prisma Access SASE audit for security policy evaluation across mobile users and remote networks, GlobalProtect Cloud Service configuration review, service connection validation, threat prevention profile assessment, and Strata Cloud Manager posture analysis across Prisma Access tenants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and network security teams use this skill to audit Prisma Access SASE posture, including mobile user policies, remote network tunnels, threat prevention profile coverage, service connections, decryption, and logging visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Prisma Access API credentials and can read tenant configuration and operational telemetry.

Mitigation: Use a dedicated least-privilege audit account, avoid sharing secrets in chat or URLs, redact tokens from logs, and rotate credentials if exposure is suspected.

Risk: Audit output may include sensitive tenant topology, policy, tunnel, route, and logging details.

Mitigation: Restrict report distribution and redact tenant IDs, routes, tunnel endpoints, user regions, and security policy details before sharing externally.

Risk: Findings may be incomplete if the wrong management plane is queried or the audit account lacks required read permissions.

Mitigation: Confirm whether Strata Cloud Manager or legacy Panorama Cloud Services is authoritative and use a view-only account with the required tenant scope.

## Reference(s):

- [Prisma Access API Reference](artifact/references/api-reference.md)
- [ClawHub skill release page](https://clawhub.ai/vahagn-madatyan/skills/prisma-access-audit)
- [Strata Cloud Manager API endpoint](https://api.sase.paloaltonetworks.com/sse/config/v1)
- [Prisma Access Insights API endpoint](https://pa-<region>.api.prismaaccess.com/api/sase/v2.0)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration review]

**Output Format:** [Markdown with inline HTTP request examples and audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit workflow requiring Prisma Access API credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
