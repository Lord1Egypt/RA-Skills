## Description:

Provide file protection while users work with openclaw. All file operations are version-indexed and support delete recovery and modification rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to protect project files during OpenClaw work by recording modifications, protected deletions, rollback data, and restoration metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain sensitive local files in a persistent backup store.

Mitigation: Use it only on trusted project files and avoid credential directories, .env files, cloud profiles, SSH/GPG keys, and system paths unless explicitly intended.

Risk: Protected delete and binary backup flows create full local copies that may consume storage or preserve data users expected to remove.

Mitigation: Require explicit confirmation before operations that store local copies, especially for binary files and files over 50 MB.

Risk: The first recorded version of a text file has no prior snapshot for rollback.

Mitigation: Tell users when a record has no rollback snapshot and rely on later records for rollback.

## Reference(s):

- [mmxagent-guardian ClawHub skill page](https://clawhub.ai/oreoandyuumi/skills/mmxagent-guardian)
- [file_guardian.DEPENDENCIES.md](artifact/file_guardian.DEPENDENCIES.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown/plain text status messages with shell commands and local backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local MiniVCS records, diffs, snapshots, trash entries, and binary backups under ~/.openclaw/minivcs/ when used.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
