## Description: <br>
Daily AI image generation from Wikipedia On This Day events using local ComfyUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asimons81](https://clawhub.ai/user/asimons81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure and run a local Windows/WSL ComfyUI workflow that turns daily Wikipedia On This Day events into historical image prompts and generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ComfyUI may be exposed or accessed over the local network. <br>
Mitigation: Bind or firewall ComfyUI, verify the configured host and port, and avoid exposing the API to the internet. <br>
Risk: The workflow contacts Wikipedia and may be configured to post generated output to Discord. <br>
Mitigation: Review the destination channel, bot permissions, and scheduled posting settings before enabling automation. <br>
Risk: Prompt, event, and image history may be retained on local storage. <br>
Mitigation: Review the configured memory and output paths and apply appropriate cleanup or retention controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asimons81/on-this-day-art) <br>
- [ComfyUI setup guide](references/SETUP.md) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>
- [StabilityMatrix](https://lynxhou.io/StabilityMatrix) <br>
- [Wikipedia On This Day API](https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{date}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May queue local ComfyUI image jobs and reference generated image files when the provided scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
