## Description:

Provides real-time weather, temperature, and clothing guidance for a specified city, asking for a location when needed and using search results as the weather source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanglingchao-2025](https://clawhub.ai/user/wanglingchao-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Users and assistants use JACK to answer Chinese-language weather questions for a city, including current temperature, weather conditions, and clothing suggestions. If no city is provided, the skill prompts for one before using search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather answers may be stale, unavailable, or inaccurate when search results are missing or unreliable.

Mitigation: Use current search results, do not fabricate weather data, and tell the user to verify manually when search fails.

Risk: Broad weather, temperature, or clothing-advice requests may trigger the skill before the city is known.

Mitigation: Ask for the user's city before searching or giving weather-specific guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanglingchao-2025/skills/my-weather-helper)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Concise Chinese-language text with weather details and clothing advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather data should come from current search results; if search fails, the skill tells the user to check manually.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
