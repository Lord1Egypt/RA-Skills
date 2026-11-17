## Description:

Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and publishes posts after the user completes OAuth in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search, monitor, and inspect Twitter/X data, then publish text or media posts through an OAuth-authorized workflow without sharing account passwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIsa API key can appear in command output.

Mitigation: Use a scoped, disposable AIsa key, avoid logging command output that contains secrets, and rotate the key if output has been captured.

Risk: A custom TWITTER_RELAY_BASE_URL can send the API key and posting payloads to an arbitrary relay endpoint.

Mitigation: Use the default trusted relay unless a custom endpoint has been reviewed and approved.

Risk: The skill can publish text and media to a real Twitter/X account after OAuth authorization.

Mitigation: Require explicit approval of the exact post text, media, and target relationship before publishing.

## Reference(s):

- [OpenClaw Twitter OAuth](references/post_twitter.md)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw Homepage](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-twitter-search)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; posting requires user OAuth authorization and can include local image or video files.]

## Skill Version(s):

1.0.5 (source: server release evidence, created 2026-03-31T03:43:16Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
