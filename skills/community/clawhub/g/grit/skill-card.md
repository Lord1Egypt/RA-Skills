## Description: <br>
Grit guides an agent to persist through blocked tasks by diagnosing failures, escalating tools and tactics, and iterating until the task is solved or a real external blocker remains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocketship4545-a11y](https://clawhub.ai/user/rocketship4545-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users invoke Grit when an agent is blocked by brittle automation, weak tooling, or multi-step troubleshooting and needs a structured escalation loop. It helps the agent diagnose failures, switch methods or tools, preserve solved layers, and report concrete blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages more persistent tool use and may lead the agent to propose new tools, browser-session use, API actions, CLI actions, or skill installation. <br>
Mitigation: Invoke it intentionally, keep required SOP and security scans in force, and review proposed new tools or privileged actions before allowing them. <br>
Risk: Escalation loops can waste effort if retries do not materially change the approach. <br>
Mitigation: Require each retry to change the tool, interaction method, target state, artifact, configuration, or sequencing, and stop when only a true external blocker remains. <br>


## Reference(s): <br>
- [Escalation Ladder](references/escalation-ladder.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with task-specific commands, code snippets, configuration changes, and concise progress updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the active user task and remain subject to workspace SOPs, system safety rules, and tool policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
