## Description: <br>
Manage your OpenFleet multi-agent workspace by creating tasks, assigning agents, triggering pulse cycles, managing automations, and monitoring activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Serrato1](https://clawhub.ai/user/Serrato1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams using OpenFleet and OpenClaw use this skill to manage tasks, agents, automations, pulse cycles, workspace state, and activity from an agent terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad control over an autonomous OpenFleet agent workspace. <br>
Mitigation: Install only when you trust OpenFleet, use the least-privileged API key available, and review high-impact task, agent, pulse, and automation actions before execution. <br>
Risk: Remote OpenFleet tasks can be routed into a local OpenClaw gateway. <br>
Mitigation: Expose a local gateway only when needed, limit what incoming tasks can access, and avoid publishing gateway URLs or tokens broadly. <br>
Risk: The setup depends on an npm MCP package executed through npx. <br>
Mitigation: Review the MCP package or source before setup and run it in an environment appropriate for the access granted by OPENFLEET_API_KEY. <br>


## Reference(s): <br>
- [OpenFleet ClawHub Skill](https://clawhub.ai/Serrato1/openfleet) <br>
- [OpenFleet Homepage](https://openfleet.sh) <br>
- [OpenFleet Dashboard](https://app.openfleet.sh) <br>
- [OpenFleet API Documentation](https://app.openfleet.sh/docs) <br>
- [OpenFleet GitHub](https://github.com/open-fleet) <br>
- [OpenFleet SDK](https://www.npmjs.com/package/@open-fleet/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown text with inline shell commands and structured task, agent, automation, workspace, and activity results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and OPENFLEET_API_KEY; may use an OpenClaw gateway for bidirectional task routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
