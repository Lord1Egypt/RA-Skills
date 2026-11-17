## Description:

Kids Points V2 is a Feishu/Lark family points tracker that uses SQLite storage, LLM semantic parsing, and a CLI interface to handle group and direct chat workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowboy231](https://clawhub.ai/user/cowboy231)

### License/Terms of Use:

MIT-0

## Use Case:

External families and developers use this skill to let a Feishu/Lark bot interpret natural-language points messages, update a local SQLite family ledger, and return balances or transaction summaries. Developers can also use the CLI and optional dashboard extension to integrate the ledger with scripts or local display hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot can modify a family points ledger from chat messages.

Mitigation: Restrict the bot to approved Feishu/Lark chats, review ledger entries, and back up the SQLite database before production use.

Risk: Message text can be sent to the configured external LLM.

Mitigation: Use a dedicated least-privilege LLM key and avoid sending sensitive family information through the bot.

Risk: Local subprocesses may inherit environment credentials.

Mitigation: Run the skill with a minimal environment and remove broad credential inheritance where possible.

Risk: The optional dashboard server may expose local ledger data if bound broadly or left unauthenticated.

Mitigation: Bind the dashboard to localhost or add authentication before exposing it beyond a trusted local device.

Risk: Installer and device-permission commands can weaken host security.

Mitigation: Avoid curl-piped shell installers and do not use chmod 666 for serial device access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cowboy231/skills/kids-points-v2)
- [Skill README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Dashboard Extension README](artifact/extensions/dashboard/README.md)
- [Dashboard Extension Source Referenced By Artifact Docs](https://github.com/cowboy231/kids-points-v2/tree/main/extensions/dashboard)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text chat replies and JSON CLI/dashboard responses, with Markdown documentation for setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message-processing flows can write to a local SQLite ledger; read-only CLI commands return JSON for balance, daily totals, and history.]

## Skill Version(s):

2.0.7 (source: SKILL.md frontmatter, server release metadata, and changelog released 2026-07-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
