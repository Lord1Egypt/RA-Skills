## Description:

Run a repo-local scan through `skills/news-aggregator-skill`, then normalize the result into a local report contract for the collect layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to run broad domestic or overseas news scans, produce repeatable Markdown news reports, and archive raw JSON for later review. It is useful when turning current news into candidate topics for human editorial selection or downstream research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact depends on repo-local news-aggregator-skill files that were not included in the artifact.

Mitigation: Review the dependency implementation and requirements before installation or deployment.

Risk: The skill contacts configured news sources and stores raw JSON plus Markdown reports in the workspace.

Mitigation: Run it in an isolated environment with only the workspace access needed for content-production/inbox outputs.

Risk: News summaries and writing-angle recommendations can be incomplete or misleading if based only on fetched snippets.

Mitigation: Have a human verify source articles and context before using recommendations for editorial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/news-collect)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact runtime](artifact/runtime.py)
- [Artifact skill manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown report plus archived JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a standardized news-report.md under content-production/inbox and raw JSON under content-production/inbox/raw/news.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
