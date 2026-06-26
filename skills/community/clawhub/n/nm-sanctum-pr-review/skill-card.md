## Description: <br>
Reviews pull requests with scope validation, requirements compliance, version checks, PR hygiene checks, and line comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub or GitLab pull and merge requests for scope alignment, requirements coverage, version consistency, PR hygiene, and actionable findings before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use authenticated GitHub or GitLab tooling to create review comments or issues. <br>
Mitigation: Review generated comments and issue text before posting, and run with credentials scoped to the target repository. <br>
Risk: Review findings may be stored in a long-lived knowledge store. <br>
Mitigation: Disable or require explicit confirmation for knowledge capture on private repositories or when findings include sensitive project details. <br>
Risk: Selected findings may be published outside the pull request workflow, including GitHub Discussions. <br>
Mitigation: Run the discussion-posting module only when the intended audience and content have been approved. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/athola/nm-sanctum-pr-review) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with inline shell commands and optional pull request comments or issue text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce classified findings, educational explanations, backlog items, local review files, and knowledge-capture summaries depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
