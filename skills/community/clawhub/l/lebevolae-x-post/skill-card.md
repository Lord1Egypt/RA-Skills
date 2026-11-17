## Description:

Automatically post text or a single local image tweet to X/Twitter using provided developer credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lebevolae](https://clawhub.ai/user/lebevolae)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social-media operators can use this skill to let an agent prepare and publish X/Twitter posts containing text or one local image from a configured account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to X/Twitter using account write credentials without defined confirmation, account scoping, or rollback safeguards.

Mitigation: Use least-privilege credentials, keep secrets out of shared configuration, and manually confirm the exact text, image, and target account before allowing a post.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lebevolae/skills/lebevolae-x-post)
- [X Developer Platform](https://developer.twitter.com)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with posting examples and credential requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish a public X/Twitter post from the configured account; supports text or one local image.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
