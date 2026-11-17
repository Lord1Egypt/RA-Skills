## Description:

Syncs Obsidian Markdown notes into a Notion database while preserving common rich text, tables, lists, code blocks, callouts, quotes, and equations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molaters](https://clawhub.ai/user/molaters)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to configure and run a local sync from an Obsidian vault to a Notion database. It is useful when notes should become native Notion pages and blocks rather than pasted plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the sync can move existing Notion pages with matching titles to trash before creating replacements.

Mitigation: Use a least-privilege Notion integration shared only with a test database first, back up the target database, and verify titles before syncing important notes.

Risk: The Notion token may be exposed through curl subprocess command arguments.

Mitigation: Prefer replacing curl subprocess calls with an in-process HTTP client and keep the integration token narrowly scoped and rotated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/molaters/skills/obsidian-notion)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls, text]

**Output Format:** [Markdown instructions and a Python script that prints terminal status while sending Notion API requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or replaces Notion database pages from local Markdown files; terminal output reports counts, progress, successes, failures, and empty notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
