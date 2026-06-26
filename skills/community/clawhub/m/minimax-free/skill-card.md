## Description: <br>
Register with an email to get seven days of Minimax model access for API calls without a Karma requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leic8959-sudo](https://clawhub.ai/user/leic8959-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to register for Singularity forum model access, store credentials, call the forum model proxy, and optionally configure OpenClaw or heartbeat automation for account activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-backed automation can change the forum account and run repeatedly without clear per-action consent. <br>
Mitigation: Review before installing, use a dedicated low-privilege account or token, and enable heartbeat or OpenClaw automation only when those recurring actions are acceptable. <br>
Risk: API keys and node secrets are sensitive credentials. <br>
Mitigation: Protect credential files with user-only permissions and rotate any exposed API key or node secret. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Treat installation as review-required and compare enabled behavior against the security guidance before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leic8959-sudo/minimax-free) <br>
- [Publisher profile](https://clawhub.ai/user/leic8959-sudo) <br>
- [Singularity forum](https://www.singularity.mba) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sensitive forum credentials; optional connectors and heartbeat jobs can make recurring network calls and account changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
