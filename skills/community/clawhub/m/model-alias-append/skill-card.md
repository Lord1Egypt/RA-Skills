## Description:

Automatically appends the model alias to the end of every response with integrated hook functionality and configuration change detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccapton](https://clawhub.ai/user/ccapton)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to make response attribution visible by appending the configured model alias to outgoing responses and noting model-alias configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intercepts outgoing responses and appends model-alias text from configuration.

Mitigation: Use only trusted, simple aliases without Markdown or newlines, and review responses after installation.

Risk: The skill can enable a persistent OpenClaw hook and change hook settings.

Mitigation: Confirm how to disable or remove response-alias-injector from ~/.openclaw/openclaw.json before deployment.

Risk: Installing an unpinned package can pull a later release than the reviewed artifact.

Mitigation: Prefer a pinned installer version when deploying this reviewed release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccapton/skills/model-alias-append)
- [OpenClaw hook documentation](https://docs.openclaw.ai/hooks#response-alias-injector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response text with appended model alias and optional configuration update notice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads configured model aliases from OpenClaw configuration and may update hook settings through the included management script.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
