## Description: <br>
Generate images via NewAPI Banana API (nano-banana, Gemini). Supports text-to-image and image-to-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loobayn](https://clawhub.ai/user/loobayn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this OpenClaw skill to generate new images from prompts and edit images from reference files through NewAPI Banana models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys for a third-party image-generation service. <br>
Mitigation: Use a limited, rotatable API key stored in local configuration or NEWAPI_API_KEY, and avoid pasting long-lived credentials into chat. <br>
Risk: The default service endpoint uses HTTP, which may expose prompts, images, or credentials on the network. <br>
Mitigation: Install only if the publisher and service are trusted, review the configured endpoint before use, and monitor account usage. <br>


## Reference(s): <br>
- [API Key Setup Guide](references/api-key-setup.md) <br>
- [Image Generation Guide](references/image-generation.md) <br>
- [Output Delivery Guide](references/output-delivery.md) <br>
- [ClawHub skill page](https://clawhub.ai/loobayn/newapi-banana) <br>
- [Publisher profile](https://clawhub.ai/user/loobayn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files delivered through the agent message tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is written under /tmp/openclaw/newapi-output/ and may include cost reporting when the API returns COST output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
