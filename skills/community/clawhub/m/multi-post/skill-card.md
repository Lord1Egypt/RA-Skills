## Description:

Multi-Post helps an agent adapt and publish text and image posts across platforms such as Weibo, Xiaohongshu, Zhihu, Twitter/X, Reddit, V2EX, Douban, and LinkedIn using browser automation with the user's logged-in sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffchang2024](https://clawhub.ai/user/jeffchang2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare platform-specific post drafts, attach local images where supported, publish through existing logged-in browser sessions, and receive per-platform success or failure reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish modified content and upload media from logged-in social accounts without a clear final approval step.

Mitigation: Use dry-run drafting by default, display the exact text, media, active account, and destination for each platform, and require explicit confirmation before every publish or clearly scoped batch publish.

Risk: The skill can post publicly from any supported account already logged in to the user's browser.

Mitigation: Verify the active account and target destination before publishing, and skip any platform where the account or destination cannot be confirmed.

Risk: Image handling may involve external image hosting for some destinations.

Mitigation: Ask separately before uploading media to any external image host and report when image publishing is skipped.

## Reference(s):

- [Platform Automation Flows](references/platform-flows.md)
- [Platform Content Rules](references/platform-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/jeffchang2024/skills/multi-post)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries with platform-specific post text and publish results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination platform, publish status, captured post URL, timestamp, and failure reason.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
