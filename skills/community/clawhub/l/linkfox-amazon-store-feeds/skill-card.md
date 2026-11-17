## Description:

Helps agents manage Amazon store Feed workflows for bulk inventory or listing data, including creating feed documents, uploading feed content to presigned URLs, submitting feeds, checking status, retrieving result documents, and cancelling feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Amazon SP-API Feeds tasks for bulk store data updates, including feed document creation, upload, submission, polling, result retrieval, and cancellation. It is intended for workflows that already have LinkFox authorization and the required Amazon Feeds permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles login, API keys, billing flows, feed uploads, and saved response files that may contain seller data or presigned URLs.

Mitigation: Use a least-privilege LinkFox key, upload only explicit feed files to fresh Amazon presigned URLs, avoid endpoint override environment variables unless you control them, and clean up saved linkfox response files after use.

Risk: Repeated bad requests, authorization failures, missing resources, or high-frequency polling can trigger Amazon SP-API store-protection cooldown behavior.

Mitigation: Stop automatic retries, fix parameters or authorization before retrying, follow retryAfter or blockedUntil when present, and reduce polling or pagination frequency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-feeds)
- [API reference](references/api.md)
- [Onboarding and authentication guidance](references/onboarding.md)
- [Amazon SP-API createFeedDocument](https://developer-docs.amazon.com/sp-api/reference/createfeeddocument)
- [Amazon SP-API getFeedDocument](https://developer-docs.amazon.com/sp-api/reference/getfeeddocument)
- [Amazon SP-API createFeed](https://developer-docs.amazon.com/sp-api/reference/createfeed)
- [Amazon SP-API getFeed](https://developer-docs.amazon.com/sp-api/reference/getfeed)
- [Amazon SP-API getFeeds](https://developer-docs.amazon.com/sp-api/reference/getfeeds)
- [Amazon SP-API cancelFeed](https://developer-docs.amazon.com/sp-api/reference/cancelfeed)
- [Amazon Feed Type Values](https://developer-docs.amazon.com/sp-api/docs/feed-type-values)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python shell commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts persist full JSON responses under a local linkfox session directory and print full or summarized JSON to stdout.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
