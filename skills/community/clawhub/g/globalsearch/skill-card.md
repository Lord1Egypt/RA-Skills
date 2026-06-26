## Description: <br>
Provides multi-source web search through the external clb.ciglobal.cn service, aggregating results from Baidu, Google, Baidu AI, and Elasticsearch-backed sources when broad coverage is requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzsn402](https://clawhub.ai/user/zzsn402) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, gather news, retrieve article references, and run comprehensive multi-source searches when the user requests broad online coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to an external provider and may be associated with the user's API-key account. <br>
Mitigation: Avoid sending passwords, tokens, private identifiers, confidential internal data, or sensitive personal searches unless the provider's privacy and retention practices have been verified. <br>
Risk: The skill requires a sensitive runtime credential, GLOBAL_SEARCH_API_KEY. <br>
Mitigation: Store the API key in an environment variable or credential manager and do not hardcode it in scripts or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzsn402/globalsearch) <br>
- [Provider homepage](https://clb.ciglobal.cn) <br>
- [Global Search API endpoint](https://clb.ciglobal.cn/web_search) <br>
- [API key setup](https://clb.ciglobal.cn/apiKey/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, code snippets, shell commands, and JSON response descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GLOBAL_SEARCH_API_KEY and sends search queries to clb.ciglobal.cn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
