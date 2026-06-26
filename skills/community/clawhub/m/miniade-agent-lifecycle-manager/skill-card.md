## Description: <br>
Agent Lifecycle Manager helps agents manage local OpenClaw agent lifecycle operations, including agent creation, channel binding, pairing approval, archiving, deletion, dashboard refreshes, and lifecycle logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miniade](https://clawhub.ai/user/miniade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to onboard, reconfigure, pair, archive, delete, and audit local OpenClaw agents. It is intended for agent administration workflows that require explicit confirmation around credential inheritance and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer local OpenClaw agents, including deletion flows. <br>
Mitigation: Verify the target agent ID and intended lifecycle action before running helpers, and use deletion only after archive creation and explicit confirmation. <br>
Risk: Generated archives and state files may contain credentials, configuration, chat history, or workspace data. <br>
Mitigation: Store archives and state outputs in private locations with appropriate access controls, and review archive paths before execution. <br>
Risk: Credential inheritance, Telegram tokens, pairing codes, and deletion bypass flags can change access or remove runtime assets. <br>
Mitigation: Require explicit user approval for --inherit-auth and --yes, and verify Telegram tokens and pairing codes before use. <br>


## Reference(s): <br>
- [OpenClaw Agent Lifecycle Playbook](references/openclaw-agent-lifecycle-playbook.md) <br>
- [Agent Lifecycle Manager on ClawHub](https://clawhub.ai/miniade/miniade-agent-lifecycle-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw state, archives, dashboard files, and lifecycle logs when executed by an agent with the required tools.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
