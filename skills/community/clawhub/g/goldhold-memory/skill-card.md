## Description: <br>
Persistent memory for AI agents. Remember across sessions. Encrypted in transit and at rest. https://goldhold.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerrysrodz](https://clawhub.ai/user/jerrysrodz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use GoldHold Memory to give AI agents durable memory across sessions, including stored decisions, facts, corrections, directives, and session summaries. The skill guides agents to search prior context, store important updates, and close sessions through the GoldHold REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages long-term storage of agent context, which can include confidential, personal, regulated, or credential-bearing content if users do not set boundaries. <br>
Mitigation: Define a clear storage policy before use, avoid storing secrets or sensitive personal data, and require review or confirmation before saving important memories or directives. <br>
Risk: The skill depends on an external API key and hosted memory service. <br>
Mitigation: Store GOLDHOLD_API_KEY in a secrets manager, rotate it if exposed, and verify how memories can be reviewed and deleted before deploying in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerrysrodz/goldhold-memory) <br>
- [GoldHold website](https://goldhold.ai) <br>
- [GoldHold relay API](https://relay.goldhold.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOLDHOLD_API_KEY and network access to the GoldHold API.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
