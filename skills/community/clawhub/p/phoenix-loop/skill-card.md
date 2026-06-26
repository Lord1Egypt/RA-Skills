## Description: <br>
Turn agent failures into permanent improvements by diagnosing blocked tasks, extracting reusable lessons, and wiring them into local recovery skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Phoenix Loop to recover from repeated task blockers by turning diagnosed failure patterns into reusable local skill guidance and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist and reuse local failure context, which could capture sensitive task details if not filtered. <br>
Mitigation: Review generated memory and skill files, apply the bundled privacy checklist, and remove secrets, credentials, personal data, and user-specific paths before saving or publishing recovery material. <br>
Risk: Recovery steps derived from logs may be incorrect or unsafe if run automatically. <br>
Mitigation: Review generated commands and recovery steps before execution, require confirmation for changes, and keep recovery guidance scoped to the diagnosed blocker. <br>
Risk: Rollback actions can rename or remove local skill files. <br>
Mitigation: Back up local skill files before using rollback instructions and verify the target path before deleting or disabling generated recovery skills. <br>


## Reference(s): <br>
- [Privacy Security Checklist](references/privacy-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command and template blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local recovery patterns, skill templates, verification criteria, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
