## Description: <br>
Persistent User Memory gives an OpenClaw agent a structured local user profile that persists across sessions for personalization, preferences, contacts, recurring patterns, and significant interaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyadhrif](https://clawhub.ai/user/eyadhrif) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent remember local preferences, contacts, recurring tasks, and important past interactions so future assistance can be personalized without repeated setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a durable local profile containing personal preferences, contacts, task patterns, and interaction summaries. <br>
Mitigation: Install only when persistent local personalization is desired, review ~/.openclaw/memory/user_profile.json periodically, and use the documented forget or reset requests when memory is wrong or unwanted. <br>
Risk: Sensitive data could be captured if a user asks the agent to remember secrets or highly private information. <br>
Mitigation: Follow the skill's stated refusal behavior for passwords, API keys, payment details, and other highly sensitive data; use a secure vault for secrets instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eyadhrif/persistent-user-memory) <br>
- [Publisher profile](https://clawhub.ai/user/eyadhrif) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON profile structure and shell installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-memory operating guidance and profile schema; it does not directly emit a remote API payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, CHANGELOG, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
