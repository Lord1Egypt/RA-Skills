## Description: <br>
Safe ComfyUI image generation. Use saved or ad-hoc server profiles, paste/upload raw workflow JSON, submit, poll, and serve downloaded outputs locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation agents use this skill to connect to a trusted ComfyUI server, submit raw or bundled workflow JSON, poll generation jobs, and collect generated image file paths and view URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved ComfyUI profiles can store reusable API keys or Basic Auth credentials in plaintext. <br>
Mitigation: Prefer environment variables for credentials and avoid saving profiles that contain secrets on shared or unmanaged machines. <br>
Risk: The generated-file viewer can expose local generated media through an unauthenticated network-accessible HTTP server. <br>
Mitigation: Run the viewer only on trusted networks, firewall the port, or modify it to bind to localhost before use. <br>
Risk: Prompts, workflows, and generated outputs are sent to the configured ComfyUI server. <br>
Mitigation: Use only trusted ComfyUI servers and avoid sending sensitive prompts or workflow data. <br>


## Reference(s): <br>
- [ComfyUI Safe Connector - Configuration](references/CONFIG.md) <br>
- [ComfyUI Safe Connector - Endpoints](references/ENDPOINTS.md) <br>
- [ClawHub release page](https://clawhub.ai/genortg/openclaw-comfyui-api-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Files] <br>
**Output Format:** [JSON status objects with generated image file paths and view URLs, plus local files under generated/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses COMFYUI_API_KEY and optional Basic Auth credentials; workflow inputs are parsed as JSON and submitted to a configured ComfyUI server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
