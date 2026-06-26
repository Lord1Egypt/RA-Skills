## Description: <br>
Reads public news and article pages from mainstream Chinese and English sources, then produces concise Simplified Chinese summaries, comparisons, or news briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaohaojie1](https://clawhub.ai/user/shaohaojie1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to summarize individual news articles, search for recent coverage by keyword, compare multiple articles, or generate quick briefings from public news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad news-summary trigger phrases may activate on underspecified requests. <br>
Mitigation: Use explicit news sources, article URLs, or clear keywords before invoking the workflow. <br>
Risk: Article summaries can be misleading when source pages are unavailable, incomplete, or stale. <br>
Mitigation: Use only fetched public content, include source and time fields when available, and state retrieval failures rather than inventing missing details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaohaojie1/post-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, comparison tables, or briefing lists in Simplified Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source and time fields when available; relies on fetched public web content and should report fetch failures instead of filling gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
