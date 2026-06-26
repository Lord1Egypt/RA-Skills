## Description: <br>
Generate English image prompts for front-view product-holding character images based on user-provided text descriptions and image assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn product descriptions and optional reference images into concise English prompts for front-view character images where the character holds the product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference product photos or character images may contain sensitive or proprietary visual information. <br>
Mitigation: Provide only images and product details that are appropriate for the agent or downstream image tooling to analyze. <br>
Risk: The generated prompt may omit or overstate product, character, pose, or background details if the user's input is incomplete. <br>
Mitigation: Review the final prompt against the source description and reference images before using it for image generation. <br>


## Reference(s): <br>
- [Product Pose Prompt Generator on ClawHub](https://clawhub.ai/openlark/product-pose-prompt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain English image-generation prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only the prompt text in English, with a maximum length of 300 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
