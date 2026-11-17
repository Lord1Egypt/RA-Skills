## Description:

Automatically scrapes, processes, and generates daily news digests from Chinese news sources with formatted summaries, source attribution, and original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zigu-creator](https://clawhub.ai/user/zigu-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up automated Chinese news monitoring, scrape configured sources, filter and deduplicate articles, and produce daily digest files for review or distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scrapes external websites and stores full article content in a local SQLite database.

Mitigation: Run it only in environments where broad web fetching and local retention of news content are acceptable, and configure retention or cleanup for the database.

Risk: The optional LLM stage can transmit article content and uses API credentials.

Mitigation: Enable LLM summarization only with trusted HTTPS endpoints and credentials that are appropriate for the data being processed.

Risk: Security evidence flags disabled TLS checks and missing URL allowlisting, redirect or IP validation, and retention controls.

Mitigation: Review and remediate these issues before running on sensitive internal networks or with valuable credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text files with source attribution, original links, and setup or configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a workspace Markdown digest and a timestamped desktop text digest; optional LLM summarization uses configured API credentials.]

## Skill Version(s):

1.0.23 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
