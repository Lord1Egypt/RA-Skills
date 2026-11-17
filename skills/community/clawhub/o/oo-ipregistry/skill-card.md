## Description:

Ipregistry (ipregistry.co). Use this skill for ANY Ipregistry request — searching and reading data. Whenever a task involves Ipregistry, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill through an OOMOL-connected account to look up IP addresses and autonomous system numbers, retrieve geolocation and related data, and parse user-agent strings with Ipregistry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can persistently change other agent skills through startup synchronization, a behavior not explained by this skill.

Mitigation: Review the oo CLI's broader skill-management behavior before installation and set OO_SKILLS_SYNC_DISABLED=1 before CLI runs to disable startup synchronization. Verify the installer separately; submit only lookup inputs you intend to share with OOMOL and Ipregistry, and account for service charges.

## Reference(s):

- [Ipregistry](https://ipregistry.co)
- [Ipregistry API authentication documentation](https://ipregistry.co/docs/authentication)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance]

**Output Format:** [Structured Ipregistry response data and concise textual summaries or instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action, submitted lookup inputs, and connected Ipregistry account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
