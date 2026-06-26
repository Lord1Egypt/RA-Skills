## Description: <br>
IceCube Tasks provides file-backed task orchestration and tracking for AI agents, including task persistence, lifecycle tracking, blockers, and execution continuity across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to keep durable task ledgers, track task status, manage blockers, and resume work after context compaction or session restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update persistent local task files during task-management conversations. <br>
Mitigation: Ask the agent to confirm before making persistent task changes and review state/tasks updates before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create or update local YAML task files under state/tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
