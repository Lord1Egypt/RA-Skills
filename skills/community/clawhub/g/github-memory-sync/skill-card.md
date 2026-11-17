## Description:

GitHub Memory Sync helps OpenClaw users sync workspace configuration, memory files, selected skills, and related workspace assets to GitHub for backup, version control, restore, and server migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davinwang](https://clawhub.ai/user/davinwang)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and operators use this skill to back up, compare, restore, or migrate workspace memory and configuration files through a GitHub repository. It is intended for workflows where workspace state needs private versioned storage and controlled recovery across servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full sync can upload sensitive OpenClaw workspace data to GitHub.

Mitigation: Use a dedicated private repository, inspect files before full sync, and prefer narrower sync modes unless full workspace backup is required.

Risk: GitHub token exposure or overbroad token permissions could grant unintended repository access.

Mitigation: Use a fine-grained, short-lived token limited to the dedicated repository and rotate it regularly.

Risk: Scheduled backups can repeatedly push to an unintended destination if repository, branch, or workspace settings are wrong.

Mitigation: Do not enable cron until the destination repository, branch, workspace path, and token scope are explicit and verified.

Risk: Restore operations can overwrite active agent instructions, memory, skills, and workspace files from remote content.

Mitigation: Treat pull and migration as high risk; review remote contents and back up the current workspace before restore.

Risk: License evidence is inconsistent across server metadata and artifact files.

Mitigation: Confirm the effective release license before redistribution or commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davinwang/skills/github-memory-sync)
- [README.md](artifact/README.md)
- [CRON.md](artifact/CRON.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided GitHub repository and token configuration before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata; matches clawhub.yaml and README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
