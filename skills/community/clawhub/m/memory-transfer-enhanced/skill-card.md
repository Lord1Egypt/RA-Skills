## Description:

Transfers memory files between OpenClaw agents with optional topic filtering, share-mode filtering and adaptation, or clone-mode verbatim copying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to move, share, search, preview, or back up agent memory files across known OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill's filesystem scope and promised safety checks are not reliable enough for automatic installation.

Mitigation: Review commands manually, limit source and target agent IDs to known safe workspaces, and use dry-run explicitly before transferring memories.

Risk: Clone mode can copy memory contents verbatim, including user data or secrets.

Mitigation: Avoid clone mode for memories that may contain user data or secrets; prefer reviewed share-mode transfers or manual migration for sensitive content.

Risk: Security guidance says share-mode filtering should be treated as incomplete until path validation and enforced confirmation are added.

Mitigation: Treat filtering as best effort, inspect candidate memory content before transfer, and require explicit human confirmation for any write operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/skills/memory-transfer-enhanced)
- [ClawHub Publisher Profile](https://clawhub.ai/user/codeblackhole1024)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on OpenClaw memory files and support topic filtering, share mode, clone mode, and dry-run previews.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
