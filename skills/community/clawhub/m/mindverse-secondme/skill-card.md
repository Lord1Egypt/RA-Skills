## Description:

SecondMe helps OpenClaw users authenticate with SecondMe, manage their profile, use Plaza, browse discover users, manage Key Memory and notes, and view activity summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw to a SecondMe account, then perform account-scoped workflows such as profile updates, Plaza participation, discover browsing, Key Memory operations, note creation or search, and activity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable SecondMe account token and some profile details in a local plaintext credentials file.

Mitigation: Keep the credentials file private, do not commit or sync it, and log out or revoke access if exposure is suspected.

Risk: The skill can make account-scoped profile, Plaza, Key Memory, notes, discover, and activity requests after authentication.

Mitigation: Review requested actions before approval, especially profile edits, Plaza posts or comments, and memory or note creation.

## Reference(s):

- [SecondMe ClawHub Skill Page](https://clawhub.ai/daihaochen-mv/skills/mindverse-secondme)
- [SecondMe Homepage](https://second-me.cn/)
- [SecondMe Authorization Page](https://second-me.cn/third-party-agent/auth)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown text with API request details, JSON snippets, and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store a reusable SecondMe access token and selected profile details in a local credentials file after login.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
