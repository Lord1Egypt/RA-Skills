## Description: <br>
Provides direct access to Metaso search, web page reading, and retrieval-augmented chat capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinmh1338863](https://clawhub.ai/user/xinmh1338863) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to search Metaso, read web page content, and ask RAG-backed questions through a Metaso API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries, chat messages, and requested URLs are sent to Metaso. <br>
Mitigation: Use the skill only when Metaso is approved for the data involved, and avoid sending secrets, private documents, internal URLs, or regulated data. <br>
Risk: The skill requires a Metaso API key that may authorize usage or billing. <br>
Mitigation: Use a dedicated API key, keep it in the METASO_API_KEY environment variable, rotate it when needed, and monitor API usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinmh1338863/metaso-search-v2) <br>
- [Metaso search API endpoint](https://metaso.cn/api/v1/search) <br>
- [Metaso reader API endpoint](https://metaso.cn/api/v1/reader) <br>
- [Metaso chat completions API endpoint](https://metaso.cn/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown returned from Metaso API calls, with setup guidance and JavaScript usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires METASO_API_KEY and sends search queries, chat messages, and requested URLs to Metaso.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
