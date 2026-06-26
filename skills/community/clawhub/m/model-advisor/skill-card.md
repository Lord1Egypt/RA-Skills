## Description: <br>
Model Advisor recommends Claude models from recent OpenClaw task history or a supplied task description and reports an OpenClaw gateway security score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrKangZuBin](https://clawhub.ai/user/MrKangZuBin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose an appropriate Claude model for a task and to review local gateway security posture before sharing or acting on the report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto and full modes can inspect recent local OpenClaw session messages and OpenClaw configuration. <br>
Mitigation: Use recommend mode with an explicit task description when history inspection is not desired. <br>
Risk: Security reports can reveal gateway posture such as bind mode, authentication mode, port, and denied command count. <br>
Mitigation: Treat the report as local-sensitive diagnostic output and avoid sharing it publicly without redaction. <br>


## Reference(s): <br>
- [Model Advisor ClawHub release](https://clawhub.ai/MrKangZuBin/model-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text report with model recommendation and security scoring guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw configuration and recent session messages when auto or security modes are used.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
