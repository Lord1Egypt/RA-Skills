## Description:

Create, inspect, and restore versioned OpenClaw state backups with rollback safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwangyy](https://clawhub.ai/user/danielwangyy)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to create, inspect, verify, and restore OpenClaw state backups for routine snapshots, migrations, recovery from configuration mistakes, and rollback after breakage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restoring a crafted archive can write files outside the intended OpenClaw state paths.

Mitigation: Install only if you trust the backup archives you will restore; use verify and dry-run, and avoid untrusted archives until restore_state.py validates tar members and enforces destination containment.

Risk: Generated backups may contain sensitive memory, session data, local skills, host metadata, and OpenClaw configuration.

Mitigation: Treat generated backup archives and restore reports as sensitive files and store or share them only in protected locations.

## Reference(s):

- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [ClawHub skill page](https://clawhub.ai/danielwangyy/skills/openclaw-state-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell command examples; bundled scripts produce tar.gz backup archives, manifest JSON, and restore report JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checksum verification, dry-run restore planning, include/exclude filters, compatibility checks, and rollback backup reporting.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
