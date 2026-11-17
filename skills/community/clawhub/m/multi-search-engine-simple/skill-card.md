## Description:

Provides a China-focused set of 10 free search engine shortcuts for searching current information on the internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose a China-focused search shortcut and form a query URL for the selected search provider. It is intended for direct search access, not aggregation across all listed engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to the selected external search engine.

Mitigation: Avoid sensitive or confidential terms and review the chosen search provider before opening the generated query URL.

Risk: The skill is China-focused and does not provide broad global search coverage or aggregate every engine by default.

Mitigation: Select the search engine intentionally and verify important results with additional sources when broader coverage is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhc888007/skills/multi-search-engine-simple)
- [Skill definition](artifact/SKILL.md)
- [Search engine configuration](artifact/config.json)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with search URL templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search terms may be inserted into external search URL templates; the skill does not aggregate every listed engine.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
