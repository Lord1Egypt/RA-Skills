## Description:

Guides an OpenClaw agent through exporting and restoring user-owned OpenClaw workspace data as a manifest-backed zip, with dry-run review, overwrite-by-path handling, and opt-in sensitive layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobudaoyuema](https://clawhub.ai/user/zhaobudaoyuema)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to have an agent export workspace memory, persona, skills, and optional OpenClaw layers into a zip, or restore that zip into another OpenClaw environment after previewing planned writes and handling conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying an archive can overwrite existing workspace memory, persona files, skills, sessions, or configuration by path.

Mitigation: Run apply in dry-run mode, inspect EXPORT_MANIFEST.txt, back up the target OpenClaw home and workspace, and resolve or explicitly approve conflicts before any non-dry-run apply.

Risk: Optional sessions and configuration snapshots can expose transcripts, secrets, tokens, channels, and machine-specific paths.

Mitigation: Require separate user approval for each sensitive optional layer, avoid public or untrusted storage for export zips, and do not restore config or sessions unless the user accepts the exposure and overwrite risks.

Risk: The exporter can unintentionally include files outside the workspace through symlinks.

Mitigation: Avoid running the skill on untrusted workspaces with symlinks and review the dry-run path list plus EXPORT_MANIFEST.txt before sharing or applying an archive.

Risk: The included publish_npm.py script performs package publishing and is not part of normal backup or restore use.

Mitigation: Do not run publish_npm.py during ordinary skill operation; use only the pack and apply scripts for backup and restore workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobudaoyuema/skills/openclaw-user-data-pack)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [README_CN.md](README_CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated zip archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run previews and EXPORT_MANIFEST.txt are used to review planned paths before writes.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
