## Description:

Daily morning briefing generator that aggregates domestic and international news, finance updates, industry developments, and policy items into a structured Markdown briefing with action suggestions and optional scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, founders, investors, and teams use this skill to quickly review daily news, finance, technology, policy, and international developments before morning meetings. It produces concise briefing files and can support recurring scheduled generation when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional recurring schedule or push behavior may generate or send briefings at an unexpected time or to an unintended recipient.

Mitigation: Confirm the schedule, recipient, output path, and disable procedure before enabling daily automation.

Risk: The security evidence notes that SECURITY.md references a script audit, but no script is included in this artifact.

Mitigation: Treat the script audit as stale unless the referenced script is provided and reviewed with the release artifact.

Risk: Daily briefings can contain incomplete, stale, or simulated news data depending on the configured sources.

Mitigation: Review generated briefings before operational use and configure trusted news sources for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/morning-briefing-gen)
- [Publisher profile](https://clawhub.ai/user/johnsmithfan)
- [README](artifact/README.md)
- [README.en.md](artifact/README.en.md)
- [SECURITY.md](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown briefing saved to the workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are date-oriented and may include categorized news summaries, source links, and action suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
