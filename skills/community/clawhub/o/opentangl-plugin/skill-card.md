## Description: <br>
OpenTangl Plugin adds OpenTangl lifecycle tools to OpenClaw so an agent can inspect queues, propose tasks, run workflows, audit cross-repo wiring, and manage merge activity from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8co](https://clawhub.ai/user/8co) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this plugin to operate an OpenTangl workspace from OpenClaw, including viewing task state, proposing and executing development work, running workflows, auditing wiring, and managing pull-request merge flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can expose powerful OpenTangl automation, including repository changes, commits, pull requests, and merges. <br>
Mitigation: Start with read-only tools, enable mutating tools deliberately, use preview or run modes where available, and keep branch protections or human review in place before allowing PR creation or merges. <br>
Risk: Misconfigured OpenTangl workspaces or credentials can cause tool failures or automation against the wrong project. <br>
Mitigation: Confirm the configured workspace path, required API key environment variables, and project registry before enabling mutating tools. <br>


## Reference(s): <br>
- [OpenTangl Plugin on ClawHub](https://clawhub.ai/8co/opentangl-plugin) <br>
- [OpenTangl Documentation](https://opentangl.com) <br>
- [Publisher Profile](https://clawhub.ai/user/8co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [OpenClaw tool responses containing text or markdown, with configuration examples and command output from OpenTangl.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only tools are available by default; mutating tools require explicit allowlist configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
