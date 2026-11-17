## Description:

Guides users through PikPak CLI setup, an informed referral choice, browser registration, and a first verified cloud download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to set up PikPak, make an informed referral choice before registration, and verify a first cloud download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the disclosed referral code may benefit the guide's sharer.

Mitigation: Explain this before registration, obtain an explicit accept or decline choice, and use an explicit empty referral value when declined.

Risk: Cloud downloads consume account quota and may continue after monitoring stops.

Mitigation: Confirm the account, authorized link, and destination before creating a task; track it by the returned task ID and tell the user that leaving does not cancel it.

Risk: A registration or download could affect an account the user did not intend to use.

Mitigation: Confirm account ownership and authorization before account queries or cloud tasks, and do not treat a logged-in status as identity proof.

## Reference(s):

- [PikPak Onboarding on ClawHub](https://clawhub.ai/pipiguai87-alt/skills/pikpak-onboarding)
- [PikPak CLI installation](https://mypikpak.com/cli)
- [PikPak CLI registration policy](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account)
- [Connected app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [Connected app transfer quotas](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell examples and JSON command previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration plans require an explicit user choice; the local planner prints a plan and does not register or log in.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
