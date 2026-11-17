## Description:

Autonomous social media engagement agent for Twitter, Farcaster, and Moltbook that fetches trending content, generates persona-driven replies, posts them, and tracks state to avoid duplicates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[story91](https://clawhub.ai/user/story91)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate social engagement across configured social platforms while applying persona, filtering, duplicate-prevention, and state-tracking rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post publicly to configured social accounts.

Mitigation: Use dedicated low-privilege accounts, keep scheduled execution disabled until behavior is reviewed, and inspect generated reply paths before enabling autonomous posting.

Risk: The skill uses social API credentials, Farcaster wallet or signing keys, and may spend small Farcaster write fees.

Mitigation: Use separate credentials and a minimally funded wallet, protect secrets outside shared files, and rotate keys if exposure is suspected.

Risk: Evidence security guidance reports unsafe shell execution around Farcaster keys.

Mitigation: Fix the Farcaster command execution path before providing real keys or enabling Farcaster posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/story91/skills/multi-channel-engagement-agent)
- [Persona Configuration Guide](references/persona-config.md)
- [Platform APIs Reference](references/platform-apis.md)
- [Reply Strategies Guide](references/reply-strategies.md)
- [Farcaster Agent Dependency](https://clawhub.com/skills/farcaster-agent)
- [X Developer Portal](https://developer.x.com/en/portal/dashboard)
- [Neynar Developer Portal](https://dev.neynar.com)
- [AISA API](https://aisa.one)
- [Moltbook API](https://www.moltbook.com/api/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON configuration, shell commands, state files, and plain text social replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update engagement-state.json and analytics.json, and may post public replies through configured platform APIs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
