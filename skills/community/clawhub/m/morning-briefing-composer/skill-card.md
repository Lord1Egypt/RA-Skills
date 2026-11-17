## Description:

Aggregates weather, game updates, and concert data into a daily markdown briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patfitzner](https://clawhub.ai/user/patfitzner)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to compose a daily briefing from weather, game updates, and concert data, then present the generated markdown briefing verbatim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured weather location is sent to wttr.in when weather is enabled.

Mitigation: Disable weather in the configuration or use a non-sensitive location if location disclosure is a concern.

Risk: External briefing content is displayed exactly as generated.

Mitigation: Treat links and instructions in generated briefings as untrusted and review content before acting on it.

Risk: Routine use depends on external content and transport behavior.

Mitigation: Prefer HTTPS and validation before relying on the generated briefing in regular workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patfitzner/skills/morning-briefing-composer)
- [Publisher Profile](https://clawhub.ai/user/patfitzner)
- [wttr.in Weather Service](https://wttr.in/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown briefing file plus shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated briefing should be presented verbatim; configuration controls weather, source enablement, and filtering.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
