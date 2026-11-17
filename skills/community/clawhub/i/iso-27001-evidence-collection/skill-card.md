## Description:

Collect, organize, and validate timestamped evidence packages for ISO 27001 and SOC 2 audits using API-first CLI guidance across major cloud platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT

## Use Case:

Security, compliance, and engineering teams use this skill to prepare audit evidence packages, refresh stale evidence, and identify gaps before ISO 27001:2022 or SOC 2 auditor review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collected audit evidence can contain sensitive security, identity, access, and configuration data.

Mitigation: Store outputs in encrypted, access-controlled evidence locations, redact unnecessary sensitive fields before sharing, and define retention and deletion rules.

Risk: Evidence collection commands may access production cloud, identity, repository, and endpoint systems using local credentials.

Mitigation: Review each command before execution and run it with least-privilege read-only accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/iso-27001-evidence-collection)
- [Internal ISO Audit](https://internalisoaudit.com)
- [Connector guidance](CONNECTORS.md)
- [API export commands](rules/api-exports.md)
- [Evidence types by control domain](rules/evidence-types.md)
- [Screenshot evidence guide](rules/screenshot-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and evidence index examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped evidence collection commands and auditor-ready index guidance; the skill itself executes no scripts.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
