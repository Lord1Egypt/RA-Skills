## Description:

Read and write Google Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Google Docs commands and call the gws CLI to get, create, or batch update Google Docs through configured Google Workspace credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Google Docs through configured Google Workspace credentials.

Mitigation: Install it only for agents that should have that account access, and review the generated gws shared authentication and security instructions before use.

Risk: Incorrect command parameters can fail a Google Docs batch update or produce unintended document changes.

Mitigation: Inspect each method with gws schema before building --params or --json arguments, as directed by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and configured Google Workspace authentication before use.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence); artifact metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
