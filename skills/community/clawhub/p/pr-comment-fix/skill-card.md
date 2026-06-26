## Description: <br>
Helps developers update local code based on unresolved GitCode pull request review comments, with optional confirmed replies or resolution updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to fetch unresolved GitCode PR review comments, choose which items to address, modify the local repository, validate the changes, and optionally prepare or send review-thread updates after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a GitCode access token and includes unsafe token-supply options, which could expose repository credentials if pasted into chat or passed on the command line. <br>
Mitigation: Use a minimally scoped GitCode token through a protected environment variable or secret manager, avoid pasting tokens into chat or command arguments, and rotate the token if exposure is suspected. <br>
Risk: Replying to or resolving PR review comments modifies remote PR discussion state. <br>
Mitigation: Require explicit user confirmation before sending replies or changing review resolution status, and review generated reply text before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autoxj/pr-comment-fix) <br>
- [GitCode personal access tokens](https://gitcode.com/setting/token-classic) <br>
- [GitCode API: reply to pull request comments](https://docs.gitcode.com/docs/apis/post-api-v-5-repos-owner-repo-pulls-number-discussions-discussions-id-comments) <br>
- [GitCode API: update review discussion resolution state](https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-pulls-number-comments-discussions-id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown summaries and tables, code edits, JSON context files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitCode PR URL and a GITCODE_TOKEN environment variable for API-backed actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
