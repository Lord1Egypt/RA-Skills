## Description: <br>
Local-first planning engine for trips, weeks, launches, projects, schedules, and structured decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn goals, trips, launches, projects, weekly priorities, and decisions into structured plans with constraints, phases, milestones, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning details are saved locally on the machine. <br>
Mitigation: Avoid storing secrets or highly sensitive personal information, and review or delete the planner JSON files when local retention is no longer desired. <br>


## Reference(s): <br>
- [Planner Philosophy](references/philosophy.md) <br>
- [ClawHub Planner Release](https://clawhub.ai/AGIstack/planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON files, guidance] <br>
**Output Format:** [Plain text command output and locally stored JSON plan records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plan data locally under ~/.openclaw/workspace/memory/planner when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
