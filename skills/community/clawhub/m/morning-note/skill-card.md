## Description:

Generates a daily investment morning note that combines macro updates, sector changes, holding anomalies, watchlist signals, and upcoming market events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy11650](https://clawhub.ai/user/dzy11650)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and investment-focused agents use this skill to generate a concise daily market briefing from macro data, sector reports, holdings or watchlist changes, and near-term event calendars. The output is intended for signal review and morning planning, not individual stock buy or sell recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio, watchlist, or other finance-related workspace context may be included in generated reports or archived summaries.

Mitigation: Use explicit investment-report prompts and review or disable IMA knowledge-base sync when those details should not be stored.

Risk: Generated market signals may be incomplete, stale, or unsuitable as trading advice.

Mitigation: Review the reported data cut-off time and underlying signals before acting, and preserve the skill's constraint against individual stock buy or sell recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dzy11650/skills/morning-note)
- [Publisher profile](https://clawhub.ai/user/dzy11650)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured Markdown report saved to a dated morning-note file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [800-1200 words; includes an explicit data cut-off time; avoids individual stock buy or sell recommendations; may sync a summary to the IMA knowledge base.]

## Skill Version(s):

1.0.0 (source: release evidence and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
