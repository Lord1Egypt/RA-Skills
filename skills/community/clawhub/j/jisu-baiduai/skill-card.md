## Description: <br>
Baidu Intelligent Search sends a user query to Baidu Qianfan's intelligent search generation API and returns a web-grounded model summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send a question to Baidu Qianfan's intelligent search generation API and receive a synthesized answer with search references. It is best suited for Chinese-language search plus summarization workflows that require current web context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search questions and optional advanced request fields are sent to Baidu Qianfan using the user's BAIDU_API_KEY. <br>
Mitigation: Avoid sending secrets, private documents, or sensitive personal data unless Baidu processing is intended, and review raw_body payloads before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-baiduai) <br>
- [Baidu Qianfan intelligent search generation API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Hmbu8m06u) <br>
- [JisuAPI publisher website](https://www.jisuapi.com/) <br>
- [JisuEPC website](https://www.jisuepc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, references, guidance] <br>
**Output Format:** [JSON response containing synthesized answer text, references, usage metadata, or structured error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts an ask command with a JSON request body.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
