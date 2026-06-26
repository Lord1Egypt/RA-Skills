## Description: <br>
Reviews recently changed code across reuse, quality, and efficiency, produces an actionable cleanup checklist, and can apply selected conservative fixes before a PR or refactor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill after implementing code, before opening a PR, or before refactoring to identify reuse, quality, and efficiency cleanup opportunities and choose which conservative fixes to apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous cleanup requests may cause the agent to inspect or modify code beyond the user's intended scope. <br>
Mitigation: Invoke the skill with an explicit scope and review proposed diffs before accepting edits. <br>
Risk: Refactoring edits can unintentionally change behavior if applied too broadly. <br>
Mitigation: Start from the generated checklist, choose which findings to apply, and run appropriate project review or tests after changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-simplify) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown cleanup report with file:line findings, severity labels, optional code edits, and suggested shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a conservative refactoring posture; broad renames, dependency installation, formatter runs, tests, and builds require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
