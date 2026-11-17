## Description:

Manage OVHcloud services via API for domains, DNS records, VPS, cloud instances, dedicated servers, email, SSL certificates, billing, and related service operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushp1997](https://clawhub.ai/user/pushp1997)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and manage OVHcloud account resources, including domains, DNS zones, VPS instances, cloud projects, dedicated servers, SSL certificates, bills, and orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make immediate changes to live OVH account resources, including DNS records and server power actions, using broad OVH credentials.

Mitigation: Use least-privileged OVH consumer keys, keep separate read-only and write credentials where possible, and manually confirm destructive or availability-impacting operations before execution.

Risk: The setup guidance relies on installing the OVH Python SDK without a pinned version.

Mitigation: Pin and review the OVH Python SDK dependency before using the bundled CLI in a managed environment.

## Reference(s):

- [OVH API token creation](https://ca.api.ovh.com/createToken/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI supports a --json flag for machine-readable OVH API responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
