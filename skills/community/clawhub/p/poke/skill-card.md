## Description: <br>
Send SMS/iMessage to the user via Poke and process inbound Poke events for alerts, forwarded Poke events, and external webhook triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to Poke for two-way SMS/iMessage communication, phone-originated requests, and Poke-routed webhook events from external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent phone-to-agent access can expose the local agent to inbound requests and external webhook events. <br>
Mitigation: Install only when this bridge is intended, use revocable least-privilege tokens, and keep clear approval rules for inbound Poke and webhook-triggered actions. <br>
Risk: The skill can set up persistent systemd services and a Poke tunnel for ongoing connectivity. <br>
Mitigation: Review the npm package and setup changes before installation, verify the created services, and understand how to disable the MCP server and tunnel services. <br>
Risk: Public exposure or broad tools such as file, log, and webhook actions can increase data exposure and command-routing risk. <br>
Mitigation: Avoid the public exposure option unless strong access controls are added, and do not expose file, log, or external webhook actions without trusted source validation. <br>


## Reference(s): <br>
- [Poke Bridge ClawHub page](https://clawhub.ai/G9Pedro/poke) <br>
- [Poke device authentication](https://poke.com/device) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of Poke/OpenClaw connectivity, systemd services, tunnel registration, message routing, and webhook trigger handling.] <br>

## Skill Version(s): <br>
0.6.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
