## Description:

Search and read DNSFilter data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External DNSFilter users and administrators can use this skill to inspect account information, IP addresses, networks, policies, and domain or application categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified installers.

Mitigation: Review setup first and approve a verified CLI release separately.

Risk: DNSFilter access passes through OOMOL.

Mitigation: Understand and review the connected-account access path before use.

Risk: Startup skill synchronization can introduce broader agent changes.

Mitigation: Control which additional skills are installed; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization.

## Reference(s):

- [DNSFilter API documentation](https://api.dnsfilter.com/docs)
- [DNSFilter](https://www.dnsfilter.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented DNSFilter queries; action schemas are checked before a request is built.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
