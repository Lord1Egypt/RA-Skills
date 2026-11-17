## Description:

List the social accounts connected to PostLake (X, LinkedIn, Instagram, TikTok, Facebook, Threads, Bluesky, YouTube, Pinterest) and their status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postlake](https://clawhub.ai/user/postlake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to list connected PostLake social accounts, retrieve account IDs before publishing to specific accounts, and check whether any account needs reauthorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries PostLake account metadata using POSTLAKE_API_KEY.

Mitigation: Keep POSTLAKE_API_KEY scoped appropriately and avoid exposing it in shared shells or logs.

Risk: Expired account connections can prevent posting.

Mitigation: Skip accounts with status "needs_reauth" and ask the user to reconnect them before posting.

Risk: Guessing account IDs can target the wrong social account.

Mitigation: Resolve account IDs through the connected accounts endpoint before publishing to specific accounts.

## Reference(s):

- [PostLake API base URL](https://api.postlake.dev)
- [Connected social accounts endpoint](https://api.postlake.dev/v1/social-accounts)
- [Platform capabilities endpoint](https://api.postlake.dev/v1/platforms/bluesky)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account IDs, platforms, handles, and account health status from PostLake.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
