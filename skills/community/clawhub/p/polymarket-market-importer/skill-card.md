## Description:

Auto-discover and import Polymarket markets matching your keywords, tags, and volume criteria on a schedule, with reusable filters that control which markets are imported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Polymarket markets that match configured keywords, categories, and volume filters, preview them in dry run, and import matching markets into Simmer when run live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can import matching markets into Simmer using the configured API key.

Mitigation: Start with dry run, review matched markets, and keep max_per_run conservative before enabling --live.

Risk: Scheduled execution can repeat imports automatically under cron when configured in OpenClaw.

Mitigation: Review the cron schedule and autostart behavior before running the skill in an account that can perform live imports.

Risk: The release depends on simmer-sdk and may follow whatever version is installed by the environment.

Mitigation: Use a pinned or reviewed simmer-sdk version for serious account usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-market-importer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Console text with optional automaton JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry run is the default and live imports require the --live flag.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
