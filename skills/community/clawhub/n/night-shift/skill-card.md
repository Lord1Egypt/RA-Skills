## Description:

Night Shift queues coding plans for later approval and unattended execution in isolated worktrees, then verifies phases and produces reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vardhineediganesh877-ui](https://clawhub.ai/user/vardhineediganesh877-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering power users use Night Shift to queue multi-step coding work, approve plans, run phases later in isolated git worktrees, and review reports or diffs before merging. It is best for deferred repo-centric work where verification and human review are part of the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended child agents can receive broad host access during approved execution phases.

Mitigation: Install first in a disposable or dedicated workspace, keep production secrets out of the environment, and sandbox or restrict child runners before using sensitive repositories.

Risk: Filesystem and verification weaknesses may allow generated changes to proceed without enough confidence.

Mitigation: Review plans immediately before execution, use dry-run first, prefer explicit tests or lint checks, and inspect diffs before merging.

Risk: Optional model runners and notifications rely on credentials and CLIs provided by the host environment.

Mitigation: Configure tokens only in local private environment files, confirm notification recipients, and run preflight in the same user or service context used for live execution.

## Reference(s):

- [Night Shift ClawHub skill listing](https://clawhub.ai/vardhineediganesh877-ui/skills/night-shift)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON queue state, and file or worktree changes from approved phases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, git, and a writable workspace; optional Cursor, Claude, and Telegram integrations depend on host configuration.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
