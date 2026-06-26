## Description: <br>
Read-only Mastodon skill. Outputs human-readable timeline summaries or raw JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patelhiren](https://clawhub.ai/user/patelhiren) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Mastodon users use this skill to inspect home timelines, own posts, mentions, and search results from a Mastodon instance without performing write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Mastodon OAuth bearer token, which could expose account data if over-scoped or leaked. <br>
Mitigation: Use a dedicated token with only the read scope, keep it secret, and revoke it from Mastodon development settings when no longer needed. <br>
Risk: Using an untrusted or mismatched Mastodon instance URL can send the bearer token to the wrong server. <br>
Mitigation: Set MASTODON_INSTANCE to the exact Mastodon server that issued the token and avoid untrusted --instance URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patelhiren/mastodon-scout) <br>
- [Publisher profile](https://clawhub.ai/user/patelhiren) <br>
- [Default Mastodon instance](https://mastodon.social) <br>
- [Alternative Mastodon instance](https://fosstodon.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable timeline summaries or raw Mastodon API JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MASTODON_TOKEN; MASTODON_INSTANCE is optional and defaults to https://mastodon.social.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
