## Description: <br>
Use Rocketlane through OOMOL's oo CLI connector to read projects, tasks, and users from a connected Rocketlane account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and customer-facing teams use this skill to retrieve Rocketlane project, task, and user records through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Rocketlane account. <br>
Mitigation: Use an account with appropriate Rocketlane permissions and reconnect only when the connector reports an authentication or scope error. <br>
Risk: The skill executes oo CLI commands on behalf of the agent. <br>
Mitigation: Review command payloads before execution and inspect the live connector schema before building JSON input. <br>
Risk: The security guidance notes that some related workflows can modify accounts, project files, or run review tools with broad local access. <br>
Mitigation: Approve only the Rocketlane read actions needed for the task and review any command that appears to perform deployment, moderation, package installation, or autoreview work. <br>


## Reference(s): <br>
- [ClawHub Rocketlane skill page](https://clawhub.ai/oomol/oo-rocketlane) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Rocketlane homepage](https://www.rocketlane.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Rocketlane get and list actions; live action schemas should be inspected before connector payloads are built.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
