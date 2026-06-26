## Description: <br>
Implements Manus-style file-based planning to organize and track progress on complex tasks by creating task_plan.md, findings.md, and progress.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kakaxiazai](https://clawhub.ai/user/kakaxiazai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to plan, track, and resume complex multi-step work with persistent markdown files in the project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session recovery reads and prints prior Claude session content, which may expose sensitive information if prior conversations contained secrets. <br>
Mitigation: Avoid putting secrets in planning files or related conversations, and review recovery output before continuing work. <br>
Risk: Planning files are repeatedly shown to the agent, so sensitive or instruction-like content in those files can influence future actions. <br>
Mitigation: Review task_plan.md, findings.md, and progress.md before resuming work; keep untrusted external content out of task_plan.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kakaxiazai/manus-planning-with-files-2-26-1) <br>
- [Publisher profile](https://clawhub.ai/user/kakaxiazai) <br>
- [Manus Context Engineering Principles](references/reference.md) <br>
- [Planning With Files Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with inline shell commands and planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates task_plan.md, findings.md, and progress.md in the project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact metadata version 2.26.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
