## Description: <br>
Reviews user-modified code such as diffs or PRs, provides best-practice recommendations, analyzes cost-effectiveness, and outputs a code score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review changed code, PRs, or selected files for correctness, readability, maintainability, performance, security, and test coverage. It is intended to produce a structured review report with prioritized recommendations, cost-effectiveness analysis, and a numeric code score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger on broad requests for best practices, cost-effectiveness analysis, or code scoring. <br>
Mitigation: Invoke it explicitly for diffs, PRs, or changed files and confirm the intended review scope before relying on the output. <br>
Risk: Review recommendations and scores may be incomplete or misleading when the supplied code context is partial. <br>
Mitigation: Provide the relevant diff, files, tests, and project conventions, then review proposed changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/modified-code-review) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with prioritized findings, optional code snippets, cost-effectiveness analysis, and a score] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blocker findings, must-change or optional recommendations, and a 0-100 code score with an A-E grade.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
