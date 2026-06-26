## Description: <br>
Auto-discovers Polymarket markets that match configured keywords, tags, and volume criteria, then previews or imports matching markets into Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Polymarket for markets matching configured keywords, volume thresholds, and categories, then dry-run or import matching markets into a Simmer workspace on a scheduled cadence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live scheduled use can change the user's Simmer account and consume import quota. <br>
Mitigation: Start with dry run, keep max_per_run and filters conservative, and enable --live or cron only when recurring imports are intended. <br>
Risk: The skill depends on a Simmer API key for live account operations. <br>
Mitigation: Store SIMMER_API_KEY securely, avoid logging or sharing it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DjDyll/polymarket-market-importer) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; runtime output is plain text with an optional JSON automaton summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; dry run is the default, live imports require --live, and the artifact defines a six-hour cron schedule.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
