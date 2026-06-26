## Description: <br>
Coordinates PR code review, AI fix suggestions, and GitHub issue tracking so teams can decide whether a pull request is ready to merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review PR diffs across logic, security, performance, readability, and test coverage, create follow-up issues for findings, and produce a pass or blocked merge recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may write to GitHub issues, PR comments, or PR status without a clear approval gate. <br>
Mitigation: Require explicit user approval or a read-only dry run before creating issues, posting comments or statuses, invoking external coding agents, or merging PRs. <br>
Risk: Review findings and generated fix suggestions may be incomplete or incorrect. <br>
Mitigation: Have a code owner review the report, linked issues, and suggested patches before applying changes or accepting a merge recommendation. <br>
Risk: High-severity findings may send code snippets to external coding agents when those integrations are enabled. <br>
Mitigation: Use the workflow only on repositories and code snippets approved for the configured external tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/pr-quality-gate) <br>
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with severity tables, issue links, fix suggestions, and gate status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update GitHub issues, PR comments, and PR status when configured with write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
