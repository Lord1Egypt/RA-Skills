## Description: <br>
Read, search, organize, and draft email through NeoMutt and w3m while saving outgoing messages as drafts unless sending is explicitly approved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elmoyeldo](https://clawhub.ai/user/elmoyeldo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal-oriented users use this skill to operate an IMAP mailbox through NeoMutt: browse and search inboxes, read HTML email via w3m, organize folders, archive messages, and draft replies or new messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials may be exposed if stored directly in a persistent NeoMutt config that is synced or shared. <br>
Mitigation: Use an app-specific password where available and prefer NeoMutt secret retrieval such as imap_pass_cmd, an OS keychain, or a password manager. <br>
Risk: Agent-assisted email sending can create unintended outbound messages if sending is enabled without explicit user approval. <br>
Mitigation: Keep sending disabled by default and save outgoing messages as drafts unless the user explicitly approves sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elmoyeldo/neomutt-commander) <br>
- [Project homepage](https://github.com/LogicalSapien/agent-skills/tree/main/clawhub/neomutt-commander) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email sending should remain disabled unless explicitly approved; outgoing messages default to drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
