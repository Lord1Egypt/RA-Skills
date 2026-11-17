## Description:

Indiegogo (indiegogo.com). Use this skill for ANY Indiegogo request — searching and reading data. Whenever a task involves Indiegogo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to find active Indiegogo campaigns and retrieve public creator and project details through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can install persistent agent skills, and this skill does not explain or limit that behavior.

Mitigation: Review and pin the CLI installation before enabling the skill; set OO_SKILLS_SYNC_DISABLED=1 before running oo to disable automatic skill synchronization.

Risk: Requests pass through OOMOL and may use its credits.

Mitigation: Review the expected OOMOL credit use before running connector actions.

## Reference(s):

- [Indiegogo](https://www.indiegogo.com)
- [Indiegogo public API documentation](https://help.indiegogo.com/article/616-indiegogo-public-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector results and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public creator and campaign data; available fields follow the live connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
