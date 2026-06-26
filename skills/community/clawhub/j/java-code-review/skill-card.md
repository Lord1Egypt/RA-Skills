## Description: <br>
Reviews GitLab branch or commit changes for Java projects across security, performance, correctness, maintainability, and testing, then produces a structured CR report and merge guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyuzhy](https://clawhub.ai/user/zhouyuzhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Java developers and code reviewers use this skill to review GitLab branch or commit changes before merging, identify critical and high-priority issues, and produce a structured CR report with merge recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide GitLab merge actions that affect repository branches. <br>
Mitigation: Confirm the exact project, source branch, target branch, and merge intent before approving any merge action. <br>
Risk: Generated CR reports may include repository details, security findings, or sensitive implementation context. <br>
Mitigation: Keep reports private and use a limited-scope GitLab token when retrieving diffs or preparing merge requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouyuzhy/java-code-review) <br>
- [Code review checklist](references/checklist.md) <br>
- [GitLab API reference](references/gitlab-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown CR report with tables, checklists, summaries, and GitLab API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitLab project identifier, source branch, target branch, and an appropriately scoped GitLab token before API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
