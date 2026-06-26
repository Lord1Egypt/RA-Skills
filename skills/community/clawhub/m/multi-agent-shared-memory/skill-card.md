## Description: <br>
Set up shared memory between multiple OpenClaw agents so they stay in sync without the user repeating context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users with multiple agent workspaces use this skill to create a shared knowledge directory, sync conversation summaries, and update each agent's AGENTS.md so agents can share durable context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify multiple agent workspaces and create durable cross-agent memory. <br>
Mitigation: Have the agent show all target paths and AGENTS.md changes, get explicit confirmation before edits, and keep the shared-knowledge directory inspectable, editable, and deletable. <br>
Risk: Shared memory may retain secrets or sensitive personal details across agents. <br>
Mitigation: Avoid storing credentials, tokens, passwords, private persona files, or sensitive personal information in shared memory; review shared files regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junweiren98-rgb/multi-agent-shared-memory) <br>
- [Publisher profile](https://clawhub.ai/user/junweiren98-rgb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and PowerShell command examples plus file templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits across multiple OpenClaw workspaces; target paths and AGENTS.md changes should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
