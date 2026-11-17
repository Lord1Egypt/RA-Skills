## Description:

Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay for research, posting, likes, follows, and related workflows without sharing passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research X/Twitter content and perform explicitly approved posting, media upload, like, unlike, follow, and unfollow workflows through the AISA relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the AISA relay authority over a connected Twitter/X account for posting, media uploads, likes, follows, unlikes, and unfollows.

Mitigation: Use write commands only after reviewing the exact action, target, text or media payload, OAuth state, and explicit approval status.

Risk: The security evidence reports that write clients do not enforce the promised final approval in code.

Mitigation: Require a human-reviewed confirmation artifact before every write action, and prefer a version that enforces approval tokens for all write operations.

Risk: The security evidence reports API-key output behavior that could expose AISA credentials in logs.

Mitigation: Rotate any AISA key that may have appeared in logs and avoid sharing command output that contains credentials.

## Reference(s):

- [Post Twitter Workflow](references/post_twitter.md)
- [Engage Twitter Workflow](references/engage_twitter.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and OAuth authorization for write actions.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
