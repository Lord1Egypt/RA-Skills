## Description: <br>
Guides Hermes and local OpenClaw collaboration through shared memory, API handoffs, and task division. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate Hermes with a local OpenClaw setup, including shared workspace memory, OpenClaw agent commands, task routing, and gateway troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes OpenClaw operations that may write workspace files, edit configuration, restart services, or delegate agent tasks. <br>
Mitigation: Install only in a trusted OpenClaw environment and require explicit approval before memory writes, configuration edits, service restarts, or delegated tasks. <br>
Risk: Message delivery examples could send content through Feishu or another channel if used without review. <br>
Mitigation: Avoid delivery flags by default and require human confirmation before sending messages outside the local environment. <br>
Risk: Operational changes may be difficult to audit after the fact if logs and backups are not maintained. <br>
Mitigation: Back up workspace and configuration files before use, enable operation logging, and periodically review file, API, and service activity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fish1981bimmer/openclaw-collaboration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety notes for approval, logging, backups, and cautious use of OpenClaw operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter: 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
