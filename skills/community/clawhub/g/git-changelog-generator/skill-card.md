## Description:

Generate structured changelogs from git history with support for conventional commits, semantic versioning, multiple output formats, and agent-assisted release note drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to turn repository commit history into structured changelogs, release notes, and summaries for project history or software releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository history may contain commit messages, authors, hashes, dates, or release details that should not be exposed to the agent or included in public notes.

Mitigation: Use the skill only on repositories whose history is acceptable for the agent to read, and include authors or hashes only when they are needed.

Risk: A user-selected output path can overwrite an existing file.

Mitigation: Prefer stdout for review, or choose a non-sensitive destination path intentionally before using file output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/git-changelog-generator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON changelog content, with optional shell commands for running the generator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write to a user-selected output file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
