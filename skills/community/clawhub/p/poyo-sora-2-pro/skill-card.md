## Description: <br>
Helps agents prepare, submit, and track PoYo Sora 2 Pro video generation jobs for 15- or 25-second clips, storyboard control, style presets, and image-to-video inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create PoYo Sora 2 Pro request payloads, submit authenticated video generation tasks, capture task IDs, and guide follow-up polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, generation parameters, and callback URLs may be sent to PoYo when using POYO_API_KEY. <br>
Mitigation: Avoid submitting secrets, regulated personal data, or internal-only callback URLs unless that data is intended to be shared with PoYo. <br>


## Reference(s): <br>
- [PoYo Sora 2 Pro API Reference](references/api.md) <br>
- [PoYo Sora 2 Pro Docs](https://docs.poyo.ai/api-manual/video-series/sora-2-pro) <br>
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Sora 2 Pro OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/sora-2-pro.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON payloads, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model ID, payload summary, reference image status, returned task ID, and next step for polling or webhook handling; live submission requires POYO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
