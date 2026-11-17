## Description:

Code Sync helps an agent batch-sync Git repositories under a configured base directory by scanning repository status and pushing or pulling changes across multiple projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep many local Git repositories synchronized across machines, typically by pushing work at the end of a session or pulling updates at the start of one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk sync actions can push or pull changes across many repositories.

Mitigation: Verify the configured base directory and review the repositories to be touched before allowing batch operations.

Risk: Automatic push or pull behavior can affect repositories without per-repository confirmation.

Mitigation: Prefer adding an explicit confirmation step before bulk push or pull operations, especially in shared or production repositories.

Risk: Repository scan output may expose credential-bearing remote URLs.

Mitigation: Avoid Git remote URLs that contain credentials and review summaries before sharing logs or output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niracler/skills/nini-code-sync)
- [Release v0.3.0 changelog](https://github.com/niracler/skill/releases/tag/v0.3.0)
- [Git documentation](https://git-scm.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and repository status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scan helper emits JSON repository status fields including paths, branch names, remotes, dirty counts, upstream status, ahead/behind counts, and fetch errors.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
