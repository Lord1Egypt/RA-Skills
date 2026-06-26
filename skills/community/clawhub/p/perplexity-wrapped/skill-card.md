## Description: <br>
Search the web with AI-powered answers via Perplexity API, including ranked Search API results, Sonar answers with citations, and Agentic Research responses with tools, with default untrusted-content wrapping for agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VACInc](https://clawhub.ai/user/VACInc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web search results, grounded answers with citations, or deeper agentic research through Perplexity. It is suited for web-grounded research workflows where external results should be treated as untrusted data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and optional agentic instructions are sent to Perplexity, and agentic mode may use third-party model providers. <br>
Mitigation: Use a dedicated API key, avoid secrets or confidential data in queries, and review provider suitability before use. <br>
Risk: Web results and generated answers can contain misleading content or prompt-injection attempts. <br>
Mitigation: Prefer the default wrapped output and treat returned content as data rather than instructions. <br>
Risk: Deep research and agentic modes can increase API spend. <br>
Mitigation: Monitor Perplexity usage and keep the explicit confirmation gate for high-cost deep research operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/VACInc/perplexity-wrapped) <br>
- [Perplexity API documentation](https://docs.perplexity.ai) <br>
- [Perplexity Search API quickstart](https://docs.perplexity.ai/docs/search/quickstart) <br>
- [Perplexity Sonar API quickstart](https://docs.perplexity.ai/docs/sonar/quickstart) <br>
- [Perplexity Agentic Research API quickstart](https://docs.perplexity.ai/docs/agentic-research/quickstart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Wrapped Markdown text with citations by default; optional raw JSON for debugging.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is bounded as external untrusted content; raw JSON requires explicit --json opt-in.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
