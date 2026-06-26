## Description: <br>
Extracts text and layout from images and PDFs using the LLMWhisperer API, including handwriting and complex forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to extract layout-preserving text from selected PDFs and images through LLMWhisperer, especially for handwriting, invoices, forms, and other complex documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or images are sent to LLMWhisperer/Unstract for processing. <br>
Mitigation: Use only with documents approved for that provider and avoid confidential or regulated content unless policy permits it. <br>
Risk: The skill requires an LLMWHISPERER_API_KEY. <br>
Mitigation: Keep the API key private and store it only in the expected environment or local configuration file. <br>
Risk: The evidence notes that the referenced script path is not present as a separate packaged file. <br>
Mitigation: Confirm the installed runtime exposes the expected llmwhisperer command before relying on the skill in workflows. <br>


## Reference(s): <br>
- [LLMWhisperer](https://unstract.com/llmwhisperer/) <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/llmwhisperer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text returned from a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LLMWHISPERER_API_KEY and sends the selected input file to LLMWhisperer/Unstract for processing.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
