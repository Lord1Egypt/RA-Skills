## Description: <br>
Iterative code review using multiple independent subagent reviews, with parallel analysis and optional automated fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciuscao](https://clawhub.ai/user/luciuscao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests or code changes through multiple independent reviewer agents, summarize findings by severity, and optionally apply fixes after user-controlled approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional automation can modify code without per-step confirmation when autoFix or autoContinue is enabled. <br>
Mitigation: Keep automation disabled for important repositories unless working on a clean branch and prepared to review or revert generated edits. <br>
Risk: Build and test commands may execute repository code. <br>
Mitigation: Approve npm build or test execution only for trusted repositories or inside a sandbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luciuscao/iterative-code-review) <br>
- [Automation Preferences](references/automation.md) <br>
- [Pre-flight Checks](references/preflight.md) <br>
- [Workflow](references/workflow.md) <br>
- [Code Review Checklist](references/checklist.md) <br>
- [Issue Severity](references/issue-severity.md) <br>
- [Final Round](references/final-round.md) <br>
- [Exit Criteria](references/exit-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown review findings with optional code edits, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by review round and severity; optional automation is controlled by user preferences.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
