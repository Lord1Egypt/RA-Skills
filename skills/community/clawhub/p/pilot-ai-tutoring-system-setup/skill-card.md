## Description: <br>
Deploys an adaptive AI tutoring system with three agents that curate content, deliver lessons, and assess learners in a feedback loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and education technology teams use this skill to configure a three-agent tutoring setup for personalized lesson delivery, learner assessment, and curriculum adaptation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to approve broad OpenClaw device permissions that are not clearly limited to the tutoring setup. <br>
Mitigation: Approve only specific permission requests that are understood and necessary for the selected role; avoid granting admin, pairing, approval, or secrets access unless each permission is justified. <br>
Risk: Tutoring workflows can include learner identifiers, progress data, answers, and assessment history. <br>
Mitigation: Use synthetic or minimized learner identifiers unless consent, retention, and deletion requirements are clearly defined for sensitive education records. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with bash commands and JSON manifest snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup steps and manifest templates for content-curator, tutor, and assessor agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
