## Description:

Viggle (viggle.ai). Use this skill for ANY Viggle request — reading, creating, updating, and deleting data. Whenever a task involves Viggle, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Viggle through an OOMOL-connected account can inspect characters, scenes, render jobs, and credit balance; create character assets and render jobs; import templates; and remove assets. The skill provides guided operations for managing Viggle content and checking render status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may run a remote CLI installer without separate user approval, and the exact runtime release could not be verified.

Mitigation: Review and install a verified CLI release before use, and check the CLI's automatic skill synchronization settings.

Risk: Viggle operations use the user's connected account, and write or deletion actions can change account data.

Mitigation: Review the requested action and payload before confirming writes or deletions; OOMOL mediates connected-account requests.

## Reference(s):

- [Viggle](https://viggle.ai)
- [Viggle API documentation](https://docs.viggle.ai/authentication)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include Viggle resource data, render status, credit balance, and video URLs.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
