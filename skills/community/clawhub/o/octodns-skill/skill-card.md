## Description:

Manage DNS zones across multiple providers using octoDNS ("DNS as code"). Use when you need to manage DNS records in YAML format, sync DNS zones between providers, deploy DNS changes with version control, bulk-update DNS records, or migrate zones between DNS providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markjr](https://clawhub.ai/user/markjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and DNS administrators use this skill to manage provider-backed DNS zones as YAML configuration, preview changes, dump existing zones, and apply approved updates through octoDNS helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can apply changes to live DNS zones, including deleting records that are absent from the YAML desired state.

Mitigation: Dump existing zones first, run dry-run previews before every apply, review delete lines and record counts, and require explicit approval before any --doit execution.

Risk: DNS provider credentials can grant broad control over domains.

Mitigation: Use least-privilege tokens scoped to test or intended zones, store credentials in a proper secrets manager or locked-down files, and avoid exposing credentials in logs or shared configuration.

Risk: Automated dynamic DNS or webhook flows can apply incorrect or unauthorized changes without human review.

Mitigation: Avoid the webhook example as written, gate automated apply flows behind review and approval, and keep audit logs for DNS changes.

## Reference(s):

- [octoDNS documentation](https://octodns.readthedocs.io/)
- [octoDNS](https://github.com/octodns/octodns)
- [octodns-easydns provider](https://github.com/octodns/octodns-easydns)
- [DNS record format guide](references/records.md)
- [Provider migration guide](references/migration.md)
- [Dynamic DNS guide](references/dynamic-dns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DNS zone configuration, dry-run review steps, and execution commands for octoDNS workflows.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
