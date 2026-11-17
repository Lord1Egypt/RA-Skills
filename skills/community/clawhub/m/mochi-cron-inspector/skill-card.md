## Description:

Preview upcoming five-field cron occurrences with an explicit timezone, including DST transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preview upcoming run times for a five-field cron expression in an explicit IANA timezone, including daylight-saving transitions, before configuring a production scheduler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A preview can differ from the production scheduler's timezone or daylight-saving behavior.

Mitigation: Verify the production scheduler's timezone and daylight-saving behavior before activating a schedule.

Risk: Timezone data may be unavailable in the Python environment.

Mitigation: Use Python 3.10 or later and ensure operating-system timezone data or the Python tzdata package is available.

## Reference(s):

- [Input contract and supported cron fields](references/input.md)
- [Chinese usage notes](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-cron-inspector)
- [Publisher profile](https://clawhub.ai/user/hznetnewpower)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [JSON schedule preview and local JSON report, summarized in text with generated artifact paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a five-field cron expression, IANA timezone, timezone-aware cutoff, and a count from 1 to 20; search is limited to 366 days.]

## Skill Version(s):

1.0.0 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
