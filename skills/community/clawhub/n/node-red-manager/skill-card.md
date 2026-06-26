## Description: <br>
Manage Node-RED instances via Admin API or CLI. Automate flow deployment, install nodes, and troubleshoot issues. Use when user wants to "build automation", "connect devices", or "fix node-red". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer Node-RED instances they control, deploy or restore flows, manage nodes, inspect diagnostics, and update context values through the Admin API or CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent changes to live Node-RED automation systems. <br>
Mitigation: Use it only against Node-RED instances you control, verify NODE_RED_URL before entering credentials, and back up flows before deploy, restore, delete, or node-management actions. <br>
Risk: Credentials and flow files may expose sensitive operational access or behavior. <br>
Mitigation: Keep the .env file private, review flow JSON before deployment or restore, and avoid sharing backups that contain sensitive flow configuration. <br>
Risk: Exec nodes and third-party Node-RED modules can introduce higher-impact runtime behavior. <br>
Mitigation: Review exec-node usage and third-party node modules before installation or deployment. <br>


## Reference(s): <br>
- [Node-RED Admin API Reference](references/admin-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/1999AZZAR/node-red-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Node-RED Admin API calls and file paths for flow backup, restore, deployment, and diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
