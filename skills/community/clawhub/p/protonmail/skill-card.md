## Description:

Read, search, and scan ProtonMail via IMAP bridge (Proton Bridge or hydroxide). Includes daily digest for important emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durchblick-nl](https://clawhub.ai/user/durchblick-nl)

### License/Terms of Use:


## Use Case:

Developers and email users use this skill to configure IMAP bridge access to ProtonMail, list and search inbox messages, read selected emails, and generate a daily digest of important unread messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private email access and credential handling require review before installation.

Mitigation: Prefer an official Proton Bridge setup when possible and protect credential files with restrictive permissions such as 0600.

Risk: Bridge setup can expose plaintext IMAP if bound beyond the local machine.

Mitigation: Bind bridge ports to 127.0.0.1 only and avoid remote plaintext IMAP access.

Risk: Email headers and message bodies may be printed in the terminal when commands are run.

Mitigation: Run commands only in trusted terminals and avoid sharing logs or transcripts that may contain private email content.

Risk: Unpinned Docker images or source revisions can change behavior across installations.

Mitigation: Pin Docker images or source revisions before deployment.

## Reference(s):

- [hydroxide GitHub repository](https://github.com/emersion/hydroxide.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a local ProtonMail IMAP bridge configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
