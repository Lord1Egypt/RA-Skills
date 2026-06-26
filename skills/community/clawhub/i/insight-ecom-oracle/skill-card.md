## Description: <br>
Lingxi E-commerce is an AI assistant for the Prompt Oracle Library that retrieves and presents advanced commercial visual architectures and prompts based on user needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kinseyho](https://clawhub.ai/user/kinseyho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce creators, marketers, and visual-content teams use this skill to search a paid prompt library for up to five commercial visual prompt architectures based on a keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and the skill-specific user ID are sent to an external backend. <br>
Mitigation: Install only if this data sharing is acceptable, and avoid sensitive business details in searches that may trigger the skill. <br>
Risk: Registration, renewal, and activation messaging routes users to an off-platform Afdian payment page. <br>
Mitigation: Verify the payment page, price, and operator identity before paying. <br>
Risk: Broad trigger phrases can activate the skill when a user only intended a general prompt request. <br>
Mitigation: Review the trigger phrases before deployment and invoke the skill with deliberate e-commerce prompt-library keywords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kinseyho/insight-ecom-oracle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [JSON object with Markdown-formatted message strings and prompt-library results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to five deduplicated prompt results and may split long messages into chunks of 3800 characters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact skill.yml lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
