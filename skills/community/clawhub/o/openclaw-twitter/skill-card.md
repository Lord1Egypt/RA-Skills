## Description:

Searches and reads X/Twitter profiles, timelines, mentions, followers, tweets, trends, lists, communities, and Spaces, and publishes posts after user OAuth authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to monitor, search, and analyze X/Twitter activity and to publish posts or media through an OAuth-based workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The posting client can expose the AISA API key in command output or relay requests.

Mitigation: Use only an AISA key that can be rotated, avoid sharing command output that may contain credentials, and rotate the key after suspected exposure.

Risk: Search terms, private drafts, credentials, and media may be processed by AISA or Twitter/X services.

Mitigation: Avoid sensitive search terms or private draft content unless the user accepts that external processing.

Risk: A custom TWITTER_RELAY_BASE_URL can send credentials and media to an arbitrary relay endpoint.

Mitigation: Use the default relay or a trusted HTTPS endpoint, and review any custom relay configuration before posting.

Risk: OAuth-enabled posting can publish public content from the authorized account.

Mitigation: Require explicit user approval before public posts and do not report success until the publish response confirms completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-twitter)
- [OpenClaw Twitter OAuth Posting Workflow](references/post_twitter.md)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw Homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return authorization URLs, tweet IDs, tweet links, API responses, and status details.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
