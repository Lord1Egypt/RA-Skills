## Description:

Insight Radar scans recent news, applies CORE analysis, generates personalized strategic briefings, and records selected events, concepts, and patterns into an agent knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kedoupi](https://clawhub.ai/user/kedoupi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to produce daily or on-demand strategic news briefings, personalize execution guidance from user context, and preserve selected news-derived concepts or patterns for later agent reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores daily web-derived news analysis under memory/news-log and may promote selected ideas into knowledge-base files.

Mitigation: Review retention expectations before installation and periodically inspect generated memory/news-log and knowledge-base content.

Risk: The skill depends on external skills that may not be pinned or independently audited.

Mitigation: Pin or audit core-prism and news-source-manager before using this skill in a controlled workflow.

Risk: Scheduled runs can repeatedly collect and preserve personalized news analysis without direct per-run review.

Mitigation: Review or disable scheduled triggers unless the workspace owner expects recurring news ingestion.

Risk: Optional Feishu or Bitable export paths may send personalized briefing content to a third-party service.

Mitigation: Confirm the export destination and data policy before enabling any external delivery workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kedoupi/skills/insight-radar)
- [README](README.md)
- [Example Output Format](references/example-output.md)
- [Category Configuration Guide](references/category-config.md)
- [Category Recommendations](references/category-recommendations.md)
- [core-prism dependency](https://clawhub.ai/kedoupi/core-prism)
- [news-source-manager dependency](https://clawhub.ai/kedoupi/news-source-manager)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown briefing with links, CORE analysis, cognitive digest entries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local news-log and knowledge-base Markdown files when run by an agent with the configured filesystem permissions.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
