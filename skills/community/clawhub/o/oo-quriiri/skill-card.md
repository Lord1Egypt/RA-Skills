## Description:

Use Quriiri to check SMS delivery, list sender IDs, and send SMS through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to check Quriiri SMS delivery statuses, list authorized sender IDs, and send SMS from a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs code downloaded from the internet, and external installers and service implementations are unverified.

Mitigation: Preinstall a reviewed, version-pinned CLI and require approval before installing additional software.

Risk: SMS requests may reach unintended recipients or incur charges.

Mitigation: Confirm recipients and message text before sending, and account for possible charges.

## Reference(s):

- [Quriiri API documentation: send SMS](https://docs.quriiri.fi/docs/quriiri/send-sms)
- [Quriiri](https://quriiri.fi/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Quriiri on ClawHub](https://clawhub.ai/oomol/skills/oo-quriiri)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read actions and SMS sending; sending requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
