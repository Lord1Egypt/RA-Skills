## Description:

Google Keep notes via gkeepapi. List, search, create, and manage notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vacinc](https://clawhub.ai/user/vacinc)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agents use this skill to interact with Google Keep notes from a CLI, including listing, searching, reading, creating, archiving, trashing, pinning, and updating notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local Google Keep token.

Mitigation: Use a Google App Password, keep the token file protected, and install only where Google Keep account access is acceptable.

Risk: The setup installs an unpinned Python dependency.

Mitigation: Use a pinned or locked dependency setup for reproducible installs.

Risk: Some commands modify notes by creating, archiving, trashing, pinning, unpinning, checking, or appending content.

Mitigation: Review note-changing commands and target note IDs before running them.

## Reference(s):

- [gkeepapi project](https://github.com/kiwiz/gkeepapi)
- [Google App Passwords](https://myaccount.google.com/apppasswords)
- [VACInc publisher profile](https://clawhub.ai/user/vacinc)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, archive, trash, pin, or unpin Google Keep notes when the corresponding command is run.]

## Skill Version(s):

1.0.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
