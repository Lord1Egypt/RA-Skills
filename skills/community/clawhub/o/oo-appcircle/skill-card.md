## Description:

Appcircle (appcircle.io). Use this skill for ANY Appcircle request — searching and reading data. Whenever a task involves Appcircle, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release teams use this skill to inspect connected Appcircle organizations and list build, testing distribution, and enterprise store profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote oo CLI installer whose behavior has not been independently verified.

Mitigation: Review the installer and CLI, use a separately reviewed version-pinned release, and explicitly approve local changes and any automatic skill installation.

Risk: Appcircle access and credentials are brokered by OOMOL, and server-side credential handling could not be independently verified.

Mitigation: Use an approved OOMOL connection, review its data handling, and keep raw credentials out of command payloads.

## Reference(s):

- [Appcircle](https://appcircle.io/)
- [Appcircle API authentication documentation](https://docs.appcircle.io/appcircle-api-and-cli/api-authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON connector results with textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only organization and profile data available to the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
