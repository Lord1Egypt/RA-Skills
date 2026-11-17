## Description:

Control a Mac from the terminal with the `macos` command (Calendar, Reminders, Contacts, Mail, Messages, Notes, Safari, Photos, Music, files, windows, screenshots, OCR, the Accessibility tree and system settings), where every command that returns data prints JSON with --json; run `macos doctor --for-agent` before anything else.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuaudio](https://clawhub.ai/user/manuaudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and manage a macOS system through the `macos` command, including productivity apps, files, windows, and system settings. Run `macos doctor --for-agent` first to check permissions and capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents sensitive macOS actions, including Keychain access and settings changes; the security review rates it benign with medium confidence.

Mitigation: Run `macos doctor --for-agent` first, review the permissions and capabilities each intended command needs, and have a person approve changes or other write actions.

Risk: The security review recommends separate review of out-of-scope README installation instructions.

Mitigation: Review those README instructions independently before using them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/manuaudio/skills/macos-cli)
- [Project installation README](https://github.com/manuaudio/macos-cli#install)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands that return data can print JSON with --json.]

## Skill Version(s):

0.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
