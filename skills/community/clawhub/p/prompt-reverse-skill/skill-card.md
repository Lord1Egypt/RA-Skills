## Description: <br>
Convert image to structured prompts for multiple AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keweizhan](https://clawhub.ai/user/keweizhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt engineers use this skill to turn input images into structured semantic data and model-specific prompts for generative image systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image uploads may expose sensitive, confidential, regulated, or proprietary content to the configured model provider. <br>
Mitigation: Avoid using sensitive images unless the provider, account, and data handling terms are approved for that content. <br>
Risk: The linked implementation may require an OpenAI API key or other sensitive credential. <br>
Mitigation: Use a dedicated key, keep credentials out of public files, and inspect the repository and requirements before running the implementation. <br>
Risk: Generated prompts and structured image descriptions may be incomplete or misleading. <br>
Mitigation: Review generated outputs before using them in production workflows or downstream image generation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON plus plain-text prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image input and may rely on an OpenAI API key when used with the linked implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
