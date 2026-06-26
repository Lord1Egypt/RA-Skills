## Description: <br>
Deep search via Perplexity API with search, reasoning, and research modes for AI-grounded answers with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to run Perplexity-powered web searches, comparative reasoning queries, and deeper research reports from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts are sent to Perplexity using the configured API key. <br>
Mitigation: Use only prompts appropriate for Perplexity processing and use a dedicated API key where possible. <br>
Risk: A file-based API key fallback can expose credentials if the key file is too broadly readable. <br>
Mitigation: Keep ~/.config/perplexity/api_key permission-restricted, such as mode 600. <br>
Risk: Research mode can incur higher API costs than quick search or reasoning modes. <br>
Mitigation: Reserve research mode for queries that need exhaustive analysis and use lower-cost modes for routine searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericsantos/perplexity-deep-search) <br>
- [Perplexity API documentation](https://docs.perplexity.ai) <br>
- [Perplexity chat completions API endpoint](https://api.perplexity.ai/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, citations, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or Markdown answers with optional JSON output and source URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Perplexity API key supplied by PERPLEXITY_API_KEY or a permission-restricted key file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
