## Description:

Manage Porkbun DNS records and domains via API v3. Use when Codex needs to create, read, update, or delete DNS records on Porkbun; list domains; configure API access; work with common record types (A, AAAA, CNAME, MX, TXT, etc.). The skill includes a CLI tool `scripts/porkbun-dns.js` for executing DNS operations reliably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmantly](https://clawhub.ai/user/wmantly)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage DNS records and domain data for Porkbun-managed domains from an agent workflow. It supports API credential setup, domain listing, DNS record lookup, and create, edit, or delete operations for common DNS record types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Porkbun API credentials can change live DNS records if exposed or misused.

Mitigation: Use environment variables or a local config file with restrictive permissions, and rotate credentials when access no longer needs to be granted.

Risk: Create, edit, edit-by, delete, or delete-by commands can disrupt domain, website, or email behavior.

Mitigation: Review the target domain, record type, name, content, TTL, and priority before running mutating DNS commands.

## Reference(s):

- [DNS Record Types Reference](references/dns-record-types.md)
- [Porkbun API v3 Documentation](https://porkbun.com/api/json/v3/documentation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Porkbun DNS API operations when the user provides valid API credentials.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
