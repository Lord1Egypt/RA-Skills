## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dtkien182](https://clawhub.ai/user/dtkien182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform live Baidu web searches for current information, documentation, or research topics from an OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu and may expose sensitive content if users submit private data. <br>
Mitigation: Avoid searching for secrets, private documents, credentials, regulated personal data, or other sensitive material. <br>
Risk: The skill requires a Baidu API key that could be misused if exposed. <br>
Mitigation: Store BAIDU_API_KEY in OpenClaw configuration, avoid committing configuration files, restrict local file access where possible, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dtkien182/ken-test) <br>
- [Baidu API key setup guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API key console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends search queries to Baidu AI Search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
