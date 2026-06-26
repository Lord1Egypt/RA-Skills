## Description: <br>
Call a local ComfyUI instance for text-to-image, image-to-image/edit, and image-to-video generation using Z-Image, SD3.5 Medium, Qwen Image Edit, and Wan2.2 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to send prompts and source images to a configured ComfyUI server for image generation, image editing, and short image-to-video generation. The skill returns generated media to the requesting session and reports configuration, model, node, timeout, or endpoint errors when generation cannot complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded source images, and generated media are sent to the configured ComfyUI server. <br>
Mitigation: Use only a ComfyUI endpoint that the deployer controls or trusts, and avoid sending private or regulated content to untrusted endpoints. <br>
Risk: Generated outputs are saved locally and may also remain in ComfyUI output storage. <br>
Mitigation: Review COMFYUI_OUTPUT_DIR and ComfyUI output retention, then remove generated media that may contain private content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunshinejnjn/image-with-comfyui) <br>
- [Publisher profile](https://clawhub.ai/user/sunshinejnjn) <br>
- [README](artifact/README.md) <br>
- [ComfyUI Impact Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack) <br>
- [ComfyUI WAS Nodes](https://github.com/WASasquatch/ComfyUI-WAS-Nodes) <br>
- [ComfyUI Manager](https://github.com/comfyanonymous/ComfyUI-Manager) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated image or video files delivered as media attachments, with concise text status or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable ComfyUI endpoint and local or remote ComfyUI workflows, models, and custom nodes configured outside the skill.] <br>

## Skill Version(s): <br>
1.4.9 (source: release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
