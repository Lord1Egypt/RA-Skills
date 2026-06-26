## Description: <br>
Lightningprox provides pay-per-use AI gateway access via Bitcoin Lightning across Anthropic, OpenAI, Together.ai, Mistral, and Google Gemini models using L402 protocol or spend token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access multiple AI model providers through LightningProx without separate provider API keys or accounts. It supports prepaid spend-token use and L402 pay-per-request flows for inference, model comparison, vision, and reasoning tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may make paid AI requests through LightningProx when using a spend token or L402 payment flow. <br>
Mitigation: Use a limited-balance spend token and review planned requests before enabling autonomous use. <br>
Risk: Prompts and request data are sent to LightningProx for inference. <br>
Mitigation: Avoid sending secrets or regulated data unless LightningProx has been approved for that data use. <br>
Risk: The optional npm SDK changes project dependencies and handles LightningProx authentication. <br>
Mitigation: Review the SDK separately before adding it to a project. <br>


## Reference(s): <br>
- [LightningProx homepage](https://lightningprox.com) <br>
- [LightningProx ClawHub release](https://clawhub.ai/unixlamadev-spec/lightningprox) <br>
- [Publisher profile](https://clawhub.ai/user/unixlamadev-spec) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples that use LIGHTNINGPROX_SPEND_TOKEN or L402 credentials for paid inference through LightningProx.] <br>

## Skill Version(s): <br>
1.4.1 (source: lightningprox.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
