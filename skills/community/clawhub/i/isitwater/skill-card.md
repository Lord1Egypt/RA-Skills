## Description: <br>
Check if geographic coordinates are over water or land using the IsItWater API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnagro](https://clawhub.ai/user/johnnagro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to determine whether latitude and longitude coordinates are over water or land, and to check IsItWater account details before making API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an IsItWater API key. <br>
Mitigation: Prefer the ISITWATER_API_KEY environment variable, avoid sharing logs or config files containing the key, and restrict permissions on any local config file that stores it. <br>
Risk: Water lookup requests consume IsItWater account credits. <br>
Mitigation: Use the account info endpoint to check the remaining balance before making many lookup requests. <br>


## Reference(s): <br>
- [IsItWater](https://isitwater.com) <br>
- [Water lookup endpoint](https://api.isitwater.com/v1/locations/water) <br>
- [Account info endpoint](https://api.isitwater.com/v1/accounts/me) <br>
- [AgentSkills Spec](https://agentskills.io) <br>
- [OpenClaw Skills Docs](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an IsItWater API key; water lookups return JSON and cost 1 credit per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
