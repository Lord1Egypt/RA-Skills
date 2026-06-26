## Description: <br>
OpenClaw ComfyUI helps agents control a ComfyUI API endpoint with workflow templates, prompt injection, image upload, result polling, and local output download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SalmonRK](https://clawhub.ai/user/SalmonRK) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run ComfyUI text-to-image and image-editing workflows through concise template IDs instead of sending full workflow JSON. It is suited for agents that need to upload local media, submit prompts to a configured ComfyUI host, and return generated file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A hostile or compromised ComfyUI server could influence where downloaded files are written locally. <br>
Mitigation: Use only trusted ComfyUI endpoints and add filename sanitization before writing downloaded outputs. <br>
Risk: Input media is uploaded to the configured ComfyUI host. <br>
Mitigation: Avoid sensitive input media unless transfer to that host is intended. <br>
Risk: The ComfyUI job polling loop has no timeout. <br>
Mitigation: Run against trusted hosts and add a polling timeout for unattended use. <br>


## Reference(s): <br>
- [OpenClaw ComfyUI ClawHub page](https://clawhub.ai/SalmonRK/openclaw-comfyui) <br>
- [Artifact README](artifact/README.md) <br>
- [Agent instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status from the ComfyUI client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media files are downloaded to outputs/comfy/ and returned as local file paths.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.release.version and artifact/manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
