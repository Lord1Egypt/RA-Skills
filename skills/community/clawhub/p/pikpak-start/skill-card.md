## Description:

Set up PikPak with the CLI: install, informed referral choice, browser signup, and a first verified cloud download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users use this guide to check or install the CLI, make an informed referral choice before signup, and follow a user-authorized first cloud download with task-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the disclosed referral code may provide a promotional benefit to the guide's sharer.

Mitigation: Explain this before registration and obtain the user's explicit choice; use the explicit empty referral value when they decline.

Risk: Registration and cloud downloads can affect the user's PikPak account, destination, and transfer quota.

Mitigation: Keep installation and account actions under user control, and confirm account authorization, the requested link and destination, and quota implications before proceeding.

## Reference(s):

- [PikPak Start on ClawHub](https://clawhub.ai/pipiguai87-alt/skills/pikpak-start)
- [PikPak CLI installation](https://mypikpak.com/cli)
- [PikPak CLI registration policy](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account)
- [Connected-app download speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [Connected-app transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [Upstream design and verification boundaries](artifact/references/upstream-design.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and a JSON registration plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The registration planner prints a user-reviewable plan only; account actions and cloud transfers remain user-authorized.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
