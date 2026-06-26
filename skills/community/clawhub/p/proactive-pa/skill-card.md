## Description: <br>
Proactive Personal Assistant behavior patterns that help an agent anticipate needs, run heartbeat checks, surface actionable insights, and improve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure an agent for proactive personal-assistant checks, scheduled heartbeat routines, and actionable follow-up suggestions. The artifact marks this release as deprecated and says the behavior moved into broader agent and personality configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous messaging or scheduled checks may contact fixed recipients or send external messages without clear user intent. <br>
Mitigation: Remove fixed recipient defaults and require explicit approval for every external message, or define a clearly bounded opt-in rule before use. <br>
Risk: Proactive scheduled behavior and memory persistence can continue after installation without enough review. <br>
Mitigation: Document and limit memory writes, keep scheduled jobs reviewable, and ensure users can disable them. <br>
Risk: Proactive alerts can become noisy or disruptive if every signal is treated as urgent. <br>
Mitigation: Alert only on actionable issues, batch non-urgent updates, and enforce quiet-hour rules except for explicitly defined critical cases. <br>


## Reference(s): <br>
- [Proactive Pa on ClawHub](https://clawhub.ai/netanel-abergel/proactive-pa) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes proactive check categories, heartbeat-state conventions, cron setup patterns, communication rules, and approval guardrails for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
