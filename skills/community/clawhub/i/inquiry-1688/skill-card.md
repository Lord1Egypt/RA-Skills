## Description: <br>
Submits procurement inquiries to 1688 suppliers about pricing, minimum order quantity, customization, logistics, qualifications, specifications, and samples, then retrieves supplier replies after about 20 minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement and sourcing users use this skill to ask 1688 suppliers product-specific questions and receive structured follow-up results. It is suited for cross-border purchasing, wholesale sourcing, OEM customization, and supplier communication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inquiry text, product links, quantities, addresses, supplier replies, and AlphaShop credentials may contain business-sensitive information. <br>
Mitigation: Configure credentials through environment variables, limit inquiry content to necessary details, and treat generated inquiry results as sensitive procurement records. <br>
Risk: The security evidence flags a fixed DingTalk recipient for proactive delivery, which can send procurement details to the wrong recipient if the target is not appropriate. <br>
Mitigation: Install only when DingTalk target 238382 is the intended recipient, or modify the skill to require a configurable or confirmed recipient before use. <br>
Risk: Delayed background follow-up can continue after submission without clear per-user control. <br>
Mitigation: Require user confirmation before each inquiry and review or clear pending inquiry records when a request should no longer be delivered. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1688AiInfra/inquiry-1688) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>
- [AlphaShop API credits](https://www.alphashop.cn/seller-center/home/api-list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AlphaShop access credentials; submitted inquiries may complete asynchronously after about 20 minutes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
