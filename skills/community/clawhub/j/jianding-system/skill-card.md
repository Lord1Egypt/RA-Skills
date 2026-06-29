## Description: <br>
收藏雅集网在线鉴定 helps users submit antique appraisal orders, obtain WeChat payment QR codes, and check appraisal results across WeChat and non-WeChat environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fozu2024](https://clawhub.ai/user/fozu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assisting agents use this skill to guide antique appraisal requests, prefer the WeChat self-service flow, and use the fallback script only when users cannot complete the flow in WeChat. The fallback flow collects item photos, a phone/SMS login, order details, payment QR code generation, and result lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends item photos, descriptions, phone/SMS login data, and order/payment information to the stated service. <br>
Mitigation: Use the skill only when the user accepts sharing that data, and verify privacy terms directly on the service before submission. <br>
Risk: The fallback script can store a reusable token at ~/.jianding_token and accepts tokens on the command line. <br>
Mitigation: Avoid passing real tokens on the command line when possible, and delete ~/.jianding_token after use. <br>
Risk: The workflow involves paid appraisal orders and service claims that may affect user expectations. <br>
Mitigation: Verify pricing, AI/free-service claims, refund terms, and payment details directly on the service before paying. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fozu2024/jianding-system) <br>
- [Publisher Profile](https://clawhub.ai/user/fozu2024) <br>
- [收藏雅集网 H5 appraisal service](https://jiand.shoucangyaji.com/) <br>
- [Platform Background Reference](references/about.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated QR-code image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fallback script may create local payment QR image files and store a reusable token at ~/.jianding_token.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
