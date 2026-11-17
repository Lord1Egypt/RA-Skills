## Description:

This skill helps agents collect hot news topics from Chinese platforms, summarize the results, and cite source metadata.

This skill is for research and development only.

## Publisher:

[13923870749](https://clawhub.ai/user/13923870749)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather trending Chinese news items from supported platforms, generate concise summaries, and produce source-attributed JSON or Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-selected topics and requests to third-party news sites and hotboard services.

Mitigation: Avoid sensitive search topics, review target platform terms, and run scraping with conservative limits and delays.

Risk: Install and model dependency provenance are under-scoped, including optional summarization model dependencies.

Mitigation: Run the reviewed local scripts in an isolated virtual environment, pin and verify Python dependencies, and pin or locally vendor optional model artifacts before abstractive summarization.

Risk: Advertised summarization capability may exceed what the scripts reliably produce.

Mitigation: Treat generated summaries as drafts, verify claims against original source URLs, and prefer source-attributed output for downstream reporting.

Risk: User-provided output paths determine where JSON and Markdown reports are written.

Mitigation: Choose output paths deliberately and avoid writing reports into sensitive or shared directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13923870749/skills/newsscraper)
- [Platform scraping strategies](references/platforms.md)
- [Summarization methods](references/summarization_methods.md)
- [Hotboard API endpoint](https://uapis.cn/api/get-misc-hotboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may be JSON data files or Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include news titles, source platform, timestamp, original URL, ranking or heat where available, and summary text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
