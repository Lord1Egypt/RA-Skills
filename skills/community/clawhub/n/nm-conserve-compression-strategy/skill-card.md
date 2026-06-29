## Description: <br>
Recommends context compression strategies for bloated or quota-heavy sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze bloated or quota-heavy sessions, choose a context compression or delegation strategy, and estimate expected savings before continuing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session summaries or context archives may contain secrets, private logs, or customer data. <br>
Mitigation: Review archived content before installing or using the skill in sensitive sessions, and avoid preserving confidential material unless it is needed for continuity. <br>
Risk: Session-clearing, compacting, or delegation workflows can lose active task state if the handoff is incomplete. <br>
Mitigation: Save critical decisions, active files, and next steps before clearing context or spawning a continuation agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-compression-strategy) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and TodoWrite checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend saving session summaries or context archives under .claude before clearing, compacting, or delegating work.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
