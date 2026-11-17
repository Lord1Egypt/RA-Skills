## Description:

Aggregates and verifies recent public information about a topic from news, official sources, social platforms, repositories, and forums, then returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[89171](https://clawhub.ai/user/89171)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent public updates about a product, technology, organization, event, competitor, or industry topic and turn them into a prioritized Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search public news, forums, repositories, and social platforms in ways that collect information about sensitive topics or communities.

Mitigation: Define the topic, language, time window, included sources, and excluded sources before use, and avoid targeting private individuals or sensitive communities without a lawful and appropriate reason.

Risk: Public-source reports can be incomplete or stale because paywalled, login-only, private, deleted, inaccessible, or fast-changing content may be missed.

Mitigation: Prefer verifiable original links and timestamps, label uncertain or outdated items, and manually review key sources before relying on the report for important decisions.

Risk: Collected findings may be retained if the agent saves them to memory.

Mitigation: Do not save findings to memory unless retention is intended and appropriate for the topic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/89171/skills/info-collector)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report with source links, timestamps, summaries, categories, and core findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topic, time window, language, regional preference, required or excluded sources, category item limits, and recency options shape the report.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
