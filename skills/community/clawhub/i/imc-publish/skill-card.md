## Description:

Publish, schedule, and check the status of posts, images, and videos to connected social media accounts through an InstallMyClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwei1213](https://clawhub.ai/user/junwei1213)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use IMC Publish to draft, schedule, publish, and check social media posts for accounts already connected to the user's InstallMyClaw workspace. It is intended for publishing workflows that require media upload, preview review, explicit confirmation, and per-platform result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real connected social accounts by publishing or scheduling content.

Mitigation: Create a draft first, show the returned preview, and require explicit user confirmation for each draft before confirming publication.

Risk: The workspace publishing key and optional service endpoint determine where publishing requests are sent.

Mitigation: Install only when the publisher and workspace key permissions are trusted, keep the key out of chat and repository files, and leave the endpoint override unset unless the endpoint is trusted.

Risk: The built-in update command can replace local skill files.

Mitigation: Prefer a managed ClawHub or OpenClaw updater and review changes before continuing publishing work.

## Reference(s):

- [IMC Publish on ClawHub](https://clawhub.ai/junwei1213/skills/imc-publish)
- [Platform Notes](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a workspace publishing key. Draft previews should be reviewed before confirming publication.]

## Skill Version(s):

1.0.6 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
