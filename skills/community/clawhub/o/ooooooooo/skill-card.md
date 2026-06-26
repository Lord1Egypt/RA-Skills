## Description: <br>
Guides an agent through batch execution of implementation plans with manual checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlreal](https://clawhub.ai/user/tlreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to execute implementation plans in batches, pause for manual review at checkpoints, verify progress, and complete final testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executing an implementation plan can change code or create commits before the direction has been reviewed. <br>
Mitigation: Use trusted plans, work on a reviewable branch, and pause at the documented checkpoints before continuing. <br>
Risk: The finalization step depends on the referenced core-finishing-branch sub-skill, which is not included in this artifact. <br>
Mitigation: Review and install or replace that sub-skill before relying on the finalization step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tlreal/ooooooooo) <br>
- [Publisher profile](https://clawhub.ai/user/tlreal) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with checklist-style checkpoints and inline skill references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation progress summaries, manual checkpoint prompts, commits, and test commands depending on the plan.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
