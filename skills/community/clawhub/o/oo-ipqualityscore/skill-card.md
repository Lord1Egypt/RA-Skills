## Description:

Connects agents to IPQualityScore lookups for IP reputation, URL risk, email validation, and phone validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to check IP reputation, scan URLs, and validate email addresses or phone numbers through their connected IPQualityScore account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified software or make broader agent changes.

Mitigation: Review setup before installing; prefer a separately approved, version-pinned CLI installation with verified integrity, and consider disabling bundled-skill synchronization using the documented control.

Risk: Lookup data is sent through OOMOL to IPQualityScore.

Mitigation: Submit only lookup data you intend to share with those services.

## Reference(s):

- [IPQualityScore API documentation](https://www.ipqualityscore.com/documentation/overview)
- [IPQualityScore](https://www.ipqualityscore.com/)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured lookup results and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific results returned by IPQualityScore]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
