## Description:

Read-only Mastodon skill. Outputs human-readable timeline summaries or raw JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patelhiren](https://clawhub.ai/user/patelhiren)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect a Mastodon account's home timeline, mentions, own posts, and status search results through read-only API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bearer token can be sent to any configured instance URL because the destination is not validated.

Mitigation: Use only a read-scope token, set MASTODON_INSTANCE to the trusted HTTPS instance that issued it, do not let prompts choose --instance, and revoke or rotate the token if it may have been used with an unknown or non-HTTPS instance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patelhiren/skills/mastodon-scout)
- [Publisher profile](https://clawhub.ai/user/patelhiren)
- [Default Mastodon instance](https://mastodon.social)
- [Example Mastodon instance](https://fosstodon.org)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Human-readable timeline summaries or raw Mastodon API JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MASTODON_TOKEN; MASTODON_INSTANCE defaults to https://mastodon.social.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
