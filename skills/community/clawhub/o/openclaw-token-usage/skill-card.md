## Description:

Inspect token usage from local OpenClaw transcripts across a specified time range, including breakdowns by day, agent, provider, model, session, rankings, CSV exports, and Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujohn74](https://clawhub.ai/user/lujohn74)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to inspect local transcript-based token usage by day, agent, provider, model, or session and to export summaries for reporting or follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw transcript metadata across agents, which can expose sensitive usage patterns or session context.

Mitigation: Use explicit date ranges and narrow scope with --agents, --providers, and --models when a full local scan is not needed.

Risk: Reported counts depend on local transcript data and do not include IDE-side GitHub Copilot usage outside OpenClaw.

Mitigation: Describe results as transcript-based OpenClaw usage and call out that external Copilot activity is out of scope.

Risk: CSV exports may contain sensitive transcript-derived metadata and can be risky if opened from untrusted transcript sources.

Mitigation: Treat CSV exports as sensitive files and sanitize formula-prefixed cells before opening them in spreadsheet software when transcript trust is uncertain.

Risk: Timezone assumptions can change the reported date range and daily breakdowns.

Mitigation: Confirm the intended timezone before running the script and include the timezone with reported results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lujohn74/skills/openclaw-token-usage)
- [ClawHub publisher profile](https://clawhub.ai/user/lujohn74)
- [Skill definition](artifact/SKILL.md)
- [Token usage reporter script](artifact/scripts/report_openclaw_token_usage.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain-language summaries with optional JSON, CSV, and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript-based token counts are deduplicated across reset or deleted transcript copies when message identifiers and usage fields match.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
