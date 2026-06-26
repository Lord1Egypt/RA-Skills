## Description: <br>
Manage Node.js applications with PM2 process manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asteinberger](https://clawhub.ai/user/asteinberger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, monitor, restart, and configure Node.js applications managed by PM2 in production-style environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PM2 stop, delete, kill, and delete-all commands can interrupt or remove running application processes. <br>
Mitigation: Confirm the target app and environment before running destructive or interrupting process-control commands. <br>
Risk: PM2 startup commands can configure applications to persist across reboot and may require sudo. <br>
Mitigation: Run startup persistence commands only when reboot persistence is intended and the generated command has been reviewed. <br>
Risk: Global PM2 installation changes the local Node.js tool environment. <br>
Mitigation: Install only in environments where PM2 should manage Node.js applications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asteinberger/pm2) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes PM2 process control commands, startup persistence guidance, and an example ecosystem.config.js configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
