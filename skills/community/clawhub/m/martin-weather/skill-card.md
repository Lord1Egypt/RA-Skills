## Description:

Get current weather and forecasts with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up current weather, forecasts, compact weather summaries, and weather API responses through public services that do not require API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries may disclose requested locations to third-party weather services such as wttr.in or Open-Meteo.

Mitigation: Avoid sending sensitive private locations when that disclosure is a concern.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and weather API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and public third-party weather services; no API key is required.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
