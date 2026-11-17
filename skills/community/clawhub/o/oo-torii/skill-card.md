## Description:

Torii (toriihq.com). Use this skill for ANY Torii request — searching and reading data. Whenever a task involves Torii, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to search and read Torii organization data, including apps, contracts, users, transactions, workflows, and organization profiles, through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can download and execute installer code without a separate review.

Mitigation: Review the installer and install the CLI separately before running it; avoid automatic installation or synchronization of other skills unless explicitly accepted.

Risk: The connector can access Torii data using the connected account's permissions.

Mitigation: Grant only the Torii access needed for the requested read operations and review the action schema before sending a payload.

## Reference(s):

- [Torii homepage](https://www.toriihq.com)
- [Torii API authentication documentation](https://developers.toriihq.com/reference/api-authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Torii skill release page](https://clawhub.ai/oomol/skills/oo-torii)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands and JSON responses presented as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves Torii records through documented get and list actions.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
