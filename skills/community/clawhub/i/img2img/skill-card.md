## Description: <br>
Generate images from text descriptions using DALL-E 3 while following usage-policy limits and avoiding realistic human faces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Binkosun](https://clawhub.ai/user/Binkosun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short text prompts into generated image URLs through DALL-E 3. It is suited for agent workflows that need image generation responses from user-provided descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JavaScript helper handles API keys less safely than necessary. <br>
Mitigation: Use a dedicated OpenAI API key, avoid sensitive prompts, and review API-key handling before installation. <br>
Risk: The JavaScript helper disables TLS certificate verification while allowing custom API endpoints. <br>
Mitigation: Fix or avoid the JavaScript helper until TLS verification is restored and custom endpoint use is clearly controlled. <br>


## Reference(s): <br>
- [ClawHub Img2img Release Page](https://clawhub.ai/Binkosun/img2img) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and generated image URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user prompts as image-generation input and returns a single 1024x1024 DALL-E 3 image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
