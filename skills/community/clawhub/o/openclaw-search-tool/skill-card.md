## Description: <br>
Search the web using LLMs via OpenRouter. Use for current web data, API docs, market research, news, fact-checking, or any question that benefits from live internet access and reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronn](https://clawhub.ai/user/aaronn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to run live web research through OpenRouter for current facts, API documentation, market research, news, and citation-heavy answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to OpenRouter and may include sensitive context if the user provides it. <br>
Mitigation: Do not include secrets or private customer/internal data in research prompts. <br>
Risk: Long-running web research can increase runtime and API cost. <br>
Mitigation: Use an OpenRouter key with spending limits and monitor long-running sub-agent or exec sessions. <br>
Risk: Live web research may return incomplete, outdated, or misleading source material. <br>
Mitigation: Review cited sources and validate important claims before relying on the answer. <br>


## Reference(s): <br>
- [OpenClaw Research Tool homepage](https://github.com/aaronn/openclaw-search-tool) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with citations and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the research-tool binary and OPENROUTER_API_KEY; stdout contains the response while stderr may contain progress, reasoning traces, and token usage.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
