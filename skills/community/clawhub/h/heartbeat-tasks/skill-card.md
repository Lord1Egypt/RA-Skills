## Description: <br>
Manage and execute periodic heartbeat tasks for trading, memory evaluation, archiving, and reporting with state tracking and anomaly alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WuZiMaKi](https://clawhub.ai/user/WuZiMaKi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to schedule recurring heartbeat checks for crypto trading decisions, memory maintenance, summaries, and anomaly reporting. It is suited for agents that need to track state and report problems while staying quiet during normal runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to run recurring crypto trading checks and take trading actions without clearly stated safety limits. <br>
Mitigation: Keep trading in paper mode or require explicit confirmation for live orders, and enforce strict account, position, and credential scopes before use. <br>
Risk: The skill can modify persistent memory and state files as part of scheduled heartbeat work. <br>
Mitigation: Back up MEMORY.md, trading_rules.md, and heartbeat-state.json before use, and review changes after heartbeat runs. <br>
Risk: Normal operation may be silent except for HEARTBEAT_OK, which can hide unwanted behavior if monitoring is weak. <br>
Mitigation: Log heartbeat runs, audit state changes, and require detailed reporting for exceptions or trading-related decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WuZiMaKi/heartbeat-tasks) <br>
- [Publisher profile](https://clawhub.ai/user/WuZiMaKi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text or Markdown status reports, including HEARTBEAT_OK for normal runs and detailed issue reports when anomalies occur.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update heartbeat state, memory, archive, and trading summary files when the host agent has access to those paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
