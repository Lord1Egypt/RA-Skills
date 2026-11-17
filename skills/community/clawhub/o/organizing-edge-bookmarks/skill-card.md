## Description:

Use when organizing Microsoft Edge bookmarks or favorites when persistence matters, when folder priorities like AI/investing/social are important, or when previous bookmark edits were reverted after restart or sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenoexia](https://clawhub.ai/user/xenoexia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to plan and carry out persistent Microsoft Edge bookmark organization on a local macOS profile, with explicit profile selection, rollback capture, consent for intrusive browser control, and post-restart verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bookmark changes can affect a live browser profile and may be reverted or reshaped by Edge sync or restart behavior.

Mitigation: Confirm the exact profile and scope, capture a rollback/export and dry-run move plan, prefer live bookmark APIs, and verify structure after reload, restart, and sync settlement.

Risk: Browser restart, profile takeover, or live-profile automation can interrupt the user's active session.

Mitigation: Require explicit approval before intrusive actions and downgrade to manual instructions when approved local control is not already proven.

## Reference(s):

- [Edge Bookmarks Organization Workflow](references/edge-bookmarks-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/xenoexia/skills/organizing-edge-bookmarks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only workflow guidance for user-approved Microsoft Edge profile organization.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
