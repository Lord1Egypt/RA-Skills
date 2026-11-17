## Description:

Leexi (leexi.ai). Use this skill for ANY Leexi request — searching and reading data. Whenever a task involves Leexi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Leexi workspace can use the skill to find and read calls, meeting notes, teams, and users. It retrieves Leexi data through the available read actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and make broader agent changes without clear user control.

Mitigation: Review setup before enabling the skill, use a separately reviewed fixed CLI version, and require approval for installation. The remote installer behavior remains unverified.

## Reference(s):

- [Leexi](https://www.leexi.ai/)
- [Leexi Public API Documentation](https://docs.public-api.leexi.ai/reference/public-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON data and agent-readable text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Leexi call, note, team, and user data; requires an existing oo CLI sign-in and Leexi connection.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
