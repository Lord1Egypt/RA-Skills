## Description:

Search and read Evenium event and guest data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Evenium account can search events and read event, guest, RSVP, and attendance information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute downloaded code, and the exact installed release is unverified.

Mitigation: Review and approve CLI installation separately, use a verified release, and consider disabling automatic skill synchronization.

Risk: The connected account may expose attendee information through OOMOL.

Mitigation: Connect only an appropriate Evenium account and consider which attendee information it can access.

## Reference(s):

- [Evenium](https://corp.evenium.com)
- [Evenium Organizer API documentation](https://static.evenium.com/api-docs/organizer/index-json.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only event and guest information]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
