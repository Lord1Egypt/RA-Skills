## Description:

Accesses and searches Apple Contacts on macOS using AppleScript for contact names, phone numbers, email addresses, and full address-book details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neriros](https://clawhub.ai/user/neriros)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on macOS use this skill to let an agent look up contacts, find phone numbers or email addresses, and retrieve address-book details from Apple Contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Contacts permission for a local helper to read address-book data.

Mitigation: Install only when that access is acceptable, and approve the macOS Contacts prompt only for trusted package contents.

Risk: The published artifact references scripts/contacts.applescript, but that file is not included.

Mitigation: Confirm the package source supplies the AppleScript before relying on the skill for contact lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neriros/skills/macos-contacts)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text contact search results and contact details from osascript commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS only; requires user-granted Contacts permission; the published artifact references scripts/contacts.applescript, which is not included.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
