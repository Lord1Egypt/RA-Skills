## Description:

Transfer memory files from one OpenClaw agent to another for migration, context sharing, or backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to list local agent memories, preview transfers, and copy selected memory files between trusted same-user OpenClaw agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent OpenClaw agent memory and may replace existing target memory files.

Mitigation: Run --dry-run first, review the source and target memory files, and keep backups before transferring.

Risk: The security evidence reports weak path scoping and cautions against untrusted agent IDs or path-like values.

Mitigation: Use only trusted same-user agent identifiers and avoid passing path-like values as agent IDs or file names.

Risk: The security evidence says the artifact overstates privacy protections and transfers should be treated as verbatim replacements rather than filtered sharing or safe merges.

Mitigation: Inspect source memory files for secrets or private context before transfer and do not rely on the skill to remove sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/skills/memory-transfer)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem changes when transfer mode is run without --dry-run.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
