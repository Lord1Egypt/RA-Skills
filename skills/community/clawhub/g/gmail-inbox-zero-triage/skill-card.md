## Description: <br>
Gmail Inbox Zero Triage helps agents process Gmail inbox messages with AI summaries, Telegram action buttons, and batch archive, filter, unsubscribe, or view workflows through the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poisondminds](https://clawhub.ai/user/poisondminds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and Clawdbot agents use this skill to triage Gmail inboxes, review AI-generated summaries, and queue email actions before executing them in batch. It is intended for Gmail users who want faster inbox maintenance through Telegram-based interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify a full Gmail inbox. <br>
Mitigation: Install only when the publisher is trusted with broad Gmail access, and require manual review before archive, filter, or unsubscribe batches are executed. <br>
Risk: Email content may be exposed through AI summarization or Telegram workflows. <br>
Mitigation: Confirm exactly what email content is sent to external channels before using the skill, and prefer a dedicated or low-risk Gmail account where possible. <br>
Risk: The setup flow asks users to handle GOG_KEYRING_PASSWORD for non-interactive use. <br>
Mitigation: Do not store GOG_KEYRING_PASSWORD in shell startup files or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poisondminds/gmail-inbox-zero-triage) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Setup guide](artifact/SETUP.md) <br>
- [Technical overview](artifact/OVERVIEW.md) <br>
- [gog CLI](https://gogcli.sh) <br>
- [Clawdbot documentation](https://docs.clawd.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown messages with inline shell commands and Telegram action controls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May queue Gmail archive, filter, unsubscribe, and view actions for batch execution after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
