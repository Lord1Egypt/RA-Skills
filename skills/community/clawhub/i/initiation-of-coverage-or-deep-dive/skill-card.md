## Description: <br>
Generates initiation-of-coverage or deep-dive research reports for listed companies in A-share, Hong Kong, U.S., and Beijing Stock Exchange markets using EastMoney data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External financial analysts and agents use this skill to generate full initiation-of-coverage or deep-dive company research reports for supported listed-company markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EastMoney API key. <br>
Mitigation: Install only when the publisher is trusted and provide the key through the required EM_API_KEY environment variable. <br>
Risk: The original report query is sent to EastMoney. <br>
Mitigation: Avoid including confidential or non-public information in report prompts. <br>
Risk: Generated PDF and DOCX report files are saved locally. <br>
Mitigation: Choose an output directory where generated report attachments can be stored safely. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/financial-ai-analyst/initiation-of-coverage-or-deep-dive) <br>
- [EastMoney initial coverage API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/write/initial-coverage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown response with generated report text, local PDF and Word file paths, and a share link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and may save PDF and DOCX report attachments to a local output directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
