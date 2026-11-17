## Description:

Google Slides: Read and write presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help an agent inspect Google Slides command schemas and prepare gws CLI calls for reading, creating, and updating presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use an authenticated gws setup to read and modify Google Slides presentations.

Mitigation: Install it only when that access is intended, and review the gws shared auth/security instructions and Google account scopes before use.

Risk: Incorrect parameters could cause unintended Google Slides changes.

Mitigation: Use gws slides --help and gws schema slides.<resource>.<method> to inspect required parameters before preparing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-slides)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authentication.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
