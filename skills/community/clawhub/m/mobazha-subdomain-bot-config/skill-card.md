## Description:

Set up a custom domain and Telegram Bot for a Mobazha store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to configure DNS, TLS, and Telegram Mini App bot settings for a Mobazha storefront.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can run an internet-downloaded Mobazha installer with root privileges.

Mitigation: Use the installer only from a trusted distribution path, prefer pinned versions with published checksums or signatures, inspect it before execution, and keep a backup or rollback plan.

Risk: BotFather tokens can expose control of the store bot if shared, logged, or reused outside the intended configuration flow.

Mitigation: Ask for explicit consent before handling credentials, use bot tokens only for the immediate store configuration task, and do not store, log, or display them.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/fengzie/skills/mobazha-subdomain-bot-config)
- [Mobazha Standalone Installer](https://get.mobazha.org/standalone)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-handling guidance for BotFather tokens.]

## Skill Version(s):

0.2.0 (source: release evidence, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
