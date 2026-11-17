## Description:

LeadBoxer (leadboxer.com). Use this skill for ANY LeadBoxer request — searching and reading data. Whenever a task involves LeadBoxer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected LeadBoxer account can look up organization and firmographic data for domains, or organization, network, and geolocation data for IP addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may direct the user to execute remote CLI installation code without clear approval.

Mitigation: Review and approve CLI installation separately before allowing setup fallback; prefer a verified, fixed release.

Risk: OOMOL mediates lookup requests and connected credentials, and the hosted connector implementation has not been verified.

Mitigation: Review OOMOL's connection and data handling, and check automatic agent-skill installation and synchronization settings.

## Reference(s):

- [LeadBoxer](https://www.leadboxer.com/)
- [LeadBoxer API documentation](https://developers.leadboxer.com/docs/authentication-api-keys.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [LeadBoxer lookup results returned as JSON, with agent-facing text or guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected LeadBoxer account and the selected domain or IP lookup.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
