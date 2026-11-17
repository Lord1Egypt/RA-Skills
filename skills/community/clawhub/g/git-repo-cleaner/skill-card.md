## Description:

Git Repo Cleaner audits Git repositories for stale or merged branches, large files, repository bloat, maintenance issues, and optional cleanup script generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Git repositories before maintenance work, identify stale branches and large files, and generate reviewable cleanup scripts when they choose to act on findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cleanup scripts can delete branches and run aggressive garbage collection with immediate pruning if executed without review.

Mitigation: Review every generated command, confirm the intended repository, and keep backups or remote copies before running cleanup output.

Risk: The cleanup output can affect the wrong repository if commands are run from an unintended location or reused without checking paths.

Mitigation: Bind cleanup work to the intended repository path and re-run the audit in that repository before executing any generated shell commands.

Risk: Force-delete mode can remove branches even when normal safe deletion would refuse them.

Mitigation: Avoid --force-delete unless the branch state is understood and recoverable from backups or remotes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/git-repo-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Text, JSON, or Markdown audit reports; optional bash cleanup script printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git CLI; supports configurable checks, stale branch age, and minimum file size thresholds; exits 1 when issues are found.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
