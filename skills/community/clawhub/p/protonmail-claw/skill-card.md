## Description:

Manage Proton Mail email through Playwright browser automation, including login, reading messages, sending mail, and mailbox management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christopher-schulze](https://clawhub.ai/user/christopher-schulze)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate Proton Mail inbox access and message sending through a browser session when no API or IMAP workflow is used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and send mail from a Proton Mail account.

Mitigation: Use only accounts you control, review actions before sending messages, and avoid running the automation with elevated privileges.

Risk: The skill handles sensitive email credentials and browser sessions.

Mitigation: Store credentials outside source files, protect environment variables and session cookies, and rotate credentials if exposure is suspected.

Risk: The artifact includes bot-detection evasion settings and disabled Chromium sandboxing.

Mitigation: Remove stealth settings and no-sandbox launch arguments before use, keep browser sandboxing enabled where possible, and pin dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christopher-schulze/skills/protonmail-claw)
- [Publisher profile](https://clawhub.ai/user/christopher-schulze)
- [Proton Mail](https://proton.me/mail)
- [Proton account login](https://account.proton.me/login)
- [Proton Mail inbox](https://mail.proton.me/inbox)
- [Proton Mail compose](https://mail.proton.me/compose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Playwright, and Chromium; examples rely on browser automation against Proton Mail web pages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
