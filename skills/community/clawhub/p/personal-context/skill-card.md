## Description: <br>
Builds a personal profile for your OpenClaw agent so it knows your name, role, timezone, goals, and communication style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyhetech](https://clawhub.ai/user/billyhetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to create and maintain an explicit local profile with the user's preferred name, role, timezone, goals, and communication style for personalized sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists personal preferences and identity details in a local profile file. <br>
Mitigation: Review or edit ~/.openclaw/workspace/me.json after onboarding and avoid storing passwords, tokens, financial details, health information, or other sensitive data. <br>


## Reference(s): <br>
- [Profile Schema Reference](references/profile-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions and JSON profile content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates ~/.openclaw/workspace/me.json after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
