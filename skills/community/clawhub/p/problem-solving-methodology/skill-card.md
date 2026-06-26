## Description: <br>
Structured problem diagnosis and resolution methodology for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose unclear problems, confirm root causes, compare solution options, execute changes carefully, and verify fixes before declaring resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostics may inspect logs, configuration, databases, or session state beyond the affected problem. <br>
Mitigation: Limit inspection to the affected issue and only gather evidence needed to confirm or reject the current hypothesis. <br>
Risk: Risky changes made during troubleshooting could cause data loss, privacy exposure, or downtime. <br>
Mitigation: Confirm risky changes with the user first, change one variable at a time, and keep a rollback plan. <br>
Risk: Reusable lessons could accidentally store secrets or private incident details. <br>
Mitigation: Do not store secrets or private incident details in .learnings/. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovensky1992-wk/problem-solving-methodology) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with structured diagnostic steps, option comparisons, checklists, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend writing reusable lessons to .learnings/ after resolution.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
