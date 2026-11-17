## Description:

Analyzes A-share price-volume momentum and portfolio positions to produce HOLD, WATCH, REDUCE, or SELL guidance with multi-factor scoring and a logic overlay for sell-signal review.

This skill is for research and development only.

## Publisher:

[xiyanjun](https://clawhub.ai/user/xiyanjun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to diagnose stock positions, scan momentum setups, and review whether technical sell signals should be acted on. Outputs are advisory analysis for human review and are not a substitute for investment judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports executable code from a local volume-price-screener skill.

Mitigation: Install and use it only when both this skill and the local volume-price-screener dependency are trusted and reviewed.

Risk: Portfolio workflows can overwrite local portfolio-related JSON files.

Mitigation: Use explicit .json portfolio filenames and keep backups before running portfolio update workflows.

Risk: HOLD, WATCH, REDUCE, and SELL outputs may be mistaken for executable trading instructions.

Mitigation: Treat all outputs as advisory analysis and review them before taking any investment action.

Risk: Chinese-only output and fundamentals/events overlays may affect how recommendations are interpreted.

Mitigation: Review the output language and overlay configuration so the basis for each recommendation is clear.

## Reference(s):

- [Pattern Rules](references/pattern_rules.md)
- [ClawHub Skill Page](https://clawhub.ai/xiyanjun/skills/hectorlee-momentum-position-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown with HOLD, WATCH, REDUCE, and SELL signals, scores, summaries, and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update local JSON portfolio files when portfolio workflows are used.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
