## Description:

Memory Hamster helps agents manage local memory with hot, warm, and cold retention, learning logs, archival, search, and lesson-to-skill extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomor1984](https://clawhub.ai/user/tomor1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent a local memory workflow for daily logs, lessons, errors, feature requests, archival, search, and skill extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memory may include sensitive, stale, or inaccurate information that persists across sessions.

Mitigation: Review memory and learning entries before storing them, exclude secrets and personal data, and periodically prune or archive unwanted files.

Risk: Promoting lessons into persistent behavior files can change future agent behavior without enough user approval.

Mitigation: Require manual approval for every promoted rule, inspect the exact destination file, and keep a clear rollback path.

Risk: Scheduled reflection and archival jobs can create or move local memory files automatically.

Mitigation: Run scripts in review modes such as dry-run or skip-reflection first, confirm the target WORKSPACE, and enable cron jobs only after reviewing affected paths.

Risk: Memory search can expose snippets from local logs and learning records.

Mitigation: Limit stored content to non-sensitive data and review search results before sharing them outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomor1984/skills/memory-hamster)
- [README](README.md)
- [Skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell command output, and generated skill scaffolds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper scripts can write local memory, archive, reflection, learning, and generated skill files when run.]

## Skill Version(s):

1.0.1 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
