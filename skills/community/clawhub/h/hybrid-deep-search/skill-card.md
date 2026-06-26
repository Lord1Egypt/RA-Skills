## Description: <br>
Hybrid Deep Search routes search queries between Brave API for fast lookup and OpenAI Codex for deeper analysis based on query complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scsun1978](https://clawhub.ai/user/scsun1978) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run query-driven web research with automatic routing between quick search and deeper synthesis modes. It is intended for fact lookup, comparison, analysis, and focused research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may include secrets, personal data, internal URLs, or proprietary text that could be sent to external search or model providers. <br>
Mitigation: Do not include sensitive data in queries, and keep API keys in environment variables rather than command text or committed configuration. <br>
Risk: Deep search mode can incur OpenAI usage costs. <br>
Mitigation: Use automatic or quick mode for simple lookups and monitor OpenAI API usage when enabling Codex mode. <br>
Risk: The artifact describes some provider behavior as simulated or requiring real integration, so returned results may not reflect live provider data in all environments. <br>
Mitigation: Verify actual Brave and OpenAI provider integration before relying on the skill for production research results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scsun1978/hybrid-deep-search) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [OpenAI GPT-5-Codex Model Documentation](https://platform.openai.com/docs/models/gpt-5-codex) <br>
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include routing analysis, selected search mode, engine status, error messages, and formatted search or analysis results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
