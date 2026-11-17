## Description:

Tripadvisor (tripadvisor.com). Use this skill for ANY Tripadvisor request — searching and reading data. Whenever a task involves Tripadvisor, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Tripadvisor account can search locations, find nearby places, and retrieve location details and photos. The skill guides an agent to check each action's input schema and return the resulting data to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may download and run CLI code, and setup changes may not be clearly approved.

Mitigation: Use a reviewed, integrity-verified CLI release and explicitly approve local changes. Review or disable bundled-skill synchronization using the oo CLI command reference.

Risk: Tripadvisor requests pass through OOMOL, and the external installer and hosted connector implementation were not verified.

Mitigation: Review the setup and connector terms before use, and limit access to information appropriate to the connected account.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Tripadvisor developer resources](https://www.tripadvisor.com/developers)
- [Tripadvisor Content API reference](https://tripadvisor-content-api.readme.io/reference/overview)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses with user-facing text and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses contain Tripadvisor location data; the skill documents search, nearby search, details, and photos actions.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
