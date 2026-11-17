## Description:

Compliance-first orthopedic expo contact lookup for querying exhibitor and attendee records from AAOS, OMTEC, DKOU, AAHKS, AOSSM, and SOFCOT with registration, an anti-harassment pledge, quotas, blocklist checks, and hash-chained audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

External business users and agents use this skill to register a lookup user, build a local expo-contact index, and query orthopedic exhibitor or attendee contacts for targeted, compliance-aware business outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and searches personal contact data, and server security evidence notes that access controls, quotas, blocklist controls, and audit claims are weaker than documented.

Mitigation: Use only in a trusted single-user or tightly controlled local environment; treat the controls as workflow reminders, restrict filesystem access, and review results before outreach.

Risk: L3 private data can be included when explicitly enabled.

Mitigation: Do not enable L3 unless there is a clear lawful basis and separate protections such as filesystem permissions, encryption, and backups.

Risk: Runtime data, registry, and audit files may contain contact data and usage history.

Mitigation: Do not publish or share data/, registry/, or audit/ outputs; exclude them from release packages and backups intended for distribution.

Risk: The optional Excel parser dependency can change over time.

Mitigation: Pin dependencies before production use and install only from trusted package sources.

## Reference(s):

- [Data Sources and Parsing Notes](references/DATA_SOURCES.md)
- [Security Audit Report](安全审计报告.md)
- [TRAC-E Pre-release Self-check](TRAC-E自查报告.md)
- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ortho-expo-contacts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only workflow; contact details are masked by default, and full reveal consumes higher quota.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
