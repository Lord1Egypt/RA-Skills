## Description: <br>
Manage IMAP email with the Post CLI and local daemon for reading, searching, drafting, replying, organizing, exporting, and downloading content from configured email accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use Post to let agents inspect, organize, export, and draft IMAP email through a local CLI and daemon while limiting mailbox access with scoped per-agent tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may access private mailbox contents across configured mail servers. <br>
Mitigation: Use narrow per-agent Post API keys, limit each token to the required server IDs, and avoid broad tokens in global shell profiles or shared environment files. <br>
Risk: Commands can change mailbox state by moving, archiving, trashing, junking, or bulk-changing messages. <br>
Mitigation: Confirm destructive or bulk mailbox changes before execution and prefer creating drafts for human review instead of sending mail automatically. <br>
Risk: Saved exports and downloaded attachments may contain sensitive email data. <br>
Mitigation: Write exports and attachments only to private directories and remove them when they are no longer needed. <br>
Risk: Daemon hooks and LaunchAgent auto-start can run local scripts in response to new mail. <br>
Mitigation: Enable postd hooks or auto-start only for trusted local scripts, inspect hook commands before use, and run the daemon in foreground when debugging hook behavior. <br>
Risk: Credentials or API keys can leak through command-line arguments or shared files. <br>
Mitigation: Prefer Keychain-backed credentials and scoped tokens, avoid command-line passwords, restrict token files to dedicated private workspaces, and rotate or delete unused tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/post) <br>
- [Post GitHub repository](https://github.com/Cocoanetics/Post) <br>
- [Post daemon documentation](https://github.com/Cocoanetics/Post/blob/main/Documentation/Daemon.md) <br>
- [Setup guide](SETUP.md) <br>
- [Common tasks](references/common-tasks.md) <br>
- [IDLE hook schema](references/hook-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON output from Post commands when results will be parsed or reused; requires the post and postd binaries on macOS.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, metadata, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
