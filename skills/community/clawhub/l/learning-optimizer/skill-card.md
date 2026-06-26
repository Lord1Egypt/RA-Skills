## Description: <br>
Learning Optimizer analyzes study patterns, identifies inefficiencies, suggests optimization steps, and can store local JSONL logs for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and learning-support agents use this skill to analyze study schedules, distractions, subject priorities, and current methods, then produce efficiency analysis, optimization suggestions, time allocation plans, and focus guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study schedules, priorities, distractions, and current learning methods entered by users are saved in local JSONL logs. <br>
Mitigation: Set LEARNING_OPTIMIZER_HOME to an appropriate private directory, avoid shared storage for sensitive study data, and delete ~/.learning-optimizer when history should no longer be retained. <br>
Risk: Optimization suggestions may be unsuitable for an individual learner and are not performance guarantees. <br>
Mitigation: Treat suggestions as planning guidance, review them before use, and adjust them through gradual experimentation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with command examples; command output may include JSON and local JSONL log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally without network or API requirements; runtime logs are stored under ~/.learning-optimizer by default or LEARNING_OPTIMIZER_HOME when set.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, skill.json, clawhub.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
