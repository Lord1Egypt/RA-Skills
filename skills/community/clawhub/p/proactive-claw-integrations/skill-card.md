## Description:

Optional network and automation helpers for Proactive Claw core: GitHub/Notion cross-skill context, team calendar awareness, daemon installer, and optional ClawHub OAuth bootstrap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googlarz](https://clawhub.ai/user/googlarz)

### License/Terms of Use:


## Use Case:

Developers and operators who already use Proactive Claw use this add-on to opt in to GitHub, Notion, team calendar, background scheduling, and ClawHub OAuth helper workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent background scheduler may run proactive workflows every 15 minutes after installation.

Mitigation: Install the daemon only when persistent automation is desired, review the core daemon behavior first, and use the documented launchd or systemd controls to disable it.

Risk: Calendar, event title, GitHub, Notion, and ClawHub OAuth metadata can include sensitive local or team context.

Mitigation: Enable only the integrations needed, confirm team calendar sharing is intentional, and keep strict privacy deployments on the core skill without this add-on.

Risk: Optional remote OAuth credential fetching depends on a ClawHub token and a configured credential hash pin.

Mitigation: Use the remote OAuth helper only when the opt-in policy setting and SHA-256 pin are configured; otherwise provide credentials through the standard local setup path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googlarz/skills/proactive-claw-integrations)
- [Publisher profile](https://clawhub.ai/user/googlarz)
- [Security notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the proactive-claw core skill; integrations are opt-in and may rely on authenticated GitHub, Notion, calendar, or ClawHub credentials.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
