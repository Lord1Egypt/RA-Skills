## Description:

Control your X/Twitter account - view timeline, search tweets, post, like, retweet, bookmark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosshuman](https://clawhub.ai/user/bosshuman)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control an X/Twitter account through a local API for reading timelines, searching tweets, posting, liking, retweeting, bookmarking, and viewing user information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control an X/Twitter account, including posting and engagement actions.

Mitigation: Review intended actions before execution and use the skill only in an isolated, trusted environment.

Risk: The skill requires exported browser login cookies, which can grant account access if exposed.

Mitigation: Treat cookies.json like a password, keep it out of synced or shared folders, and rotate or revoke account sessions if exposure is suspected.

Risk: The skill depends on a downloaded executable that server security evidence describes as insufficiently scoped and unverified.

Mitigation: Install only after careful review, prefer verified releases, and favor scoped or revocable authentication such as OAuth when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bosshuman/skills/openclaw-x)
- [OpenClaw X GitHub releases](https://github.com/bosshuman/openclaw-x/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with curl command examples and concise instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to call a local API that can read from and act on an X/Twitter account.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
