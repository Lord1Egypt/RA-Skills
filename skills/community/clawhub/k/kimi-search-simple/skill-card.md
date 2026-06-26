## Description: <br>
通过 Kimi API 的 builtin_function $web_search 联网检索，用于新闻、实时信息、股价、公司动态等时效性内容，并支持中英检索与总结或原始结果输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Kimi/Moonshot web searches for timely information, choosing either a synthesized answer or raw search-result style entries when the user asks for sources, links, or excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Moonshot/Kimi API key and sends user search queries to Moonshot. <br>
Mitigation: Store the API key in supported environment variables or credential files, avoid exposing it in logs or screenshots, and rotate it if leakage is suspected. <br>


## Reference(s): <br>
- [Moonshot Open Platform](https://platform.moonshot.cn/) <br>
- [Moonshot API Models Endpoint](https://api.moonshot.cn/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown or plain text with optional command-line and Python usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return either a synthesized search summary or raw result entries; default model is kimi-k2-turbo-preview with max_tokens set to 8192.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
