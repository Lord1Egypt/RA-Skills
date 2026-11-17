## Description:

Checks a list of patent numbers and summarizes whether each is in force, lapsed, or pending, including lapse reasons and estimated expiry years.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business professionals use this skill to batch-check patent legal status when reviewing contracts, filings, or supporting materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential protection and cache-file handling flaws warrant review before installation.

Mitigation: Avoid sharing paid keys in chat; use protected credential configuration, and prefer a version that validates patent identifiers, confines cache paths, and blocks unsafe authenticated redirects.

Risk: Patent numbers and query terms are sent to PatentMax, and calls can consume account credit.

Mitigation: Tell users before paid calls and use a task spending limit where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/patent-legal-status)
- [PatentMax API](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Excel-compatible CSV checklist]

**Output Parameters:** [One row per supplied patent number, with legal status, lapse reason, estimated expiry year, and related patent details.]

**Other Properties Related to Output:** [Preserves the supplied order and includes entries that could not be found. Patent numbers and query terms are sent to PatentMax; requests may consume account credit.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
