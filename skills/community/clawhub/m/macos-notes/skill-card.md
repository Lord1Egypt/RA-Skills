## Description:

Create, read, search, and manage macOS Notes through AppleScript on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaperret](https://clawhub.ai/user/lucaperret)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent create, read, list, and search Apple Notes from natural-language requests on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read from and create entries in Apple Notes on the local macOS account.

Mitigation: Confirm the requested account, folder, and note operation before running commands that access private notes.

Risk: A persistent plaintext log can retain note titles, note names, search terms, and folder or account names.

Mitigation: Review or disable the logging behavior before using the skill with sensitive personal, work, health, legal, password, or account-related notes.

Risk: Password-protected notes are skipped and cannot be read or modified by the helper script.

Mitigation: Do not rely on this skill for workflows that require access to protected notes; handle those notes directly in Notes.app.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucaperret/skills/macos-notes)
- [Project homepage](https://github.com/lucaperret/agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-over-stdin inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return plaintext or Markdown-like text from Apple Notes; create operations accept plain text or HTML note bodies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
