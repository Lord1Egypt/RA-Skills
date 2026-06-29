## Description: <br>
Helps agents prepare and submit PoYo Tripo3D text-to-3D, image-to-3D, and multiview-to-3D requests, then report task IDs for polling or webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical creators use this skill to plan, configure, and submit PoYo Tripo3D asset-generation jobs from text prompts, object images, or multiview image sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager and avoid echoing it in generated commands or responses. <br>
Risk: Prompts, source image URLs, generated asset URLs, or callback URLs may reveal confidential project details. <br>
Mitigation: Review payloads before submission and avoid confidential prompts, private asset URLs, sensitive object images, or callback receivers unless PoYo and the receiver are trusted. <br>
Risk: Live submissions can send prepared payloads to PoYo before the user has confirmed intent. <br>
Mitigation: Submit jobs only when the user explicitly asks for a live API call from a trusted shell and the payload has been reviewed. <br>


## Reference(s): <br>
- [PoYo Tripo3D API Reference](references/api.md) <br>
- [PoYo Tripo H3.1 3D Docs](https://docs.poyo.ai/api-manual/3d-series/tripo-h31-3d) <br>
- [PoYo Tripo P1 3D Docs](https://docs.poyo.ai/api-manual/3d-series/tripo-p1-3d) <br>
- [PoYo Tripo H3.1 Model Page](https://poyo.ai/models/tripo-h31-3d) <br>
- [PoYo Tripo P1 Model Page](https://poyo.ai/models/tripo-p1-3d) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/poyo-tripo-3d) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id when a request is submitted; the skill submits jobs and does not directly produce final 3D asset files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
