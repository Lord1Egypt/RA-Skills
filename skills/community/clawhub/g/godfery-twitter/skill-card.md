## Description:

Search X (Twitter) in real time, extract relevant posts, and publish tweets or replies for social listening, engagement, and rapid content operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media teams use this skill to search X/Twitter content, inspect users and trends, and perform account actions such as posting, liking, or retweeting through the provided API examples and Python client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send X/Twitter account credentials, 2FA codes, and proxy credentials to the SkillBoss/aisa.one service.

Mitigation: Prefer read-only use, avoid passing passwords or TOTP codes on the command line, use a dedicated low-risk account for testing, and rotate any credentials already submitted through this workflow.

Risk: Write operations can post, like, or retweet publicly from an authenticated account.

Mitigation: Review generated actions before execution, limit use to approved accounts, and monitor for rate limits or account suspension warnings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/skills/godfery-twitter)
- [OpenClaw](https://openclaw.ai)
- [SkillBoss](https://skillbossai.com)
- [SkillBoss API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python client usage, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY. Write operations require an X/Twitter account login and may perform public account actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
