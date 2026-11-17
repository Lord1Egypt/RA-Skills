## Description:

Queries current weather for a city and returns a concise Chinese response with the weather condition and temperature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lushulin-jack](https://clawhub.ai/user/lushulin-jack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to request current city weather and receive a short Chinese summary containing the city, weather condition, and temperature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to construct a curl command from user-provided city text, which can be unsafe if the city contains quotes, shell metacharacters, newlines, or URL delimiters.

Mitigation: Validate and URL-encode city names before requests, avoid shell invocation when possible, and review generated commands before execution.

Risk: Network weather requests may disclose city queries to an external weather service.

Mitigation: Use only when external network weather lookup is acceptable and avoid sensitive location data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lushulin-jack/skills/lsl-test-skill1)
- [ClawHub publisher profile](https://clawhub.ai/user/lushulin-jack)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Concise Chinese text response, typically one to two sentences.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the city name, weather condition, and temperature; failure responses ask the user to check the city name and prefer English city names.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
