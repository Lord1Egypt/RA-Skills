## Description:

Connects to Gmail via IMAP, filters emails by subject prefix keyword in a specified mailbox, crawls links found in filtered emails using Playwright, converts crawled content to Markdown, and saves it to the OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive web content from Gmail messages that match a chosen subject prefix. It is suited for saving newsletter links or read-later links as Markdown files in an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable Gmail app password locally for persistent IMAP access.

Mitigation: Use a dedicated Gmail app password, review the saved config file, keep filesystem permissions restricted, and revoke the app password when access is no longer needed.

Risk: The skill automatically browses links found in matching emails from the user's machine.

Mitigation: Use a hard-to-guess subject prefix, run it only on trusted mailboxes or senders, and limit the number of links crawled for each run.

Risk: Email-supplied URLs may reach localhost, private networks, cloud metadata addresses, unsafe redirects, or other sensitive network locations.

Mitigation: Run the skill in an isolated environment or add URL review and network blocking for localhost, private networks, cloud metadata addresses, and unsafe redirects before deployment.

Risk: Setup and Playwright dependency commands may install browser packages and system dependencies.

Mitigation: Review setup commands before execution and avoid running setup or Playwright dependency installation with administrator privileges unless explicitly approved.

## Reference(s):

- [Gmail Link Archiver ClawHub Page](https://clawhub.ai/jinwangmok/skills/gmail-link-archiver)
- [Publisher Profile](https://clawhub.ai/user/jinwangmok)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [Skill Instructions](artifact/SKILL.md)
- [Gmail Link Archiver Script](artifact/references/gmail_link_archiver.py)
- [Setup Script](artifact/references/setup.sh)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter, plus terminal status output and setup/configuration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves crawled page content to a user-selected workspace path; defaults to a maximum of 50 links per run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
