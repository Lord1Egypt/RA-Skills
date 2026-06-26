## Description: <br>
Analyze GitHub pull requests for security risks and determine if a PR is safe to merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerdvana-labs](https://clawhub.ai/user/nerdvana-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and reviewers use this skill to assess GitHub pull requests before merging, with attention to exposed secrets, large changes, and sensitive file edits. It returns a risk level, key issues, and a merge recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private-repository analysis can require sending a GitHub token to a third-party analyzer service. <br>
Mitigation: Prefer public repositories. For private repositories, use a fine-grained read-only token scoped to one repository, avoid broad or long-lived tokens, and revoke the token after use. <br>
Risk: The analyzer service can fail or return an incomplete response. <br>
Mitigation: Report failed or invalid analysis instead of assuming the pull request is safe, and require manual review before merging. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/nerdvana-labs/pr-risk-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with risk level, issue bullets, and merge recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a repository name, pull request number, and optional GitHub token for private repositories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
