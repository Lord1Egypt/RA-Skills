## Description:

Provides guidance for reading UniOne account data and sending transactional email through the UniOne connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect UniOne account information, suppressions, tags, and templates, and to prepare transactional email actions through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute remote code without separate approval or clear limits on local changes.

Mitigation: Review setup first, install a verified fixed CLI version under your control, and assess automatic skill synchronization before use.

Risk: Actions use the connected UniOne account, and email sends can reach recipients with the supplied content.

Mitigation: Review the connected account's permissions and confirm recipients and message content before sending.

## Reference(s):

- [UniOne homepage](https://unione.io)
- [UniOne API documentation](https://docs.unione.io/en/web-api-ref)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [UniOne ClawHub release](https://clawhub.ai/oomol/skills/oo-unione)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payload examples vary by UniOne action; action schemas define the available input fields.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
