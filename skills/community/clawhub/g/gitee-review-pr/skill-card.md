## Description:

Use this skill to review Gitee pull requests through the Gitee MCP Server when the user asks for a PR review, code review, pull request check, "review this PR", "review-pr", or "look at this pull request".

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to review Gitee pull requests, inspect PR details and diffs, classify findings by severity, and prepare structured review comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish review comments to Gitee pull requests without clearly requiring user confirmation.

Mitigation: Require the agent to show the draft review and receive explicit approval before calling comment_pull.

Risk: Optional local git and file inspection could examine unintended repository context.

Mitigation: Limit local git or file inspection to the intended repository before running the review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oschina/skills/gitee-review-pr)

## Skill Output:

**Output Type(s):** [analysis, markdown, API calls, guidance]

**Output Format:** [Markdown review comment with severity-classified findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post review comments to a Gitee pull request and may use local repository context when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
