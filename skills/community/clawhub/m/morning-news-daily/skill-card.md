## Description:

Daily morning news digest covering tech and finance that gathers current global coverage, curates top items with one-line summaries, and includes original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request concise daily technology, AI, and finance news digests with categorized summaries and source links. It supports focused requests such as AI and semiconductor news, finance-only digests, or company-specific filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on current public web search, so news and finance summaries can be stale, incomplete, or inaccurate.

Mitigation: Verify important finance or market-moving claims against the linked original sources before relying on them.

Risk: Weekend merge behavior depends on retaining prior weekend items, but the evidence describes that behavior conceptually rather than as implemented persistence.

Mitigation: Treat weekend merging as workflow guidance unless the host agent provides suitable caching or memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/morning-news-daily)
- [ClawHub metadata homepage](https://clawhub.ai/BusTes01/morning-news-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news digest with categorized one-line summaries and original source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current web search or similar network access; standard weekday output targets about 20 items, while Monday merged editions target about 25 to 30 items.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
