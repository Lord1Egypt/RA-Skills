## Description: <br>
Meshy 6 3D asset generation on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit for text-to-3D, image-to-3D, multi-image-to-3D, polling, and webhook workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare PoYo Meshy 6 3D generation requests, select the appropriate text, image, or multi-image workflow, submit prepared payloads, and track async task follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, callback URLs, and generated asset metadata may be sent to PoYo during live submissions. <br>
Mitigation: Use the skill only for intended PoYo Meshy 6 workflows, avoid sending sensitive inputs, and review payloads before submission. <br>
Risk: POYO_API_KEY is required for API calls and could be exposed if handled in logs, browser code, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a secret manager and avoid logging credentials or private request data. <br>
Risk: The helper can create live PoYo generation jobs when explicitly invoked. <br>
Mitigation: Allow live submissions only after the user requests them and the agent is running in a trusted shell with a prepared payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-meshy-6-3d) <br>
- [PoYo Meshy 6 3D API documentation](https://docs.poyo.ai/api-manual/3d-series/meshy-6-3d) <br>
- [PoYo Meshy 6 3D model page](https://poyo.ai/models/meshy-6-3d) <br>
- [Local API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model id, request type, payload summary, source-image status, returned task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
