## Description: <br>
Monitor OpenAnt task activity, notifications, platform statistics, task details, escrow status, watched tasks, and wallet balance through the OpenAnt CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenAnt users and their agents use this skill as an account dashboard for checking notifications, task status, pending reviews, arbitration, escrow state, platform activity, and wallet balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad monitoring prompts can trigger authenticated OpenAnt account commands, exposing account dashboard details to the agent session. <br>
Mitigation: Invoke the skill with explicit OpenAnt wording and install it only when agent access to the OpenAnt dashboard is intended. <br>
Risk: The notifications read-all command changes notification read state. <br>
Mitigation: Require user confirmation before running read-all, even though most monitoring commands are read-only. <br>
Risk: Wallet-related commands can expose sensitive account or balance information, and future wallet CLI behavior may exceed simple balance checks. <br>
Mitigation: Limit wallet usage to balance checks unless the user explicitly confirms the exact wallet action. <br>
Risk: Using @latest for the OpenAnt CLI can change behavior as new package versions are released. <br>
Mitigation: Use a pinned or pre-vetted CLI version when supply-chain stability matters. <br>


## Reference(s): <br>
- [ClawHub skill page: monitor-tasks](https://clawhub.ai/ant-1984/monitor-tasks) <br>
- [Publisher profile: ant-1984](https://clawhub.ai/user/ant-1984) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to append --json; includes a status reference table and dashboard workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
