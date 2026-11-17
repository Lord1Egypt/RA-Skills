## Description:

LifeLog records daily life entries to a Notion database, recognizes dates in messages, appends entries to the matching day, and supports scheduled summary analysis for emotions, events, locations, and people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[421zuoduan](https://clawhub.ai/user/421zuoduan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to capture personal life notes, store them in Notion by date, and generate daily summaries of emotions, events, locations, and people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send personal journal entries, inferred emotions, locations, and people information to a Notion database and possibly through an LLM workflow.

Mitigation: Install only after reviewing the privacy impact, avoid recording highly sensitive details, and review entries before enabling automatic summaries.

Risk: The skill needs Notion credentials and database access to write and update life-log records.

Mitigation: Use a dedicated least-privilege Notion integration and keep tokens in environment variables or a local secret store rather than edited scripts.

Risk: Automatic recording and scheduled summaries can capture more personal context than the user intends.

Mitigation: Use explicit consent and review controls for automatic capture and scheduled cron summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/421zuoduan/skills/lifelog)
- [ClawHub publisher profile](https://clawhub.ai/user/421zuoduan)
- [Notion integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and Notion database field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTION_KEY and NOTION_DATABASE_ID credentials and may call Notion APIs and an LLM workflow for summaries.]

## Skill Version(s):

1.2.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
