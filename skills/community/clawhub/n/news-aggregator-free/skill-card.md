## Description: <br>
Aggregates domestic and international social, technology, and military news, then filters, deduplicates, and structures results by category with sources, times, and key points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce structured daily or topic-specific news summaries across technology, military, and social categories from multiple sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use network search and possibly command execution to gather news. <br>
Mitigation: Install only when that tool posture is acceptable, and give narrow topics, date ranges, and source constraints. <br>
Risk: Private or sensitive information could be exposed through optional callback URLs or overly broad prompts. <br>
Mitigation: Avoid private data in prompts and use callback URLs only when they are trusted and necessary. <br>
Risk: News search results can be stale, incomplete, duplicated, or inconsistent across sources. <br>
Mitigation: Require source names, timestamps, and links in summaries, and verify important claims against authoritative sources. <br>
Risk: Military news can include restricted, speculative, or conflicting information. <br>
Mitigation: Prefer official or authoritative sources, filter unverified reports, and label uncertainty or conflicting accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-aggregator-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown structured news summaries with titles, links, sources, times, and key points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on network/search availability, source freshness, and user-provided topic or date constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
