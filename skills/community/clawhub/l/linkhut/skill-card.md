## Description:

LinkHut bookmark management API integration with managed OAuth. Save, organize, search, and manage bookmarks with tags, notes, and privacy settings. Use this skill when users want to save bookmarks, search saved links, organize bookmarks with tags, or manage their reading list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage LinkHut bookmarks from an OpenClaw chat, including saving links, searching saved bookmarks, organizing tags, updating metadata, and maintaining a reading list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and permanently enable an unaudited external plugin that is not pinned to a specific version.

Mitigation: Review the ClawLink plugin package and publisher before installing, request pinned version and permission details where possible, and keep a rollback path before enabling it.

Risk: The skill can perform write operations and irreversible bookmark deletion after LinkHut is connected.

Mitigation: Require confirmation for write actions, use read operations to verify targets first, and require the exact bookmark URL before deletion.

## Reference(s):

- [LinkHut](https://linkhut.org/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkhut)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [LinkHut Skill on ClawHub](https://clawhub.ai/hith3sh/skills/linkhut)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JavaScript tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, OAuth connection guidance, bookmark tool examples, troubleshooting notes, and safety notes for write and delete operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
