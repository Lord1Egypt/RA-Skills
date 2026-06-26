## Description: <br>
Google AI Mode Search calls the LinkFox gateway to retrieve Google AI Overview or AI Mode results for a single search query and returns the captured answer as Markdown with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request live Google AI Overview style summaries for research, technical questions, product sourcing, market preference checks, and web-wide topic summaries. Follow-up questions are handled by summarizing prior context into a new single query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, summarized follow-up context, and feedback text may be sent to LinkFox and Google-related services. <br>
Mitigation: Do not include secrets, credentials, personal data, regulated data, confidential business plans, or sensitive prior conversation context unless the user explicitly approves that disclosure. <br>
Risk: Live AI Overview output can vary by query phrasing and may be absent for some keywords. <br>
Mitigation: Preserve source links, tell the user when no AI Overview is returned, and rephrase or narrow the query when appropriate. <br>


## Reference(s): <br>
- [Google AI Search API reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-google-aimode-search) <br>
- [LinkFox Google AI Mode gateway endpoint](https://tool-gateway.linkfox.com/aiMode/googleSearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown answer text with inline source links plus JSON response metadata from the gateway] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-query requests only; empty results can occur when Google AI Overview does not trigger for the keyword.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
