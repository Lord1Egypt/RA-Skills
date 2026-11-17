## Description:

Analyzes greyhound races, fetches data, and predicts winners/placings for upcoming races based on form, odds, and simple models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iglemanyte-ctrl](https://clawhub.ai/user/iglemanyte-ctrl)

### License/Terms of Use:


## Use Case:

External users use this skill to fetch public greyhound racing data, compare runners using form, odds, trap position, and simple scoring, and produce winner and placing predictions with concise rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Race predictions may be incorrect or misconstrued as reliable gambling advice.

Mitigation: Present predictions as informational analysis, avoid claims of certainty, and make clear that users should not rely on them as gambling advice.

Risk: Public racing websites or APIs may be unavailable, stale, or incomplete.

Mitigation: Report missing or uncertain data clearly, cite the race details used, and ask the user for a track or date when needed.

Risk: Optional local Python execution may run modeling code based on fetched data.

Mitigation: Review code and dependencies before execution and keep analysis limited to the public race data needed for scoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iglemanyte-ctrl/skills/greyhound)
- [GBGB today's trials and meetings](https://www.gbgb.org.uk/racing/todays-trials-meetings/)
- [GBGB results API](https://api.gbgb.org.uk/api/results?page=1&date={today}&track={track})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown or plain text race analysis with optional Python modeling snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces winner and placing predictions with concise reasoning; may include uncertainty notes or fetch-failure messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
