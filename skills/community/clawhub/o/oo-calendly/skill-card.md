## Description:

Use the connected Calendly account to read and manage scheduling data, including events, availability, invitees, and organization settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and manage Calendly scheduling data through a connected account, including events, availability, invitees, and organization settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download-and-run CLI installation fallback and hosted connector code were not inspected; no malicious behavior was established.

Mitigation: Preinstall a reviewed, verified CLI release instead of using the download-and-run fallback.

Risk: Automatic skill synchronization may change other agent skills without disclosure.

Mitigation: Review the synchronization behavior and disable it with OO_SKILLS_SYNC_DISABLED=1 if it is not wanted.

Risk: Connected Calendly permissions may allow changes to account data.

Mitigation: Connect only the Calendly account and permissions needed, and review targets before approving changes.

## Reference(s):

- [Calendly API documentation](https://developer.calendly.com/api-docs)
- [Calendly](https://calendly.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-calendly)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action payloads and Calendly results summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Calendly data require confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
