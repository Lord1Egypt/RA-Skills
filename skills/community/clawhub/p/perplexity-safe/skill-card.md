## Description: <br>
Provides a bash-based Perplexity API client for web-grounded AI search with source citations and hardened handling of user input and API secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haru3613](https://clawhub.ai/user/haru3613) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query Perplexity for current, web-grounded answers with citations when built-in knowledge is insufficient or the user asks for Perplexity-backed research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and custom system prompts are sent to Perplexity. <br>
Mitigation: Avoid confidential or proprietary prompts and use a dedicated Perplexity API key for this skill. <br>
Risk: Perplexity API use is billable. <br>
Mitigation: Monitor API usage and prefer lower-cost models for routine queries. <br>
Risk: Server security guidance notes an unused GitHub WebFetch permission. <br>
Mitigation: Review the permission before installation and remove or question it if it is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/haru3613/perplexity-safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Plain text, Markdown, or pretty-printed JSON with optional source citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Perplexity API key; query length is capped at 8000 characters and max tokens are capped at 4096.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact/package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
