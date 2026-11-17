## Description:

Secure Google Docs management for permission-based document creation, reading, editing, sharing, permissions, renaming, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Google Docs through the PortEden CLI, including creating, reading, editing, sharing, permission review, renaming, and trashing documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a mutable external CLI that handles credentials.

Mitigation: Install only after trusting PortEden, verify the CLI source and release before installation, and prefer a dedicated least-privilege token or account.

Risk: Google Docs and Drive access can expose or modify sensitive documents when broad scopes or unrestricted tokens are used.

Mitigation: Use tokens with only the required access, confirm Drive access is intentionally enabled, and review accessInfo or account scope before operating on documents.

Risk: Sharing and delete commands can change document availability or remove documents from normal views.

Mitigation: Manually confirm recipients, public sharing settings, and delete targets before execution; use Google Drive trash restoration when a trashed document must be recovered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porteden/skills/porteden-docs)
- [PortEden publisher profile](https://clawhub.ai/user/porteden)
- [PortEden homepage](https://porteden.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference provider-prefixed Google Docs IDs, permission settings, document text, and JSON operation files; recommends compact JSON CLI output with -jc.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
