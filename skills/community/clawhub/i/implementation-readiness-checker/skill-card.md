## Description: <br>
Checks whether a project is ready for implementation by organizing supplied scope, resource, environment, and dependency information into a structured readiness review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project implementers, delivery leads, and customer-facing teams use this skill before kickoff to identify ready conditions, missing prerequisites, high-risk blockers, suggested actions, start thresholds, and ownership items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script can inspect files or directories supplied as input and can write a report to an output path. <br>
Mitigation: Run it from a narrow workspace, avoid home directories or credential stores, and review the chosen output path before writing. <br>
Risk: Readiness conclusions depend on user-provided project information and may be incomplete when prerequisites are missing. <br>
Mitigation: Treat generated reports as review drafts and confirm missing items, ownership, and start thresholds with project stakeholders before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/implementation-readiness-checker) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON readiness reports, with optional local shell command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report file when an output path is provided; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
