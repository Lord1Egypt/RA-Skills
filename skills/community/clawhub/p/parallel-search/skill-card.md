## Description:

AI-powered web search via Parallel API. Returns ranked results with LLM-optimized excerpts. Use for up-to-date research, fact-checking, and domain-scoped searching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Parallel web searches for current research, fact-checking, and domain-scoped lookup tasks, then synthesize cited answers from ranked JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and related task context are sent to Parallel through an authenticated external CLI.

Mitigation: Avoid secrets, credentials, private internal details, and local-only lookup tasks unless external web search is intentional.

Risk: The skill depends on parallel-cli being installed and authenticated before use.

Mitigation: Check parallel-cli availability and authentication first; if either fails, stop and direct the user to Parallel CLI documentation.

Risk: Search results may be incomplete, stale, or conflicting.

Mitigation: Prefer official or primary sources, preserve source URLs and publish dates when available, and surface discrepancies in the final answer.

## Reference(s):

- [Parallel Homepage](https://parallel.ai)
- [Parallel API Docs](https://docs.parallel.ai)
- [Parallel Search API Reference](https://docs.parallel.ai/api-reference/search)
- [Parallel CLI Integration Docs](https://docs.parallel.ai/integrations/cli)
- [ClawHub Skill Page](https://clawhub.ai/normallygaussian/skills/parallel-search)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash examples and JSON search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports result-count, keyword, date, domain include/exclude, and excerpt-size controls through parallel-cli flags.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
