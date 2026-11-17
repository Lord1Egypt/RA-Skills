## Description:

Manages a user's news category preferences and trusted information sources in a local news-sources.json configuration for add, remove, list, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kedoupi](https://clawhub.ai/user/kedoupi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure personalized news interests and source preferences for AI briefing workflows such as insight-radar. It helps initialize, view, update, disable, and export active news categories from local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local news preferences may reveal interests such as finance, health, policy, or work focus on shared or synced machines.

Mitigation: Review or delete ~/.openclaw/workspace/memory/news-sources.json when preferences should no longer be retained.

## Reference(s):

- [Keyword templates](artifact/references/keyword-templates.json)
- [News Source Manager ClawHub page](https://clawhub.ai/kedoupi/skills/news-source-manager)
- [insight-radar ClawHub page](https://clawhub.ai/skills/insight-radar)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses and JSON-compatible configuration data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local news category, keyword, source, active-state, and search parameter settings.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
