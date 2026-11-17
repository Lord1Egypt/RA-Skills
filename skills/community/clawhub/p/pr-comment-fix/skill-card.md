## Description:

Helps an agent fetch unresolved GitCode PR review comments, summarize them for user approval, apply selected local code fixes, validate the changes, and optionally reply to or resolve discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code-review agents use this skill to turn unresolved GitCode PR line comments into user-approved local code changes. It also supports controlled follow-up actions, such as drafting replies and marking discussions resolved after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitCode access tokens and PR review context that may be confidential.

Mitigation: Use a narrowly scoped GITCODE_TOKEN from the environment, avoid pasting tokens into chat or command lines, and treat generated context JSON and terminal logs as potentially confidential PR data.

Risk: Applying fixes from review comments can change local source code in ways the user did not intend.

Mitigation: Review the summarized comment list before approving edits, limit work to the selected comment range, and run local validation on changed files.

Risk: Replying to comments or resolving discussions changes the live PR discussion.

Mitigation: Only send replies or update resolve status after explicit user confirmation following local modification and validation.

## Reference(s):

- [GitCode Pull Request comment reply API](https://docs.gitcode.com/docs/apis/post-api-v-5-repos-owner-repo-pulls-number-discussions-discussions-id-comments)
- [GitCode review discussion resolve API](https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-pulls-number-comments-discussions-id)
- [GitCode personal access token settings](https://gitcode.com/setting/token-classic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local code edits, validation results, and optional GitCode API actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch produces JSON context containing unresolved PR review comments grouped by file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
