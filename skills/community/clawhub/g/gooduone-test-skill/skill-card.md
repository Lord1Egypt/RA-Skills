## Description:

Get current weather and forecasts with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooduone](https://clawhub.ai/user/gooduone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for weather lookup commands and guidance for current conditions or forecasts through public weather services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries may disclose requested locations or coordinates to wttr.in or Open-Meteo.

Mitigation: Avoid including secrets, private personal details, or sensitive locations in weather query strings.

Risk: The skill depends on public weather services reached through curl.

Mitigation: Review generated commands before execution and confirm that contacting the named public service is acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gooduone/skills/gooduone-test-skill)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and weather API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands that call public weather services.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
