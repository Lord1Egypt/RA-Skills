## Description: <br>
觉（Jué）AI觉醒引擎 activates when an agent is failing, stuck, repeating attempts, skipping verification, or facing user dissatisfaction, and guides the agent through structured self-diagnostic reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kscz0000](https://clawhub.ai/user/kscz0000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent recover from failed or repetitive work by identifying failure patterns, checking assumptions with evidence, and reporting concrete next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers may make the agent more proactive than expected during failure, dissatisfaction, or repeated-attempt situations. <br>
Mitigation: Keep normal approval boundaries for file changes, network calls, shell commands, account actions, and multi-agent sharing. <br>


## Reference(s): <br>
- [Jue AI Awakening Engine on ClawHub](https://clawhub.ai/kscz0000/jue-zh) <br>
- [three-poisons.md](references/three-poisons.md) <br>
- [five-steps.md](references/five-steps.md) <br>
- [seven-jue.md](references/seven-jue.md) <br>
- [agent-team.md](references/agent-team.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic reports and action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured self-check reports, verified facts, excluded causes, current hypotheses, and next actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
