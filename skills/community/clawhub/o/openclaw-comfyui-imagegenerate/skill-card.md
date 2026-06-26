## Description: <br>
Generates images through a local ComfyUI service and sends the generated image and prompt text to a Feishu chat, with no success reply after delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y93442100-beep](https://clawhub.ai/user/y93442100-beep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to generate images from prompts with a local ComfyUI instance and deliver those images into Feishu chats. It is most useful where image generation and chat delivery should be handled as one agent action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images and prompt text may be sent to Feishu without a success confirmation. <br>
Mitigation: Install only where silent Feishu posting is expected and restrict bot permissions to intended chats. <br>
Risk: The skill runs a helper script from a hard-coded local path that may not match the reviewed package. <br>
Mitigation: Verify the configured helper directory points to the reviewed draw.py before deployment. <br>
Risk: Generated images or prompts may remain in the output_images directory. <br>
Mitigation: Monitor or clean the output directory when prompts or generated images may be sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/y93442100-beep/openclaw-comfyui-imagegenerate) <br>
- [README.md](artifact/README.md) <br>
- [skill.md](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Text] <br>
**Output Format:** [PNG image files, Feishu message delivery, and text errors; successful Feishu delivery is silent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prompt text as the primary input, writes generated images under output_images, and depends on a local ComfyUI service plus Feishu bot permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
