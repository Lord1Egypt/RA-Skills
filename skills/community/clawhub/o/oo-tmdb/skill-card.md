## Description:

Search TMDB and retrieve movie, TV, person, trending, and configuration data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search TMDB and retrieve movie, TV series, person, trending, and configuration information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloaded oo CLI installer could not be inspected and may execute code during setup without a clear approval step.

Mitigation: Review and approve CLI installation separately using a verified version. If only TMDB functionality is needed, consider disabling managed-skill synchronization with OO_SKILLS_SYNC_DISABLED.

## Reference(s):

- [TMDB](https://www.themoviedb.org)
- [TMDB API documentation](https://developer.themoviedb.org/reference/intro/getting-started)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, Text, JSON]

**Output Format:** [JSON data returned by TMDB actions, presented as text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only searches, listings, and lookups.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
