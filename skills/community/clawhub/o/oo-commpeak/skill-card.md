## Description:

Use CommPeak to read account data and send SMS through TextPeak.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account operators use this skill to inspect CommPeak TextPeak streams, domains, senders, and messages, and to send SMS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential handling as an area that needs care.

Mitigation: Keep returned stream tokens out of responses and logs; prefer send_sms, which retrieves its token internally, and confirm recipients and message content before sending.

Risk: The CLI installation path and hosted connector were not verified by the security review.

Mitigation: Independently verify the CLI release before installation and consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [CommPeak TextPeak API documentation](https://docs.commpeak.com/reference/textpeak-api-overview)
- [CommPeak](https://www.commpeak.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text summaries and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector results may include execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
