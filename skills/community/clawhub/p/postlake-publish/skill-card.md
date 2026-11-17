## Description:

Publish a social media post right now to one or more connected accounts (X, LinkedIn, Instagram, TikTok, Facebook, Threads, Bluesky, YouTube, Pinterest) through PostLake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postlake](https://clawhub.ai/user/postlake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish immediate social media posts through PostLake to selected profiles, account IDs, or platform subsets. It is suited for agent-assisted posting workflows where the user provides or approves the caption, media, and destination accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to live connected social accounts.

Mitigation: Install and use it only when the intended workflow is immediate publishing through PostLake.

Risk: A profile may include multiple accounts or platforms, causing a post to go to more destinations than intended.

Mitigation: Verify the exact caption, media, profile or account IDs, and platform list before each publish request.

Risk: Retries without idempotency could create duplicate posts.

Mitigation: Send a unique Idempotency-Key header for each publish request so retries replay the same result.

Risk: Some target platforms require media or may process asynchronously.

Mitigation: Check each target state and URL, poll processing posts when needed, and report failed targets separately from successful ones.

## Reference(s):

- [PostLake Publish Skill Page](https://clawhub.ai/postlake/skills/postlake-publish)
- [PostLake API Base URL](https://api.postlake.dev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTLAKE_API_KEY and user-specified profile or account targets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
