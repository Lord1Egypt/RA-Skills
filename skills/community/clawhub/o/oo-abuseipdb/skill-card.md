## Description:

Use an OOMOL-connected account to search and read AbuseIPDB data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use this skill to check IP addresses or CIDR blocks, retrieve reports, and read the AbuseIPDB blacklist through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unchecked downloaded software or make broader agent changes without clear approval.

Mitigation: Review and approve CLI installation separately, preferably using a verified release. Inspect or disable automatic skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

Risk: OOMOL mediates queries and holds the connected AbuseIPDB credentials.

Mitigation: Use the connected service through the documented account flow, and do not place raw credentials in prompts or command payloads.

## Reference(s):

- [AbuseIPDB API documentation](https://docs.abuseipdb.com/)
- [AbuseIPDB](https://www.abuseipdb.com/)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on the connected AbuseIPDB account and current service data.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
