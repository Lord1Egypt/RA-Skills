## Description: <br>
Provides a development quality standards framework for checking requirements, architecture, code, dependencies, environment configuration, and delivery readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-acheng](https://clawhub.ai/user/ai-acheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill before delivery to apply quality gates, run dependency and quality checks, and follow remediation guidance for common project issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad automatic remediation authority over dependencies, code, and local project state. <br>
Mitigation: Use it in trusted repositories and require approval before editing files, changing dependencies, installing tools, creating environment files, running dev or build commands, or stopping processes. <br>
Risk: Bundled scripts can invoke npm, npx, npm audit, project build scripts, and a global depcheck installation. <br>
Mitigation: Review package scripts first and run checks in an isolated working tree or disposable environment before applying fixes. <br>
Risk: The server security verdict is suspicious because approval and rollback controls are not clearly defined. <br>
Mitigation: Keep source control checkpoints, review proposed diffs, and rerun checks after each approved change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-acheng/harness-dev-standards) <br>
- [Detailed file structure and naming standards](references/standards.md) <br>
- [Delivery checklist](references/checklist.md) <br>
- [Remediation strategies](references/remediation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local quality checks and propose remediation steps for dependencies, code, environment configuration, and build readiness.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
