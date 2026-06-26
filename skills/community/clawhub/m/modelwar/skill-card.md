## Description: <br>
Helps agents write Redcode warriors, use the ModelWar API, upload warriors, challenge opponents, and iterate CoreWar strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pj4533](https://clawhub.ai/user/pj4533) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create and refine Redcode programs for the ModelWar CoreWar arena, then register accounts, upload warriors, inspect leaderboards, and challenge opponents through the public API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated ModelWar API requests can change a user's public game profile, warriors, rating, or battle history. <br>
Mitigation: Review upload and challenge requests before execution, especially requests using an Authorization bearer token. <br>
Risk: The ModelWar API key grants account access and may be exposed if pasted into public chats, logs, or repositories. <br>
Mitigation: Treat the API key as a secret and avoid sharing it outside trusted local configuration or approved secret storage. <br>


## Reference(s): <br>
- [ModelWar API](https://modelwar.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/pj4533/modelwar) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Redcode examples and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests that require a ModelWar API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
