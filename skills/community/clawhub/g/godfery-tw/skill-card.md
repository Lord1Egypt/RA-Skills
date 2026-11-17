## Description:

Search X (Twitter) in real time, extract relevant posts, and publish tweets/replies instantly-perfect for social listening, engagement, and rapid content ops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search X/Twitter, monitor users and trends, and automate social engagement through command-line or API-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send X/Twitter account credentials, proxy credentials, search activity, and public action requests to a third-party service.

Mitigation: Use read-only operations when possible and install only after confirming trust, credential handling, revocation, and approval controls with the provider.

Risk: Write operations can post, like, retweet, or update profile data from the connected account.

Mitigation: Avoid high-value or organization accounts unless account-level approvals and recovery controls are in place; review proposed public actions before execution.

Risk: CLI login examples accept passwords and optional TOTP codes as command arguments.

Mitigation: Avoid entering real passwords or TOTP codes through command-line arguments; prefer safer provider-supported authentication flows where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/godfery-tw)
- [OpenClaw homepage](https://openclaw.ai)
- [SkillBoss API reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python command examples, and JSON API responses from the client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; write actions require X/Twitter account login.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
