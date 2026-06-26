## Description: <br>
Controls Home Assistant smart home devices, automations, scenes, and webhooks through REST API calls and a CLI wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and control Home Assistant entities, run scenes, scripts, and automations, and handle webhook-triggered home events from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants authenticated control over Home Assistant devices and services using long-lived credentials. <br>
Mitigation: Use a dedicated least-privilege Home Assistant account when possible, protect token storage with restrictive permissions, and prefer HTTPS or WSS connections. <br>
Risk: Agent actions can affect sensitive smart-home functions such as locks, covers, alarms, climate controls, scripts, automations, and generic service calls. <br>
Mitigation: Require explicit user confirmation before executing sensitive or broad-impact Home Assistant actions. <br>
Risk: Tokens and webhook identifiers could expose home-control capabilities if shared in prompts, logs, or public output. <br>
Mitigation: Avoid exposing Home Assistant tokens or webhook IDs and rotate credentials if they may have been disclosed. <br>


## Reference(s): <br>
- [Home Assistant REST API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq, with Home Assistant URL and long-lived token supplied by configuration file or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
