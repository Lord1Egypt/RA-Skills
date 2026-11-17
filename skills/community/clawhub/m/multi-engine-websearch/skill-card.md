## Description:

Multi-engine web search across DuckDuckGo, DDG Lite, Yahoo, Yahoo JP, Startpage, and Google headless Chromium, returning ranked results without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nirveshdagar](https://clawhub.ai/user/nirveshdagar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up current web information, verify facts, research topics, and collect multi-source search results for summarization or citation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to third-party search engines.

Mitigation: Avoid sensitive or confidential queries and restrict engines when a smaller provider set is sufficient.

Risk: The Google mode runs headless Chromium without the browser sandbox.

Mitigation: Prefer the non-Google HTTP engines unless Google is required, do not run the skill as root, and execute it in a constrained environment.

Risk: Install instructions use mutable latest dependency resolution.

Mitigation: Use pinned and reviewed dependency versions for production or managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nirveshdagar/skills/multi-engine-websearch)
- [Publisher Profile](https://clawhub.ai/user/nirveshdagar)
- [Engine Notes & Troubleshooting](references/engines.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON search results or plain-text ranked results, usually summarized by the calling agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include query, total count, per-engine hit counts, titles, URLs, snippets, and engine attribution.]

## Skill Version(s):

2.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
