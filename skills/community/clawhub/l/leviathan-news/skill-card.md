## Description:

Crowdsourced crypto news API. Submit articles, comment, and vote to earn SQUID tokens. Human-curated DeFi news with token-aware tagging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcor](https://clawhub.ai/user/zcor)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to authenticate with Leviathan News, browse crypto news, submit articles, comment on posts, vote on content, and inspect leaderboards through the Leviathan News API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private key handling can expose identity or assets if the key is reused, logged, transmitted, or stored insecurely.

Mitigation: Use a dedicated low-value wallet, keep the private key only in local secret storage or environment variables, and never reuse a wallet that holds assets.

Risk: Automated posting, voting, or article submission can create unwanted activity under the user's identity.

Mitigation: Require human review before authenticated actions, enforce strict rate limits, and monitor results before scaling automation.

Risk: Python dependency installation for wallet signing may introduce supply-chain exposure.

Mitigation: Pin and isolate dependencies before running wallet-signing examples.

## Reference(s):

- [Leviathan News Website](https://leviathannews.xyz)
- [Leviathan News API Docs](https://api.leviathannews.xyz/docs/)
- [ClawHub Skill Page](https://clawhub.ai/zcor/skills/leviathan-news)
- [TL;DR Bot Starter](https://github.com/leviathan-news/tldr-buccaneer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with curl commands, JSON examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally managed wallet private key for signing authentication messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
