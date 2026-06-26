## Description: <br>
Integrates with the Lovart.ai API to help agents generate AI designs, images, edited visuals, videos, and template-based creative assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mendynew](https://clawhub.ai/user/mendynew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert design requests into Lovart API workflows for product images, marketing assets, logo concepts, and short videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, design requirements, or brand material to Lovart.ai for processing. <br>
Mitigation: Use a trusted environment and avoid submitting confidential product plans, customer data, secrets, or unreleased brand assets unless third-party processing by Lovart is acceptable. <br>
Risk: Lovart API calls may consume paid credits. <br>
Mitigation: Confirm broad or batch generation requests before execution and monitor API usage against the account plan. <br>
Risk: The skill requires a Lovart API key. <br>
Mitigation: Store LOVART_API_KEY only in trusted environment variables, never expose it in client-side code, and rotate it regularly. <br>


## Reference(s): <br>
- [Lovart Skill on ClawHub](https://clawhub.ai/mendynew/lovart) <br>
- [Lovart.ai](https://www.lovart.ai/) <br>
- [Lovart API Documentation](https://lovart.info/lovart-api) <br>
- [Lovart for Developers](https://lovart.info/lovart-ai-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Lovart API prompts, curl commands, task polling guidance, and result URLs from Lovart responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, config.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
