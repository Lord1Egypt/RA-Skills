## Description:

Search and read Venafi TLS Protect Cloud data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Security and certificate administrators use this skill to list and retrieve certificates and certificate requests in Venafi TLS Protect Cloud through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run downloaded code and introduce persistent agent skills.

Mitigation: Review setup first, use a reviewed CLI release, approve local installation separately, and disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not needed.

Risk: The connected account may have broader access than the task requires.

Mitigation: Connect only the Venafi account and permissions needed.

## Reference(s):

- [Venafi TLS Protect Cloud](https://www.paloaltonetworks.com/network-security/next-gen-trust-security/certificate-manager)
- [Venafi API documentation](https://docs.venafi.cloud/api/vaas-rest-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action responses and shell commands with JSON payloads; Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads certificate and certificate request records through the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
