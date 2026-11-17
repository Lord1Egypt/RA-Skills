## Description:

Use Neutrino API to search and read data for Neutrino-related requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to make Neutrino API lookups for IP blocklists and geolocation, domain information, and email or phone validation through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill setup can execute changing remote code and add agent skills without clearly explaining those effects.

Mitigation: Review CLI installation and any additional skill changes before enabling the skill. Use a verified CLI release and consider setting OO_SKILLS_SYNC_DISABLED=1 before invocation to prevent startup skill writes.

Risk: Lookup data is sent to OOMOL and Neutrino when actions run.

Mitigation: Submit only lookup data you are authorized to share with OOMOL and Neutrino.

## Reference(s):

- [Neutrino API](https://www.neutrinoapi.com/)
- [Neutrino API documentation](https://www.neutrinoapi.com/api/api-basics/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON API responses and concise text summaries, with shell commands for invoking actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Neutrino account; response details depend on provider data and account access.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
