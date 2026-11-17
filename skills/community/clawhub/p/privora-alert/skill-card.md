## Description:

Helps agents configure and verify persistent threshold alerts for subscribed assets, with notifications delivered through Feishu, WeChat, or other webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangfuwu](https://clawhub.ai/user/guangfuwu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to set up, test, and enable alerts when subscribed gold, fund, or stock data crosses a chosen threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overly broad or mishandled Privora token can authorize unintended alert changes.

Mitigation: Use an operator-created token limited to the realtime-alerting preset and keep it private.

Risk: Testing or enabling alerts can send real, irreversible messages to a webhook destination.

Mitigation: Review the destination and notify recipients before testing; verify the real threshold before enabling a rule.

Risk: Stale asset data or an accidental second toggle can prevent expected notifications.

Mitigation: Check rule state and evaluation logs before retrying a toggle, and review data freshness when alerts do not fire.

## Reference(s):

- [Privora alert skill release](https://clawhub.ai/guangfuwu/skills/privora-alert)
- [Privora asset marketplace](https://privora.cn/marketplace)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell examples and alert status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alert tests may deliver real webhook messages; enabled rules persist until paused or disabled.]

## Skill Version(s):

1.0.8 (source: frontmatter, CHANGELOG.md, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
