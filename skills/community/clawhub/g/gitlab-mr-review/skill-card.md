## Description: <br>
Review GitLab merge requests using a standardized code review template, automatically fetching MR changes, analyzing the diff, and posting a review comment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujinyuan](https://clawhub.ai/user/wujinyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitLab merge requests from a supplied MR URL, inspect diffs for defects and security concerns, and publish a structured review comment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the configured GitLab CLI account to read merge request diffs and publish review comments. <br>
Mitigation: Use least-privilege GitLab credentials and review generated comments before allowing them to be posted, especially for shared or sensitive repositories. <br>


## Reference(s): <br>
- [Code review template](artifact/code-review-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/wujinyuan/gitlab-mr-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review comments with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post comments to GitLab through the user's configured glab account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
