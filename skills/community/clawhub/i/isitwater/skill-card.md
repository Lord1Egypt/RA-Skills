## Description:

Check if geographic coordinates are over water or land using the IsItWater API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnagro](https://clawhub.ai/user/johnnagro)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to configure the IsItWater API and check whether latitude and longitude coordinates are over water or land. It can also help check account balance before spending lookup credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an IsItWater API key, and exposed credentials could allow unauthorized use of the account.

Mitigation: Keep the key in an environment variable or protected OpenClaw configuration, and do not paste real API keys into chat or shared logs.

Risk: Coordinate and place-name lookups may disclose sensitive home, work, or travel locations to external services.

Mitigation: Avoid geocoding or checking private locations unless the user is comfortable sending that location to external services.

Risk: Water lookup requests consume paid credits.

Mitigation: Use the account endpoint to check remaining balance before making many lookups.

## Reference(s):

- [IsItWater](https://isitwater.com)
- [IsItWater water lookup endpoint](https://api.isitwater.com/v1/locations/water)
- [IsItWater account endpoint](https://api.isitwater.com/v1/accounts/me)
- [AgentSkills Spec](https://agentskills.io)
- [OpenClaw Skills Docs](https://docs.openclaw.ai/tools/skills)
- [ClawHub skill page](https://clawhub.ai/johnnagro/skills/isitwater)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with JSON and bash examples for API setup and requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an IsItWater API key; water lookups cost 1 credit each while account lookup is free.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
