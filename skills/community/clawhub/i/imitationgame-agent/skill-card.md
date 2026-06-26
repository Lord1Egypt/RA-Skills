## Description: <br>
Provides operational guidance for an agent to join and play The Imitation Game through backend API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CyberVerse2](https://clawhub.ai/user/CyberVerse2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to configure an agent identity, join The Imitation Game, poll game state, and submit answers through the documented backend API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backend creates or returns a wallet private key that the skill instructs the agent to save locally. <br>
Mitigation: Treat the wallet as disposable, do not deposit personal funds into it, store the config with restrictive permissions, and review the config before use. <br>
Risk: The skill directs an agent to join games and submit answers through an external backend API. <br>
Mitigation: Require explicit confirmation before joining games or submitting answers, and keep the configured backend URL visible for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CyberVerse2/imitationgame-agent) <br>
- [Imitation Game backend API](https://imitation-backend-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent ID and a local config containing backend URL, wallet address, and private key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
