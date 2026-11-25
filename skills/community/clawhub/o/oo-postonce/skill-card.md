## Description:

Use PostOnce through OOMOL to read, create, update, and manage posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

PostOnce users with an OOMOL-connected account use this skill to list accounts and posts, publish or schedule posts, update or cancel scheduled posts, retry failed deliveries, and review analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running a remote installer that was not available for inspection and appears unrelated to its PostOnce purpose.

Mitigation: Do not install until the installer is independently verified; establish why it is needed and what it changes, and obtain approval before running it.

Risk: PostOnce write actions can publish or change posts, and cancel_post can cancel a scheduled or pending post.

Mitigation: Inspect the live action schema and confirm the exact payload and effect before write actions; explicitly approve the target before cancellation.

## Reference(s):

- [PostOnce](https://postonce.to)
- [PostOnce API documentation](https://docs.postonce.to/api-reference/create-post)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON action responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected PostOnce action and connected accounts.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
