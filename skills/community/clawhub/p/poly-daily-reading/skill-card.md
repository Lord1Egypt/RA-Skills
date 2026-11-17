## Description:

Generates Guillaume's daily reading list by searching curated AI, LLM, full-stack development, anime, horror game, and metal music sources, deduplicating prior reads, writing Obsidian Markdown, updating Mission Control, and supporting weekly and yearly archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumemaka](https://clawhub.ai/user/guillaumemaka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation agents use this skill to generate a daily, deduplicated reading list for Guillaume, save it as an Obsidian Markdown file, notify him, and update Mission Control. The skill also supports routine weekly and yearly archive maintenance for those reading lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes named Obsidian reading-list files and updates Mission Control, which can affect a user's personal knowledge base and automation records.

Mitigation: Install only when those file and Mission Control updates are intended, and review the target paths before unattended use.

Risk: Mission Control commands use shell execution and inline JSON payloads, which can be fragile or unsafe if web-derived fields are not validated.

Mitigation: Pin the Mission Control CLI tooling, validate article titles, URLs, categories, and summaries before ingestion, and prefer structured argument passing over inline JSON where possible.

Risk: Weekly and yearly archive workflows delete source archive files after consolidation.

Mitigation: Make archive deletion confirmable or reversible, and verify the consolidated archive exists before removing daily or monthly files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guillaumemaka/skills/poly-daily-reading)
- [Publisher Profile](https://clawhub.ai/user/guillaumemaka)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown daily reading files, JSON status and ingestion payloads, and concise text summaries with shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated reading-list files and archive files, updates a read-status cache, and uses bounded source searches with deduplication against recent history.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
