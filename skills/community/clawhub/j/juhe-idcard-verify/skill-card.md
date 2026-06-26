## Description: <br>
Verifies whether a Chinese resident ID card number and real name match by calling the Juhe ID card verification API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to perform Chinese ID card real-name authentication when a user provides a name and ID number. It supports setup guidance, command-line verification, API invocation, and formatted masked results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real names and Chinese ID numbers are sent to Juhe for verification. <br>
Mitigation: Use only with explicit user consent and disclose that identity data is transmitted to the Juhe API. <br>
Risk: The artifact script uses an HTTP API endpoint for the verification request. <br>
Mitigation: Prefer a version that uses HTTPS before handling production identity data. <br>
Risk: Raw script output may include sensitive verification details in terminal logs or agent transcripts. <br>
Mitigation: Keep formatted displays masked and redact or avoid storing raw responses that contain identity data. <br>


## Reference(s): <br>
- [Juhe ID Card Verification API](https://www.juhe.cn/docs/api/id/103) <br>
- [Juhe Data Platform](https://www.juhe.cn) <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-idcard-verify) <br>
- [Publisher profile](https://clawhub.ai/user/juhemcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-formatted script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_IDCARD_VERIFY_KEY; verification output masks the name and ID number in the formatted display.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
