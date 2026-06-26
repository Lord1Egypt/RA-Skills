## Description: <br>
Fetch webpage content as clean Markdown with Jina AI Reader, or search the web with Jina AI Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudy-my-laudy](https://clawhub.ai/user/claudy-my-laudy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to inspect URLs, extract article or documentation content, summarize links, and retrieve web search results in LLM-friendly formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, search queries, and any configured JINA_API_KEY may be sent to Jina AI as part of normal operation. <br>
Mitigation: Avoid confidential internal links, signed URLs, secrets, and sensitive personal data; use a dedicated JINA_API_KEY when needed and unset it when authenticated requests are not intended. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/claudy-my-laudy/jina-ai-skill) <br>
- [Jina AI API dashboard](https://jina.ai/api-dashboard) <br>
- [Jina Reader endpoint](https://r.jina.ai/) <br>
- [Jina Search endpoint](https://s.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON, with shell commands when using the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can omit images to reduce output size; uses JINA_API_KEY when present for authenticated Jina requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
