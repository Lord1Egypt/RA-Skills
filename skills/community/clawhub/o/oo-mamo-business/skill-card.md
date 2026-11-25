## Description:

Search and read Mamo Business account data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Mamo Business account use the skill to inspect balances, business details, payments, and payment links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious because the CLI setup instructions can run a remote installer, a high-impact capability unrelated to reading Mamo Business data.

Mitigation: Avoid installing the CLI from the remote script until it has been reviewed; install it only through a method you trust.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Mamo Business API documentation](https://docs.mamopay.com/)
- [Mamo Business](https://www.mamopay.com/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON connector responses with account data and textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [List results may be paginated.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
