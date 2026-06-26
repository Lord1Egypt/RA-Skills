## Description: <br>
Search Google and get AI Overviews using Pangolin APIs for AI answers, search engine results, multi-turn AI search conversations, and optional search screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyu020923](https://clawhub.ai/user/liuyu020923) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Pangolin-backed Google AI Mode or SERP searches, summarize results, retrieve source URLs, and optionally capture result-page screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, follow-up prompts, and optional screenshot requests are sent to Pangolin. <br>
Mitigation: Avoid confidential or regulated queries and use the skill only when Pangolin receiving the search content is acceptable. <br>
Risk: The skill can cache a Pangolin API key on disk for future use. <br>
Mitigation: Prefer API keys over passwords, protect the cache file, and delete or rotate ~/.pangolin_api_key when access should no longer persist. <br>


## Reference(s): <br>
- [Pangolin account and dashboard](https://www.pangolinfo.com) <br>
- [AI Mode API Reference](references/ai-mode-api.md) <br>
- [AI Overview SERP API Reference](references/ai-overview-serp-api.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Error Codes](references/error-codes.md) <br>
- [ClawHub release page](https://clawhub.ai/liuyu020923/pangolin-ai-serp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance derived from structured JSON search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI overview text, source URLs, organic results, error guidance, and screenshot URLs when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
