## Description: <br>
Automated code review assistant that analyzes code changes, pull requests, and files for quality issues, best practices, security concerns, and style violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review local files, staged Git changes, commits, or diff files before merging or shipping code. It helps surface maintainability, style, best-practice, and common security issues in Markdown or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local repository files and Git state to produce review findings. <br>
Mitigation: Run it only in repositories and paths you intend to inspect. <br>
Risk: Repository-controlled filenames or source snippets may appear in terminal or Markdown output. <br>
Mitigation: Treat reports from untrusted repositories with normal caution before sharing or rendering them. <br>
Risk: The skill can write review reports to a user-selected output path. <br>
Mitigation: Choose report output paths deliberately and review generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/openclaw-code-review) <br>
- [Publisher profile](https://clawhub.ai/user/michealxie001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON code review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include issue summaries, per-file findings, severities, line references, and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
