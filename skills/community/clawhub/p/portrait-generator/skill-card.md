## Description: <br>
Generates hyper-detailed AI portraits through the ComfyDeploy Morfeo Portrait workflow with structured controls for facial features, skin, hair, and expression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to convert natural-language portrait requests into structured facial parameters, queue a ComfyDeploy Morfeo Portrait run, and retrieve the resulting portrait image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portrait prompts, facial traits, run IDs, and output links are sent to ComfyDeploy. <br>
Mitigation: Use only authorized portrait inputs, avoid private likenesses or sensitive identity details unless authorized, and prefer a limited ComfyDeploy API key when available. <br>
Risk: Remote execution requires a ComfyDeploy bearer token. <br>
Mitigation: Keep API keys out of prompts and shared transcripts, and restrict or rotate the key according to the account's available controls. <br>


## Reference(s): <br>
- [Portrait Generator Skill Page](https://clawhub.ai/PauldeLavallaz/portrait-generator) <br>
- [ComfyDeploy Queue Endpoint](https://api.comfydeploy.com/api/run/deployment/queue) <br>
- [ComfyDeploy Run Status Endpoint](https://api.comfydeploy.com/api/run/{run_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with JSON request bodies and API polling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queues a ComfyDeploy run and returns an output image URL after successful polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
