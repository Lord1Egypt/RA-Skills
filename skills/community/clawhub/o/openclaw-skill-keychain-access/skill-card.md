## Description:

Keychain Access provides macOS Keychain helpers for listing, reading, storing, updating, and deleting generic passwords through the security CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents on macOS use this skill to inspect, store, update, and remove generic Keychain passwords with explicit service/account filters and confirmation controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal Keychain secrets when raw output is explicitly requested.

Mitigation: Default to masked get output and allow raw secret disclosure only after the requester explicitly approves it.

Risk: Credential updates or deletions can change local Keychain entries.

Mitigation: Use service/account filters, dry-run previews, and confirmation prompts; reserve confirmation bypasses for explicitly approved operations.

Risk: Broad list operations on the default search list can expose credential metadata.

Mitigation: Prefer specific service/account filters and a specific keychain path where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppopen/skills/openclaw-skill-keychain-access)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with the security CLI; secret values are masked by default unless raw output is explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
