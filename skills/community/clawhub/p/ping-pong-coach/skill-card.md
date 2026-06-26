## Description: <br>
Generates a staged table tennis coaching plan from a learner's age, gender, and years of training, including stage duration, technical focus, current-stage analysis, and estimated time to progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taradl7347c](https://clawhub.ai/user/taradl7347c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, coaches, and agent users use this skill to generate practical table tennis training plans tailored to a learner's age and training history. It combines a local stage calculator with a seven-stage curriculum reference to produce an actionable plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run a local Python helper with learner-provided numeric inputs. <br>
Mitigation: Review the command before running it and pass only intended learning-year and age values. <br>
Risk: Generated coaching plans can be incomplete when learner details are missing. <br>
Mitigation: Confirm age, training history, and any missing learner information before using the plan for training decisions. <br>


## Reference(s): <br>
- [Table Tennis Curriculum](references/curriculum.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown coaching plan with a stage-analysis section generated from a local Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses learner age and years of training when provided; marks missing learner information when inputs are incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
