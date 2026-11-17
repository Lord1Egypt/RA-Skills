## Description:

Generate PPTs using services provided by PI (Presentation Intelligence).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmcbbkad](https://clawhub.ai/user/xmcbbkad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate editable PowerPoint decks from a topic, outline, prompt, or a supported uploaded document through the PI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and optional uploaded documents to the external PI service.

Mitigation: Confirm the configured PIPPT_BASE_URL is a trusted HTTPS PI endpoint and only submit documents your organization permits PI to process.

Risk: The skill requires PI application credentials in environment variables.

Mitigation: Store PIPPT_APP_ID and PIPPT_APP_SECRET in a managed secret store or runtime environment and avoid placing them in prompts, command history, or source files.

## Reference(s):

- [PI website](https://www.pi.inc/)
- [ClawHub skill page](https://clawhub.ai/xmcbbkad/skills/pi-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a generated PPT document URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks usually take about 3-6 minutes and may be based on one supported uploaded document.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
