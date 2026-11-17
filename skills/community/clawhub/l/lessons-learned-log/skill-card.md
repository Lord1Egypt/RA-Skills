## Description:

Lessons Learned Log turns mistakes, rework, and corrections into searchable Markdown lesson entries, then prompts the agent to search those lessons before similar future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[po-et](https://clawhub.ai/user/po-et)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to maintain a persistent lessons-learned log for mistakes, corrections, rework, and near misses. It helps the agent create, search, update, merge, and retire Markdown entries before repeating similar tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent lesson records may accidentally include private context, secrets, account details, IDs, or personnel judgments.

Mitigation: Choose a specific storage folder, review entries before saving, and avoid storing sensitive data or evaluations of people.

Risk: Outdated lessons can conflict with current user instructions or changed tools and processes.

Mitigation: Use the skill's review flow to mark stale entries as outdated, merge duplicates, and treat current explicit user requirements as authoritative.

Risk: The skill may write or reorganize user files when maintaining the lesson log.

Mitigation: Agree on the storage location before first write and ask before creating directories, writing entries, or merging records when no prior location is configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/po-et/skills/lessons-learned-log)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown lesson entries, search results, checklist guidance, and inline Python or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records are stored as user-controlled Markdown files and may include a standard-library Python search script.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
