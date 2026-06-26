## Description: <br>
Kling 2.6 Motion Control uses PoYo's API to submit `kling-2.6-motion-control` jobs for motion transfer, character animation, orientation control, and 720p or 1080p output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare or submit PoYo Kling 2.6 Motion Control tasks that animate a character image from a reference motion video. It is suited to workflows that need explicit character orientation and 720p or 1080p output control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, video URLs, and generation metadata are sent to PoYo for processing. <br>
Mitigation: Do not use sensitive, private, or proprietary media unless PoYo's terms and retention practices are acceptable for the intended use. <br>
Risk: The submission script authenticates with POYO_API_KEY and sends a caller-provided JSON payload to the PoYo generation endpoint. <br>
Mitigation: Keep POYO_API_KEY secret, review payloads before submission, and use the returned task_id for controlled follow-up polling or webhook tracking. <br>


## Reference(s): <br>
- [PoYo Kling 2.6 Motion Control API Reference](references/api.md) <br>
- [PoYo Kling 2.6 Motion Control Documentation](https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control) <br>
- [PoYo Kling 2.6 Motion Control OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control.json) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/poyo-kling-2-6-motion-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, final payload or parameter summary, reference-media usage, returned task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
