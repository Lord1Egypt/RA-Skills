## Description:

Provides outdoor photography timing guidance by subject, including golden hour, blue hour, midday, and travel-day planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and photography assistants use this skill to plan outdoor shoot timing and explain which times of day suit portraits, landscapes, architecture, city night scenes, and travel photography.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is Chinese-first with some English trigger phrases, which may reduce usefulness in other language contexts.

Mitigation: Review the skill for the intended deployment language and translate or adapt user-facing guidance as needed.

Risk: Timing guidance is less reliable for indoor shoots, cloudy or rainy weather, and cases where light direction is the primary decision.

Mitigation: Route indoor lighting and light-direction questions to more appropriate skills, and ask about weather or shooting conditions before applying golden-hour advice.

Risk: Golden-hour duration and light quality vary by latitude, season, local terrain, and weather.

Mitigation: Treat the recommendations as planning guidance and confirm local sunrise, sunset, weather, and location constraints before a shoot.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/bianchunhui/nyip-photography-skills/tree/main/golden-hour)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/golden-hour)
- [ClawHub publisher profile](https://clawhub.ai/user/bianchunhui)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text photography planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, dependency installation, persistence, or data access.]

## Skill Version(s):

0.1.0 (source: server release metadata and test-prompts.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
