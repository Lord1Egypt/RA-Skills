## Description: <br>
Analyze and prioritize GitHub repository issues using fixability signals, then produce a structured issue-analysis report with root cause hypotheses and fix approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to triage GitHub issues for open-source contribution targeting, sprint planning, backlog grooming, and bug-fix selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use an authenticated GitHub CLI session to fetch issue and pull request data. <br>
Mitigation: Use a least-privileged GitHub token where possible and confirm the authenticated account before running repository queries. <br>
Risk: The generated issue-analysis.md report could overwrite an existing workspace file. <br>
Mitigation: Check for an existing issue-analysis.md before writing and choose a new path when the existing file matters. <br>
Risk: Issue scores and fix hypotheses can be incomplete when issue threads are stale, ambiguous, or missing maintainer context. <br>
Mitigation: Review selected issues and proposed fixes against the current issue thread and repository state before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sliverp/issue-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/sliverp) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with issue scores, selected candidates, root cause hypotheses, and fix approaches.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes issue-analysis.md in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
