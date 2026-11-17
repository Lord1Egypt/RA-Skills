## Description:

Creates, updates, and maintains structured identity entries for people, organizations, groups, and AI personas mentioned in conversation, with local persistent memory and verification hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace users and agents use this skill to maintain persistent local identity records for people, organizations, groups, and AI personas mentioned in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically record people, groups, relationships, and sensitive context from normal conversations into persistent local files.

Mitigation: Install only when this always-on local identity memory is desired; consider setting IDENTITY_AUTO_SCAN=false and using explicit /identity commands.

Risk: Identity files, hook logs, group links, and soul entries are retained locally and cleanup is not automatic.

Mitigation: Audit generated files regularly and manually delete or trim identity, memory, hook log, and soul files when retention is no longer appropriate.

## Reference(s):

- [Identity Manager ClawHub Page](https://clawhub.ai/cyber-bye/skills/identity-manager)
- [Identity Manager Homepage Metadata](https://clawhub.ai/skills/identity-manager)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Markdown identity entries, JSON memory indexes, local files, and brief text warnings when synchronization breaches occur]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local identity, memory, hook log, and soul context files under workspace-relative paths.]

## Skill Version(s):

2.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
