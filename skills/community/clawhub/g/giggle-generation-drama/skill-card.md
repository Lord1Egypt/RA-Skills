## Description:

Generates Giggle.pro AI videos from user-provided stories, with modes for episodes, narration videos, and short films.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through creating Giggle.pro video projects from stories, selecting generation modes or styles, and returning completed video download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically pay for pending Giggle.pro video-generation tasks using the account's available credits.

Mitigation: Require explicit user confirmation of budget, selected mode, duration, and payment before running the workflow or any payment action.

Risk: The skill requires a Giggle API key and returns signed private video download URLs.

Mitigation: Store the API key only in the GIGGLE_API_KEY environment variable, avoid logging credentials, and share signed download URLs only with the intended user.

Risk: Video generation depends on external Giggle.pro API calls and may run for an extended period.

Mitigation: Confirm setup before use, report API errors directly, and make the user aware that the workflow can poll for up to one hour.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-drama)
- [Publisher profile](https://clawhub.ai/user/patches429)
- [Giggle.pro](https://giggle.pro/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API calls, shell setup snippets, JSON response examples, and signed video download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and a GIGGLE_API_KEY environment variable; successful workflows may block while polling for up to one hour.]

## Skill Version(s):

0.0.10 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
