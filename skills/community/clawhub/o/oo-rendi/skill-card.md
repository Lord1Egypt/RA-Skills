## Description:

Operate Rendi to read, create, update, and delete stored media data and run media-processing jobs through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Rendi users use this skill to manage stored media and FFmpeg jobs, including retrieving file metadata, processing media, and managing outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags an unpinned remote installer and setup behavior that does not clearly match the Rendi data-management purpose; installer behavior is not fully understood, and two local references were unresolved. No clear malicious intent was established.

Mitigation: Review the installer and its expected local changes before installing, and consider whether you trust the installer source.

## Reference(s):

- [Rendi API Documentation](https://www.rendi.dev/docs/api-reference/introduction)
- [Rendi](https://www.rendi.dev/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Rendi ClawHub release](https://clawhub.ai/oomol/skills/oo-rendi)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Files]

**Output Format:** [oo CLI commands, JSON action payloads and results, and media outputs with a natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read Rendi data, create or modify stored resources, run media-processing jobs, or delete stored data.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
