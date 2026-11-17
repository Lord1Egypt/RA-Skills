## Description:

Linguistic Landscape Analyzer is a local MCP tool for sentiment analysis, keyword extraction, note listing, and Markdown weekly reports from CSV social-media text data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystaria](https://clawhub.ai/user/crystaria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, analysts, and content operations teams use this skill to analyze local social-media CSV data for sentiment, keywords, note summaries, and weekly Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CSV files and generated reports may contain copied note data.

Mitigation: Review input CSV contents before analysis, keep generated reports local when needed, and avoid sharing reports that contain sensitive or proprietary notes.

Risk: The dependency lockfile and registry source require review before installation.

Mitigation: Review or update the dependency lockfile and prefer the official npm registry when appropriate.

Risk: Dictionary-based sentiment analysis and simple Chinese tokenization can produce inaccurate NLP results.

Mitigation: Treat sentiment and keyword outputs as preliminary analysis and review them before research, operational, or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crystaria/skills/linguistic-landscape-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON text responses and generated Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CSV data and writes reports under the skill reports directory.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md changelog; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
