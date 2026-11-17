## Description:

Analyzes a local Git repository's commit history, branch state, and work in progress to generate structured daily standups, weekly reports, or sprint reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximum2974](https://clawhub.ai/user/maximum2974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to summarize local Git activity into human-facing status reports, including individual or team daily standups, weekly updates, and sprint reviews. It is useful when users need concise progress, carry-over work, and risk signals derived from repository history and current worktree state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted report parameters could be inserted into Bash commands and run unintended shell code.

Mitigation: Use trusted mode, day-count, and author values; review generated commands before execution until command templates add strict validation or structured argument passing.

Risk: The skill inspects local repository metadata and work-in-progress state, including commit messages, branch names, stash entries, and contributor emails.

Mitigation: Run it only in repositories whose Git history and working-tree metadata can be disclosed to the active agent session, and avoid repositories with sensitive commit messages or branch names.

## Reference(s):

- [Git Reporter ClawHub Skill Page](https://clawhub.ai/maximum2974/skills/git-reporter)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with concise sections, summary metrics, and optional inline shell command context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report language follows the repository's commit-message language, and daily and weekly modes aim to stay concise.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
