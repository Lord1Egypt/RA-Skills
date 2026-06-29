## Description: <br>
AI图像创作(AI付版) - 聚合数据 generates images from text prompts through Juhe's paid AI image service and an Alipay payment flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create paid AI-generated images from prompts, with user confirmation before sending prompt text to Juhe and completing payment through Alipay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent in plaintext to Juhe for generation. <br>
Mitigation: Avoid personal, sensitive, confidential, or regulated information in prompts before continuing. <br>
Risk: The workflow uses a paid Alipay payment flow before results are returned. <br>
Mitigation: Confirm the payment amount, order details, and user consent before invoking payment. <br>
Risk: Generated images may be unlawful, infringing, or inappropriate for a user's jurisdiction or use case. <br>
Mitigation: Review requested content and generated outputs against applicable law, platform rules, and organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-ai-image-generate-a2a) <br>
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user consent for paid generation; prompt text is sent to Juhe and payment handling is delegated to alipay-payment-skill.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
