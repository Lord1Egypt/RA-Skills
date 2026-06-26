## Description: <br>
A Chinese-language Liuyao divination skill that opens a classical ink-style local webpage where users cast six lines and receive offline or optional LLM-assisted interpretations from Xueer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clara-Wang-2023](https://clawhub.ai/user/Clara-Wang-2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users interested in Liuyao or I Ching divination use the local page to enter a question, cast six lines, and receive a basic offline reading or an optional streamed LLM interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions, cast details, and API keys can be sent to the configured LLM endpoint. <br>
Mitigation: Use only trusted provider URLs, prefer revocable or limited API keys, and avoid entering sensitive medical, financial, legal, or deeply personal details unless that provider processing is acceptable. <br>
Risk: The skill provides divination-style interpretations that may be mistaken for professional advice. <br>
Mitigation: Treat readings as entertainment or personal reflection and seek qualified professional guidance for consequential medical, financial, legal, or safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Clara-Wang-2023/liuyao-xueer) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Markdown guidance and browser-rendered plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional API key, provider endpoint, and model settings; basic offline interpretation is available when no API key is supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
