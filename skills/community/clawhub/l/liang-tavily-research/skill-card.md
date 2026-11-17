## Description:

Comprehensive research grounded in web data with explicit citations for multi-source synthesis, comparisons, current events, market analysis, and detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew77](https://clawhub.ai/user/matthew77)

### License/Terms of Use:


## Use Case:

Developers, analysts, and other external users use this skill to run Tavily-backed web research from an agent workflow and produce cited summaries, comparisons, market research, or detailed reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to Tavily using the user's Tavily API key and may contain sensitive or confidential material.

Mitigation: Avoid submitting secrets, regulated personal data, or confidential internal material as research queries.

Risk: The output-file option writes generated reports to a user-specified path.

Mitigation: Use the output-file option only with paths the user intends the skill to write.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [ClawHub skill page](https://clawhub.ai/matthew77/skills/liang-tavily-research)
- [Publisher profile](https://clawhub.ai/user/matthew77)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Markdown research report by default, raw JSON when requested, or a saved Markdown file when an output path is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes AI-generated synthesis, source titles and URLs, relevance scores when available, query metadata, and response time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
