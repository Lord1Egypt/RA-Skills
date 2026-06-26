## Description: <br>
Momo helps freelancers track work time, prepare timesheet reports, and start invoicing workflows from a local shell helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kleberbaum](https://clawhub.ai/user/kleberbaum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Freelancers and solo operators use this skill to invoke a local time tracking helper for logging work, reviewing reported hours, and preparing invoice-related actions. In this version, users should treat the workflow as a prototype because the reviewed script only reports selected modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local command execution through a shell script. <br>
Mitigation: Install only if local command execution is acceptable, and inspect the script before running it. <br>
Risk: The release description claims time tracking, PDF invoices, and payment tracking, but the reviewed script currently only prints selected modes. <br>
Mitigation: Treat generated output as a prototype workflow and verify records, invoices, and payment status outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kleberbaum/momo) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local shell script with exec permission on Linux.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
