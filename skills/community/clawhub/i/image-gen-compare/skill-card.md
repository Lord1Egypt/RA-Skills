## Description: <br>
Side-by-side comparison of paid vs local image generation models, including DALL-E 3, FLUX.1-schnell, Gemini Imagen, and others, that generates images from the same prompt, logs metadata, and stores run history for model evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and technical evaluators use this skill to compare cloud and local image-generation models on the same prompt, including output quality, generation time, cost, and saved run history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local secret-manager credentials to retrieve an OpenAI API key. <br>
Mitigation: Set OPENAI_API_KEY explicitly when possible and review any 1Password service-token access before running. <br>
Risk: Prompts and generated images may be sent to third-party cloud services or saved into a cloud-synced Proton Drive path when that path exists. <br>
Mitigation: Use non-sensitive prompts unless third-party processing is acceptable, and check the output directory before generating images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/image-gen-compare) <br>
- [OpenAI Images API endpoint used by the skill](https://api.openai.com/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [PNG image files, JSON run history, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and image model dependencies; cloud generation uses OPENAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
