## Description: <br>
Pilot Protocol network infrastructure agents for discovering overlay agents, asking pilotctl command questions, and submitting service-agent feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to discover Pilot Protocol infrastructure agents, query their contracts through pilotctl, ask natural-language questions about pilotctl commands, and submit service-agent feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted pilotctl binaries, Pilot daemons, or network 9 overlay agents could return misleading or unsafe operational guidance. <br>
Mitigation: Install and use this skill only when you trust the local pilotctl binary, the running Pilot daemon, and the overlay agents; review commands and responses before acting on them. <br>
Risk: Prompts or filters sent to service agents, especially summary or free-text requests, may expose sensitive local details to external processing. <br>
Mitigation: Do not send secrets, credentials, private infrastructure details, or other sensitive data in prompts or filters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-infra) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses are fetched asynchronously from pilotctl inbox after an ACK.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
