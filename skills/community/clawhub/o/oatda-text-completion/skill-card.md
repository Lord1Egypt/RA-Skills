## Description: <br>
Generate text using OATDA's unified LLM API across supported providers and model aliases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send text prompts to OATDA, choose a supported provider/model, and return generated text with optional token usage and cost information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, model choices, and usage metadata are sent to OATDA's external API. <br>
Mitigation: Use only with data intended for OATDA; avoid secrets, regulated data, or private content unless that external transmission is acceptable. <br>
Risk: The skill requires an OATDA API key for API calls. <br>
Mitigation: Use a limited or monitored API key where possible, store it in OATDA_API_KEY or the declared credentials file, and never print the full key. <br>


## Reference(s): <br>
- [OATDA](https://oatda.com) <br>
- [OATDA LLM API endpoint](https://oatda.com/api/v1/llm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OATDA_API_KEY or ~/.oatda/credentials.json; responses may include provider, model, token usage, and cost.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
