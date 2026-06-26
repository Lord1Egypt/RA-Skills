## Description: <br>
Tracks Microsoft Outlook email and optional Microsoft Teams messages on a Windows machine, helps surface items that may need replies, and prepares concise email reply drafts using Outlook Desktop automation and optional Microsoft Graph access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinavjp](https://clawhub.ai/user/abhinavjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees who use Outlook Desktop and optionally Teams use this skill to identify recent messages that may need replies, generate reminders, and draft short reply options for review before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects recent Outlook mail and, when enabled, Teams chats that may contain sensitive work content. <br>
Mitigation: Install only when that access is acceptable, use minimal Microsoft Graph scopes, and keep Teams scanning disabled unless tenant permissions are understood. <br>
Risk: Generated state, token cache, scan cache, and thread context files may contain message metadata or content. <br>
Mitigation: Protect or delete generated local files and do not commit populated configuration, token cache, state, or thread JSON files. <br>
Risk: Reminder messages sent to Telegram or Teams could expose confidential content to the wrong destination. <br>
Mitigation: Review the configured reminder destination before running nagging workflows and avoid shared Telegram targets for confidential work messages. <br>
Risk: Draft replies may be incomplete or unsuitable for the thread context. <br>
Mitigation: Review all generated drafts before sending; the skill is configured to create drafts or approval text rather than auto-send messages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abhinavjp/ms-outlook-teams-assistant) <br>
- [Example Configuration](references/config.example.json) <br>
- [Teams via Microsoft Graph Setup](references/teams-graph-setup.md) <br>
- [Writing Style](references/writing-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, plain-text reminders, and draft reply text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON state, scan cache, or thread context files when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
