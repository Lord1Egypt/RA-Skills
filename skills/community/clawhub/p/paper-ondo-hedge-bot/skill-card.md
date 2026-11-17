## Description:

Guides users in configuring and operating a PaperTrade and ONDO Perps hedging bot, including mock runs, account checks, and emergency position closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and developers use this skill to configure and run a neutral hedge across PaperTrade and ONDO Perps, inspect account status, manage session keys, and close positions. It supports mock runs and real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web panel may expose saved wallet and API secrets and start or stop real trades without authentication.

Mitigation: Use mock mode by default; do not enter valuable keys or broad API credentials into the panel or expose the local service while browsing untrusted sites. Add authentication, origin and host checks, secret masking, input validation, and explicit confirmation before real trading.

Risk: Real leveraged trades can cause financial losses if the hedge executes unevenly or a position cannot be closed.

Mitigation: Review and harden the skill before use with real funds; verify settings and account status, use conservative position sizes, and be prepared to close positions manually.

## Reference(s):

- [ClawHub release](https://clawhub.ai/0xcii/skills/paper-ondo-hedge-bot)
- [Server-resolved source repository](https://github.com/0xcii/paper-ondo-hedge-bot)
- [PaperTrade](https://papertrade.xyz/)
- [ONDO Perps](https://app.ondoperps.xyz/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide mock or real trading and emergency position closure.]

## Skill Version(s):

0.1.0 (source: ClawHub release; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
