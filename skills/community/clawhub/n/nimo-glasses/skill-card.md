## Description: <br>
Connect AI smart glasses to OpenClaw via Companion App with link-code pairing, chat API access, and SSE streaming for voice-controlled AI conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orideclaw](https://clawhub.ai/user/orideclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-glasses integrators use this skill to connect Nimo AI Glasses companion workflows to an OpenClaw Gateway for paired chat requests and streaming AI responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer and pairing flow may expose an OpenClaw gateway and active pairing secret to the network with weak or default protection. <br>
Mitigation: Review before installing, prefer localhost-only binding unless remote access is required, use a strong unique gateway token, and protect exposed gateways with firewall or reverse-proxy controls. <br>
Risk: The active link code may be visible through unauthenticated health responses. <br>
Mitigation: Remove the active link code from unauthenticated health responses or restrict access to the health route before using the plugin outside a trusted local environment. <br>
Risk: Provider API keys may be configured by deployment scripts. <br>
Mitigation: Confirm where provider API keys are stored and restrict access to OpenClaw configuration files before running deploy.sh. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/orideclaw/nimo-glasses) <br>
- [Publisher Profile](https://clawhub.ai/user/orideclaw) <br>
- [README](artifact/README.md) <br>
- [OpenClaw Plugin Manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with JSON configuration examples, shell commands, TypeScript plugin code, and HTTP/SSE API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The plugin exposes JSON chat responses and token-by-token SSE events through OpenClaw Gateway routes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
