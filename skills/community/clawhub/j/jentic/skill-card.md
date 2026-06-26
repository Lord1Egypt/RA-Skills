## Description: <br>
Call external APIs through Jentic, an AI agent API middleware that lets agents search, inspect, and execute catalog API operations through a broker while centralizing authentication outside the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanblanchfield](https://clawhub.ai/user/seanblanchfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Jentic Mini and route external API work, such as Gmail, Google Calendar, GitHub, Stripe, and Twilio operations, through Jentic instead of direct API calls. It is intended for workflows where credential management, permission requests, and brokered execution should stay outside the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes external API work through Jentic and can trigger powerful credential-backed operations. <br>
Mitigation: Install only when that routing is intended, connect only accounts the agent should use, and review permission requests before approval. <br>
Risk: Running Jentic Mini on the same machine as the agent weakens the intended boundary around credentials and administrative controls. <br>
Mitigation: Prefer a separate trusted Jentic Mini host for production or sensitive accounts, and reserve same-machine Docker setup for development or testing. <br>
Risk: Loss or exposure of JENTIC_API_KEY could allow unauthorized brokered API requests. <br>
Mitigation: Keep the Jentic API key protected in agent configuration and regenerate it through the Jentic Mini UI if it is lost or exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanblanchfield/jentic) <br>
- [Jentic website](https://jentic.com) <br>
- [Jentic Mini repository](https://github.com/jentic/jentic-mini) <br>
- [Jentic Mini AUTH docs](https://github.com/jentic/jentic-mini/blob/main/docs/AUTH.md) <br>
- [Jentic Mini CREDENTIALS docs](https://github.com/jentic/jentic-mini/blob/main/docs/CREDENTIALS.md) <br>
- [Jentic Skills repository](https://github.com/jentic/jentic-skills) <br>
- [tools-block.md](references/tools-block.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JENTIC_URL and JENTIC_API_KEY; guides the agent to use brokered API requests and human-approved permission changes.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
