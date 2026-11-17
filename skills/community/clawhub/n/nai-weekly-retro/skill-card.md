## Description:

Weekly Retro analyzes memory logs to identify accomplishments, recurring patterns, friction points, unfinished work, and forward-looking recommendations for the next week.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and OpenClaw users use this skill to turn weekly memory logs into a strategic retrospective with wins, patterns, friction points, carry-forward work, recommendations, and a week score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process private OpenClaw memory logs and may read SOUL.md and AGENTS.md by default.

Mitigation: Use explicit --memory-dir, --soul, and --agents paths, and review those inputs before running the pipeline.

Risk: Generated retrospectives and optional history files may preserve sensitive work patterns and personal notes as long-lived files.

Mitigation: Choose explicit --output and --history paths, restrict access to the destination vault or history directory, and review generated Markdown before sharing.

Risk: The cron example can run the skill automatically before output location and privacy expectations are reviewed.

Mitigation: Do not enable scheduled execution until configuration paths and retention expectations are confirmed.

## Reference(s):

- [Retrospective Format Reference](references/retro-format.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-weekly-retro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Obsidian-compatible Markdown with YAML frontmatter, plus intermediate JSON from the gather and analysis scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write retrospectives and history files to user-selected paths; uses only the Python standard library.]

## Skill Version(s):

1.0.0 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
