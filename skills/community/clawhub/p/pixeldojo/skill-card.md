## Description: <br>
Access PixelDojo's API helpers for AI image and video generation, live model catalog inspection, async job status checks, and finished asset downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blovett80](https://clawhub.ai/user/blovett80) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to select PixelDojo image or video generation models, submit generation jobs, poll for completion, and download generated media assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input image URLs, and generation requests are sent to PixelDojo under the user's API key. <br>
Mitigation: Use the skill only for intended PixelDojo workflows and avoid submitting secrets, credentials, or sensitive personal content. <br>
Risk: Changing PIXELDOJO_API_BASE can redirect requests to a non-default endpoint. <br>
Mitigation: Keep PIXELDOJO_API_BASE at the default unless the alternate endpoint is trusted. <br>
Risk: Generated media is downloaded to local output paths. <br>
Mitigation: Choose output paths deliberately and review saved files before sharing or reusing them. <br>


## Reference(s): <br>
- [PixelDojo Skill Page](https://clawhub.ai/blovett80/pixeldojo) <br>
- [PixelDojo](https://pixeldojo.ai) <br>
- [PixelDojo API Base](https://pixeldojo.ai/api/v1) <br>
- [PixelDojo Model Catalog](references/model-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated assets are saved as image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PIXELDOJO_API_KEY, may call the PixelDojo API, and saves downloaded media to default or user-selected local output paths.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and api.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
