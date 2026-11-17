## Description:

Creates AI music videos through the Giggle.pro MV trustee workflow from text music prompts or custom lyrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Giggle.pro API access, gather MV generation inputs, run the trustee workflow, monitor progress, and return the generated video result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically pay pending Giggle MV projects using GIGGLE_API_KEY.

Mitigation: Require explicit user confirmation of the project and amount before any paid workflow proceeds, or use a manual payment step.

Risk: A configured GIGGLE_API_KEY may allow billable Giggle account actions.

Mitigation: Use only a user-provided environment variable, avoid echoing the key, and review account billing exposure before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-aimv)
- [Giggle.pro](https://giggle.pro/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands and JSON-like workflow results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, and GIGGLE_API_KEY; successful workflows return project status and a signed video download URL.]

## Skill Version(s):

0.0.10 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
