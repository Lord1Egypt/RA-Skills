## Description: <br>
iaskaster helps agents run Bazi fortune-telling workflows by logging in to the iaskaster service, submitting birth details, and returning or downloading PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjlzw](https://clawhub.ai/user/tjlzw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a user explicitly asks for fortune-telling, Bazi analysis, fate readings, horoscope charts, report downloads, balance checks, or report interpretation through the iaskaster service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles phone or email login plus detailed birth information and may retain local token, session, PDF, or screenshot files. <br>
Mitigation: Use only with trusted accounts and user consent, and remove .iaskaster-token, .iaskaster-uid, .iaskaster-session, downloaded PDFs, and generated screenshots when they are no longer needed. <br>
Risk: The skill can read local report files and could be invoked with unintended paths. <br>
Mitigation: Restrict report-reading requests to expected downloaded iaskaster PDF files and review any requested file path before execution. <br>
Risk: The skill exposes recharge and payment links that users could treat as authoritative. <br>
Mitigation: Independently verify the recharge destination and amount before completing any payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tjlzw/iaskaster) <br>
- [iaskaster API service endpoint](https://iaskmaster.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown-style terminal output, with PDF files or links when reports are downloaded or shown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and phone or email verification login; may store local session, token, PDF, and screenshot artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
