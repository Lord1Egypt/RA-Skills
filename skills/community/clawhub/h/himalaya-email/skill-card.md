## Description: <br>
Himalaya Email CLI helps agents use the `himalaya` terminal client to list, read, write, reply, forward, search, and organize email over IMAP/SMTP, with multiple accounts and MML composition support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate configured email accounts from the terminal through the Himalaya CLI, including account setup, mailbox navigation, search, message composition, and mailbox organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Himalaya CLI can read and change the user's mailbox. <br>
Mitigation: Install only when the local Himalaya CLI and account configuration are trusted, and limit credentials to the intended mailbox account. <br>
Risk: Raw passwords or OAuth tokens in configuration can expose email credentials. <br>
Mitigation: Prefer app-specific passwords, OAuth tokens, pass, or a system keyring, and protect the Himalaya configuration file. <br>
Risk: Send, reply-all, forward, move, and delete commands can affect real messages or recipients. <br>
Mitigation: Review recipients, folders, and message IDs before running commands that send or modify email. <br>


## Reference(s): <br>
- [Himalaya project homepage](https://github.com/pimalaya/himalaya) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Message Composition with MML](references/message-composition.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/himalaya-email) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and TOML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for a locally installed Himalaya CLI and configuration guidance for IMAP, SMTP, OAuth2, app passwords, pass, and system keyring setups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
