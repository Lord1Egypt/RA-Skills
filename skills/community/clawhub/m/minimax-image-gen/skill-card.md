## Description: <br>
Generates images with the MiniMax Image API, including text-to-image prompts, style presets, aspect ratios, and optional preview output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bluestar-34](https://clawhub.ai/user/Bluestar-34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate PNG images from prompts through MiniMax models, with preset styles for subjects such as portraits, landscapes, products, pets, and cyberpunk scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that TLS certificate verification is disabled, which weakens protection for MiniMax API requests and image downloads. <br>
Mitigation: Review the Python script before installation, enable certificate verification before sensitive use, and install only after the publisher fixes TLS verification. <br>
Risk: The skill sends prompts to the MiniMax API and may load a MiniMax key from OpenClaw config when MINIMAX_API_KEY is unset. <br>
Mitigation: Use a scoped MiniMax API key with limited billing exposure, avoid sensitive prompts, and confirm where the key is loaded from before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bluestar-34/minimax-image-gen) <br>
- [MiniMax Image Generation API documentation](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i) <br>
- [MiniMax API key management](https://platform.minimaxi.com/user-center/interface-key) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MINIMAX_API_KEY; generated files are saved under the configured output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, artifact changelog, and script version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
