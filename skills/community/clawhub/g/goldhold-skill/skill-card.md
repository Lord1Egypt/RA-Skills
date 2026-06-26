## Description: <br>
Persistent memory for AI agents. Remember across sessions. Encrypted in transit and at rest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerrysrodz](https://clawhub.ai/user/jerrysrodz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect an AI agent to GoldHold for durable memory across sessions, including searching prior notes, storing decisions and facts, sending messages, and closing sessions with summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories may contain sensitive or confidential data in a persistent third-party service. <br>
Mitigation: Do not store API keys, tokens, private customer data, confidential code, system prompts, or other sensitive content unless GoldHold data handling has been explicitly reviewed and approved. <br>
Risk: The skill requires a GoldHold API key and sends authenticated requests to an external relay API. <br>
Mitigation: Store GOLDHOLD_API_KEY only in secure secret storage and review outbound API usage before enabling the skill. <br>


## Reference(s): <br>
- [GoldHold website](https://goldhold.ai) <br>
- [GoldHold API base URL](https://relay.goldhold.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jerrysrodz/goldhold-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jerrysrodz) <br>
- [Skill guide](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOLDHOLD_API_KEY and sends authenticated requests to the GoldHold relay API.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
