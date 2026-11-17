## Description:

Uses an OOMOL-connected Gender-API.com service to look up likely gender and country-of-origin information from names or email addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query likely gender or country-of-origin details for a first name, full name, or email address, and to check connected-account credits and recent usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote installer, and the installer and hosted connector implementation have not been inspected.

Mitigation: Review the installer and install a verified oo CLI version before use.

Risk: The linked CLI documents startup synchronization that can make broader changes to installed agent skills.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 to disable the documented startup synchronization.

Risk: Lookups submit names or email addresses and may consume account credits.

Mitigation: Send only information authorized for the lookup and check account credits and usage as needed.

## Reference(s):

- [Gender-API.com](https://gender-api.com/)
- [Gender-API.com API documentation](https://gender-api.com/en/api-docs/v2)
- [oo CLI tool](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector responses with concise Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include result data and execution metadata; lookups may consume account credits.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
