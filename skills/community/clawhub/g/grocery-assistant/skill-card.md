## Description:

Persistent pantry-backed grocery checklist for OpenClaw, intended for normal conversational use with Telegram shopping-list UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serdarsalim](https://clawhub.ai/user/serdarsalim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to maintain a persistent grocery checklist, update pantry status through normal conversation, and render Telegram shopping-list controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects grocery state changes to Telegram and reads the user's OpenClaw Telegram configuration.

Mitigation: Use a dedicated grocery Telegram account or bot, bind it only to the grocery workflow, and review the Telegram account allowlist before enabling the integration.

Risk: Broad exec approvals such as scripts/*.py would also approve utilities beyond the primary grocery wrapper.

Mitigation: Approve the specific grocery wrapper needed for normal use instead of approving every Python script in the skill directory.

Risk: The bundled session-pruning utility is overbroad for this grocery skill and can move session files.

Mitigation: Do not run the pruning utility unless it is fixed with path containment checks and a dry-run or confirmation flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/serdarsalim/skills/grocery-assistant)
- [README](artifact/README.md)
- [Setup guide](artifact/SETUP.md)
- [Agent notes](artifact/AGENTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown or plain-text grocery responses, Telegram checklist interactions, shell command invocations, and local JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads OpenClaw Telegram configuration and writes grocery checklist and Telegram polling state under the user's OpenClaw data directory.]

## Skill Version(s):

1.1.3 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
