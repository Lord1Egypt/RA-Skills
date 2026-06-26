## Description: <br>
SSH-based PM2 service management for remote servers. List processes, restart/stop services, view logs, monitor CPU/memory usage, and perform common PM2 operations on production servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoohsuan](https://clawhub.ai/user/qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to manage Node.js applications running under PM2 on approved remote servers over SSH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes SSH commands that can restart, stop, delete, scale, flush logs for, or otherwise alter PM2-managed services on remote servers. <br>
Mitigation: Use least-privilege SSH accounts, replace example hosts and process names with approved targets, and require explicit confirmation before executing state-changing PM2 commands. <br>
Risk: Startup persistence and log-rotation commands can change host-level service behavior or install PM2 modules. <br>
Mitigation: Review commands with the responsible operator before applying startup, persistence, install, or log-management changes on production systems. <br>


## Reference(s): <br>
- [PM2 Remote Manager on ClawHub](https://clawhub.ai/qoohsuan/pm2-remote-manager) <br>
- [Publisher profile: qoohsuan](https://clawhub.ai/user/qoohsuan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes SSH command examples, PM2 process operations, ecosystem configuration examples, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
