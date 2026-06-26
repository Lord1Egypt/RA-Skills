## Description: <br>
Read, search, and scan ProtonMail via IMAP bridge (Proton Bridge or hydroxide). Includes daily digest for important emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durchblick-nl](https://clawhub.ai/user/durchblick-nl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect a ProtonMail account through a local IMAP bridge, list and search messages, read selected messages, and generate a daily digest of important unread email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive ProtonMail content and bridge credentials to any agent or process with access to its configuration. <br>
Mitigation: Use it only with a ProtonMail account the agent is allowed to access, and store bridge credentials with restrictive file permissions or a secret manager. <br>
Risk: An IMAP bridge bound beyond the local host can expose mailbox access on the network. <br>
Mitigation: Bind bridge ports to 127.0.0.1 only and avoid exposing the bridge service outside the local machine. <br>
Risk: Unpinned or unofficial bridge software can add supply-chain and account-access risk. <br>
Mitigation: Prefer official or pinned bridge software and review bridge updates before deployment. <br>
Risk: Some list or search behavior may change email read status. <br>
Mitigation: Review mailbox state effects before routine use, especially for workflows that rely on unread status. <br>


## Reference(s): <br>
- [ClawHub ProtonMail release](https://clawhub.ai/durchblick-nl/protonmail) <br>
- [hydroxide repository](https://github.com/emersion/hydroxide.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with command-line usage and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include mailbox names, message metadata, message bodies, search results, unread email summaries, and daily digest sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
