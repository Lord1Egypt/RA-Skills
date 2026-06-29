## Description: <br>
Classifies agent tasks into 4 risk tiers (GREEN/YELLOW/RED/CRITICAL). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent orchestrators use this skill to classify coding tasks by risk tier before execution, assign verification gates, and decide when review, reversibility scoring, or human approval is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger broadly in conversations about risk, safety, or verification. <br>
Mitigation: Review the tier rules before deployment and enable the skill only where its checklist matches the team's workflow. <br>
Risk: Pattern-based classification can miss context that is not visible from file paths or file counts. <br>
Mitigation: Use the documented escalation rules, reversibility scoring for RED and CRITICAL tasks, and human approval for CRITICAL tasks. <br>
Risk: Task plans could rely on an incorrect risk tier if defaults are accepted without review. <br>
Mitigation: Require risk reasons in task metadata and verify that the assigned tier's gates pass before marking work complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-risk-classification) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [Night Market leyline homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Readiness levels module](modules/readiness-levels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with risk-tier labels, checklists, and task metadata examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GREEN/YELLOW/RED/CRITICAL labels, readiness levels, verification gates, and human-approval recommendations.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
