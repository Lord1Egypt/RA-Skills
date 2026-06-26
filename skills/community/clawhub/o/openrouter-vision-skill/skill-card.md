## Description: <br>
OpenRouter Vision Agent helps an agent analyze images through OpenRouter's vision API using x-ai/grok-4.1-fast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gawainchin](https://clawhub.ai/user/gawainchin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to describe, explain, and interpret publicly accessible images through OpenRouter when visual analysis is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, image URLs, and prompts are sent to OpenRouter as part of the skill's stated function. <br>
Mitigation: Use only when sending the selected image content to OpenRouter is acceptable; avoid private, regulated, or sensitive images unless that provider use has been approved. <br>
Risk: The skill requires an OpenRouter API key. <br>
Mitigation: Keep OPENROUTER_API_KEY in the environment or another secret store and do not write the key into files or prompts. <br>


## Reference(s): <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>
- [ClawHub Skill Page](https://clawhub.ai/gawainchin/openrouter-vision-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and OpenRouter response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENROUTER_API_KEY and returns model-generated image analysis from choices[0].message.content; documented max_tokens range is 500-2000.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
