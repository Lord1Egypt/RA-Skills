## Description:

Practical News Monitor is a configurable Chinese-language news monitoring framework for keyword-based tracking across JSON API and HTML news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrisingz-crypto](https://clawhub.ai/user/zrisingz-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure news sources and keyword categories, monitor relevant finance and geopolitical news, save structured JSON data, and generate concise Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabled news sources make outbound requests and custom headers could expose sensitive cookies or authenticated headers if added by the user.

Mitigation: Review each source URL and header before use, avoid adding secrets, and prefer unauthenticated public endpoints.

Risk: Fetched titles, links, timestamps, relevance metadata, and source statistics are saved locally under ~/shared_memory/practical_news by default.

Mitigation: Change DATA_DIR to a controlled location when needed, apply appropriate file permissions, and remove retained monitor files that are no longer needed.

Risk: Regex-based HTML parsing and source-specific API field mappings can produce incomplete or misleading summaries when source pages change.

Mitigation: Use the test mode and manually review parsed summaries before relying on them for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrisingz-crypto/skills/practical-news-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated JSON monitor data and Markdown summary reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fetched titles, links, timestamps, relevance metadata, and source statistics to local JSON files when configured sources are enabled.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
