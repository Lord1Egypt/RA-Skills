## Description:

Use an OOMOL-connected IPinfo account through the oo CLI to look up IP addresses and map IP lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve IP address geolocation, network, privacy, and related enrichment data, inspect account usage information, and map lists of IP addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required toolkit may persistently add other agent skills, and the provided skill does not explain all resulting installation effects.

Mitigation: Review and pin the toolkit installation; if only IPinfo access is needed, disable automatic skill synchronization before first use as described in the security guidance.

Risk: IP addresses sent for lookups or mapping may be uploaded to IPinfo, and credential handling is managed through the connected OOMOL account.

Mitigation: Confirm the IP data is permitted to be sent and review OOMOL credential handling before use.

Risk: Remote installer contents and the eventual installed version have not been verified in the provided release evidence.

Mitigation: Use a reviewed, version-pinned installation and inspect its broader installation effects before proceeding.

## Reference(s):

- [IPinfo API documentation](https://ipinfo.io/developers)
- [IPinfo](https://ipinfo.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [IPinfo connection setup](https://console.oomol.com/connections/ipinfo_io)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-ipinfo-io)

## Skill Output:

**Output Type(s):** [JSON, Text, Report URLs]

**Output Format:** [JSON or plain text responses from IPinfo actions, with report URLs for IP mapping]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields vary by action and IPinfo account entitlements.]

## Skill Version(s):

1.0.6 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
