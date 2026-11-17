## Description:

Git Log Tracker records Git commit metadata to a local SQLite index through post-commit hooks and provides CLI commands to query, list, summarize, label, update, and delete records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and engineers use this skill to install and manage a Git post-commit tracking CLI, persist commit metadata locally, and query commit history across repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Git hooks and global mode can affect future commits across repositories.

Mitigation: Ask for explicit scope before setup, prefer current-repository installation when appropriate, and verify or remove hooks with status and uninstall commands.

Risk: The local index stores commit metadata such as author emails, branch names, repository paths, and commit subjects under ~/.commit-logs.

Mitigation: Restrict permissions on ~/.commit-logs, avoid recording sensitive repositories, and use delete or reinstall controls deliberately.

Risk: Bulk scan installation, delete or update operations, reinstall actions, and remote installer commands can change many repositories or remove stored data.

Mitigation: Require explicit confirmation before broad or destructive commands, avoid curl-to-shell installation when a local or package-manager install is available, and back up important records before reset operations.

Risk: The artifact includes unrelated AGENTS.md and CLAUDE.md policy files.

Mitigation: Review and remove unrelated policy files before deploying the skill package.

## Reference(s):

- [Git Log Tracker Onboarding](references/ONBOARDING.md)
- [ClawHub Skill Page](https://clawhub.ai/leeshunee/skills/git-log-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, repository names, commit hashes, and SQLite-backed query results.]

## Skill Version(s):

0.7.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
