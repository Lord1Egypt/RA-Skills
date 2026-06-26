## Description: <br>
Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnicholasbcarter-code](https://clawhub.ai/user/mrnicholasbcarter-code) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run single or batch web-search queries through OpenRouter and return grounded results with citations when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are shared with OpenRouter and may include sensitive information. <br>
Mitigation: Avoid entering secrets or sensitive private information in queries. <br>
Risk: OpenRouter API usage may affect account usage or billing. <br>
Mitigation: Monitor OpenRouter API usage and billing for the configured API key. <br>
Risk: The release wording may confuse users by referring to both Perplexity and OpenRouter. <br>
Mitigation: Clarify for users that the skill requires OpenRouter credentials and sends requests to OpenRouter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrnicholasbcarter-code/openrouter-perplexity) <br>
- [OpenRouter](https://openrouter.ai/) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown-style search results by default, or raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and accepts one or more query strings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
