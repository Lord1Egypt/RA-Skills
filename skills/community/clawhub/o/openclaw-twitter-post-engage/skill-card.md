## Description:

Search X/Twitter profiles, tweets, trends, and run OAuth-approved posting, like, follow, and related workflows through the AISA relay without sharing passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research X/Twitter content and perform user-approved posts, replies, quotes, likes, follows, and unfollows through relay-backed Python commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media upload workflows can send arbitrary readable local files to the relay.

Mitigation: Use only explicit, reviewed media paths from the workspace and avoid passing sensitive local files.

Risk: The AISA relay receives OAuth-backed authority for Twitter/X posting and engagement actions.

Mitigation: Install only when the publisher and relay are trusted, review OAuth scopes, and require explicit confirmation before public write or engagement commands.

Risk: The AISA_API_KEY is sent in request bodies as well as headers by the current clients.

Mitigation: Prefer a restricted or rotating API key and avoid exposing command payloads in shared logs.

## Reference(s):

- [OpenClaw Twitter OAuth](references/post_twitter.md)
- [OpenClaw Twitter Engagement](references/engage_twitter.md)
- [AISA homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and explicit confirmation flags for public write or engagement actions.]

## Skill Version(s):

2.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
