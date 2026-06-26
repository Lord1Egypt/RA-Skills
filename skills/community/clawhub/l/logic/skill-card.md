## Description: <br>
Start from what must be true. Stop answering on autopilot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to structure ambiguous strategy, debugging, decision, and judgment tasks before making recommendations. It helps an agent identify objectives, constraints, load-bearing variables, mechanisms, and fragile assumptions before answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heartbeat maintenance may update local reasoning notes under ~/logic. <br>
Mitigation: Review heartbeat changes before relying on them and keep maintenance scoped to ~/logic as described by the skill. <br>
Risk: The skill can influence agent recommendations by imposing a reasoning structure. <br>
Mitigation: Review important recommendations for correctness, especially when the cost of weak reasoning is meaningful. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ProjectSnowWork/logic) <br>
- [Logic Homepage](https://clawic.com/skills/logic) <br>
- [Logic Philosophy](references/philosophy.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with occasional shell commands and local file maintenance notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain scoped local reasoning files under ~/logic when heartbeat behavior is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
