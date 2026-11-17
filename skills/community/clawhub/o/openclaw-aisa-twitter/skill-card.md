## Description:

Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and analyze Twitter/X data, monitor accounts and trends, publish posts with OAuth authorization, and perform account interactions such as liking or following when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured AIsa API key may be exposed in command output.

Mitigation: Use a low-privilege or disposable AIsa key where possible and avoid status or authorize commands until key-printing behavior is fixed.

Risk: Relay traffic can be redirected to arbitrary HTTP(S) hosts.

Mitigation: Do not set TWITTER_RELAY_BASE_URL except to a trusted HTTPS endpoint.

Risk: Posting, liking, unliking, following, and unfollowing are live changes to the authorized Twitter/X account.

Mitigation: Review targets and content before execution, require OAuth authorization for account-changing actions, and do not report success unless the relay confirms it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-twitter)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw Twitter OAuth](references/post_twitter.md)
- [OpenClaw Twitter Engagement](references/engage_twitter.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AISA_API_KEY and Python or curl commands to call Twitter/X read, posting, and engagement workflows.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
