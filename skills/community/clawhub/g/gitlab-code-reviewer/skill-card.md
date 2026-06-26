## Description: <br>
Reviews GitLab merge requests by fetching MR metadata and diffs, filtering non-reviewable files, generating structured engineering findings, and optionally posting inline comments through the GitLab API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neuyazvimyi](https://clawhub.ai/user/Neuyazvimyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to analyze GitLab merge request diffs, identify actionable code quality and security issues, and prepare or post review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post public merge request comments without a clear final confirmation step. <br>
Mitigation: Review the exact comments before allowing them to be posted, and use a read-only token when analysis-only behavior is intended. <br>
Risk: The skill depends on a GitLab token and a user-provided merge request URL. <br>
Mitigation: Use a dedicated, least-privileged GitLab token and verify that the MR URL host matches the intended GitLab instance before running the workflow. <br>
Risk: Temporary review comment files may contain review feedback intended for a specific merge request. <br>
Mitigation: Delete temporary comment files such as /tmp/mr_comments.json after posting or after abandoning a review. <br>


## Reference(s): <br>
- [Review Guidelines](references/review-guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Neuyazvimyi/gitlab-code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review summaries with optional JSON comment files, shell commands, and inline code suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform GitLab API reads and comment-posting when credentials permit.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
