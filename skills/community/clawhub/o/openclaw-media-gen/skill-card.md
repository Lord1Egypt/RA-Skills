## Description: <br>
Generate AI images or videos through AIsa for creative generation, asset drafts, and media workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate image or video assets through AIsa from prompts, creative briefs, or media workflow requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AISA_API_KEY is required and should be treated as a sensitive, billable credential. <br>
Mitigation: Use a scoped key where possible, avoid sharing it in prompts or logs, and review AIsa API usage after first runs. <br>
Risk: Prompts and media generation requests are sent to AIsa. <br>
Mitigation: Install and use the skill only when the user trusts AIsa to process the submitted prompts and media requests. <br>
Risk: The bundled client may overwrite a file at the caller-provided output path. <br>
Mitigation: Choose output paths deliberately and avoid pointing generation output at existing files unless overwriting is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baofeng-tech/openclaw-media-gen) <br>
- [AIsa image generation endpoint](https://api.aisa.one/v1/images/generations) <br>
- [AIsa video generation endpoint](https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis) <br>
- [AIsa video task status endpoint](https://api.aisa.one/apis/v1/services/aigc/tasks/{task_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI emits JSON and can save image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY. Generated media is saved to local output paths selected by the caller.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
