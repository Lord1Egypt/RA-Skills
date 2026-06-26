## Description: <br>
Ghostty monitors communication channels, builds a writing-style profile, drafts replies in the user's voice, and routes responses for approval or escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use Ghostty to configure an always-on communication proxy that monitors selected channels, drafts personal replies, escalates urgent items, and queues responses for review. It is intended for users who want agent-assisted management of email, calendar, Slack, WhatsApp, Signal, or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent channel monitoring can expose private communications and account data. <br>
Mitigation: Grant access only to selected accounts and senders, prefer narrow OAuth scopes over broad IMAP access, protect stored secrets, and regularly review or delete generated profiles and logs. <br>
Risk: The skill can send messages or accept calendar invites as the user with weak safeguards. <br>
Mitigation: Disable direct sending and calendar auto-accept by default, and require approval for every outbound message or calendar change unless the user has explicitly configured a trusted exception. <br>
Risk: Nondisclosure behavior may mislead recipients about whether AI drafted or sent a response. <br>
Mitigation: Do not use nondisclosure behavior in contexts where recipients should know an AI assisted with the response. <br>


## Reference(s): <br>
- [Ghostty ClawHub release](https://clawhub.ai/fuzzyb33s/ghostty) <br>
- [Channel Monitors](references/channel-monitors.md) <br>
- [Delivery Router](references/delivery-router.md) <br>
- [Draft Engine](references/draft-engine.md) <br>
- [Voice Profile](references/voice-profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, configuration examples, and drafted communication text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local profile, configuration, pending draft, availability, and sent-log files when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
