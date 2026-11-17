## Description:

Instabot (instabot.io). Use this skill for ANY Instabot request — reading, creating, updating, and deleting data. Whenever a task involves Instabot, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read, create, update, restore, and delete Instabot users through a connected OOMOL account. It guides them to inspect each action's schema and obtain approval before state-changing or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation can introduce software and broader side effects, and the remote installer contents remain unverified.

Mitigation: Review and approve installation separately; prefer a verified, pinned release.

Risk: Automatic skill synchronization may change skill files during CLI use.

Mitigation: Review the synchronization behavior and set OO_SKILLS_SYNC_DISABLED=1 to disable it when appropriate.

Risk: Instabot writes and deletion affect account data.

Mitigation: Connect only an account trusted for this access, and retain approval for each data change, especially destructive actions.

## Reference(s):

- [Instabot homepage](https://www.instabot.io/)
- [Instabot API documentation](https://docs.instabot.io/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific commands use schema-conformant JSON payloads; the skill documents read, write, and destructive actions.]

## Skill Version(s):

1.0.5 (source: server-resolved release and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
