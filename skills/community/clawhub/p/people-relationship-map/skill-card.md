## Description: <br>
Personal CRM and relationship graph for OpenClaw that tracks people, connections, notes, and stale relationships in Obsidian-friendly Markdown plus a JSON graph index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gobiraj](https://clawhub.ai/user/gobiraj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to maintain a local personal CRM, prepare for meetings, query relationship context, and receive reminders about relationships that may need follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores names, relationship links, notes, birthdays, and contact history in local workspace files that may be synced through tools such as Obsidian or cloud storage. <br>
Mitigation: Review captured entries, avoid secrets or highly sensitive third-party information, and confirm where the people folder is synced before use. <br>
Risk: Auto-capture can persist personal relationship context from conversations when intent is clear. <br>
Mitigation: Ask before persisting ambiguous information and periodically review the generated person files and graph index. <br>
Risk: Optional weekly digests can send relationship reminders to WhatsApp or Telegram channels. <br>
Mitigation: Enable chat delivery only after confirming the digest content, target channel, and who can see that channel. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub listing](https://clawhub.ai/gobiraj/people-relationship-map) <br>
- [Project homepage](https://github.com/gobiraj/people-relationship-map) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON graph data, Mermaid graph text, shell command output, and chat-friendly digest text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local people records as Markdown files and a JSON graph index under the user's workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, _meta.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
