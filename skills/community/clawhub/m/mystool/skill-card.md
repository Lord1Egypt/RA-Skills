## Description:

Mystool helps an agent manage Miyoushe accounts through SMS, QR, or Cookie login, then perform MiYoCoin tasks, China-server game sign-ins, game note lookups, goods browsing, redemptions, reservations, cross-platform account linking, and proxy configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carcloud-ml](https://clawhub.ai/user/carcloud-ml)

### License/Terms of Use:

MIT-0

## Use Case:

External Miyoushe users and skill operators use this skill to automate account-bound Miyoushe workflows, including daily tasks, China-server game sign-ins, account status checks, and MiYoCoin goods redemption. Operators should deploy it only where they trust the host environment with reusable Miyoushe session cookies.

### Deployment Geography for Use:

China mainland Miyoushe services; deployment may be global where those services are reachable.

## Known Risks and Mitigations:

Risk: The skill handles reusable MiHoYo session cookies and stores account/session data locally.

Mitigation: Install and operate it only in a trusted host environment, restrict file access to the skill data directory, and remove stored accounts when access is no longer needed.

Risk: Proxy routing can expose phone login and session traffic to the proxy provider.

Mitigation: Use the proxy feature only with a trusted proxy provider and avoid configuring shared or unvetted proxy endpoints.

Risk: Cross-platform account linking and redemption commands can copy access or spend points with limited confirmation.

Mitigation: Review account-link requests and redemption targets before use, and limit access to channels where the operator trusts the sender identity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carcloud-ml/skills/mystool)
- [Publisher profile](https://clawhub.ai/user/carcloud-ml)
- [mihoyo_sms_login](https://github.com/NuoManDai/mihoyo_sms_login)
- [MihoyoBBSTools](https://github.com/Womsxd/MihoyoBBSTools)
- [nonebot-plugin-mystool](https://github.com/Ljzd-PRO/nonebot-plugin-mystool)
- [Mys_Goods_Tool](https://github.com/Ljzd-PRO/Mys_Goods_Tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown responses with occasional shell command snippets and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate QR-code links, account status summaries, task results, sign-in results, product lists, redemption status, schedule status, and proxy configuration confirmations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
