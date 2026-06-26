## Description: <br>
A lightweight parallel-agent harness for complex tasks that should only be used when swarm processing is explicitly requested or when a task has at least two independent subtasks and three or more tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use GLM Swarm to split complex work into smaller worker tasks, coordinate parallel subagents, and aggregate results into concise summaries and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate multiple subagents and persist worker task data under /tmp. <br>
Mitigation: Use it only for tasks that intentionally require swarm coordination, avoid sensitive data, and clean task directories after completion. <br>
Risk: Cleanup and task directory handling rely on caller-provided task IDs and local shell scripts. <br>
Mitigation: Review task IDs before running scripts and avoid broad cleanup operations unless the target directories are understood. <br>
Risk: Code changes, deployment steps, or other external actions may be proposed by workers. <br>
Mitigation: Require manual approval after aggregation before applying code changes, deployment actions, or external side effects. <br>


## Reference(s): <br>
- [Context Packet Protocol](references/context-packet.md) <br>
- [Predefined Pattern Library](references/patterns.md) <br>
- [GLM Swarm on ClawHub](https://clawhub.ai/mupengi-bot/glm-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown with structured worker instructions, shell commands, and summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Worker outputs are expected to stay concise, with aggregator summaries of 3 to 5 lines when detailed results exceed 500 tokens.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
