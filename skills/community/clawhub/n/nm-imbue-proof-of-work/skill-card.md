## Description: <br>
Enforces validation and evidence before agents claim work complete, including before implementation sign-off, PR creation, or deliverable submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to require reproducible validation, test evidence, acceptance criteria, and documented blockers before claiming that work is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad trigger words such as validation, testing, proof, or acceptance criteria. <br>
Mitigation: Review whether the proof-of-work workflow is relevant before applying it to a task. <br>
Risk: Evidence logs can include sensitive task context or command output. <br>
Mitigation: Avoid recording secrets or sensitive data in evidence, and redact sensitive output before sharing. <br>
Risk: Completion claims can still be wrong if captured evidence is incomplete or misunderstood. <br>
Mitigation: Review the commands, outputs, acceptance criteria, and blocker notes before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-proof-of-work) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Atlassian definition of done guidance](https://www.atlassian.com/agile/project-management/definition-of-done) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, evidence logs, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require captured command output, timestamps, acceptance criteria, and blocker notes.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
