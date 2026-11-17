## Description:

Search and read Greip data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up autonomous system, country, and IP information through the Greip connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code or make changes to other agent skills that this skill does not explain.

Mitigation: Review the CLI installation separately and consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI to disable startup skill synchronization.

Risk: Lookup inputs are sent to OOMOL and Greip.

Mitigation: Send only lookup inputs you are comfortable sharing with OOMOL and Greip.

## Reference(s):

- [Greip API documentation](https://docs.greip.io/)
- [Greip homepage](https://greip.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [Greip lookup results as JSON, with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides lookup results for ASN, country, or IP queries; no file output is specified.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
