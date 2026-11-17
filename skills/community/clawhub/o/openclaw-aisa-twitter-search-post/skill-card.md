## Description:

Searches and reads X (Twitter) profiles, timelines, mentions, followers, tweets, trends, lists, communities, and Spaces, and publishes posts after user OAuth authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and monitor Twitter/X data, inspect profiles and conversations, and publish text or media posts through an OAuth-based workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The posting helper can expose the AISA API key.

Mitigation: Use only a dedicated, revocable AISA API key and avoid running the status, authorize, or post helper until the API-key output issue is fixed.

Risk: Credentials or post content can be sent to an arbitrary relay URL.

Mitigation: Do not set TWITTER_RELAY_BASE_URL to untrusted or HTTP destinations.

Risk: Searches, media, and post content are disclosed to AIsa as part of the skill workflow.

Mitigation: Avoid sensitive searches or media unless that disclosure is acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-twitter-search-post)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://docs.aisa.one/reference/)
- [AIsa signup](https://aisa.one)
- [OAuth posting workflow](references/post_twitter.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples, Python command examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and uses curl or Python 3 for Twitter/X read and posting workflows.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
