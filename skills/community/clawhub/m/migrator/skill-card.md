## Description:

Securely migrate OpenClaw Agent config, memory, and skills to a new machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenjie2024](https://clawhub.ai/user/wenjie2024)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to export sensitive agent state into an encrypted archive and restore it on another machine. It supports migrations involving OpenClaw configuration, memory, skills, workspace paths, and host environment metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore can write files before archive integrity is fully verified.

Mitigation: Use only trusted .oca archives, restore into a controlled destination first, and fix the restore integrity issue before relying on this skill for important agent state.

Risk: Backup passwords can be exposed when passed directly on the command line.

Mitigation: Avoid command-line passwords; use an environment variable or another secret-handling method that does not persist in shell history or process logs.

Risk: .oca archives may contain sensitive agent configuration, memory, skills, and credentials.

Mitigation: Treat archives as highly sensitive files, restrict access, and transfer or store them only through trusted encrypted channels.

## Reference(s):

- [README.md](README.md)
- [ClawHub skill page](https://clawhub.ai/wenjie2024/skills/migrator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline bash commands and references to encrypted .oca archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow creates password-protected archives and can restore OpenClaw state into a target directory when the commands are executed.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
