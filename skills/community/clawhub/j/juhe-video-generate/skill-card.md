## Description: <br>
Creates AI-generated videos from text prompts or source images through Juhe, with options for resolution, duration, aspect ratio, polling, and local MP4 download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit text-to-video or image-to-video jobs, estimate quota cost, wait for completion, and retrieve generated MP4 videos. It is suited for short-form creative video generation where prompts, media inputs, and API quota usage can be shared with Juhe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, base64 images, and audio URLs are sent to Juhe for video generation. <br>
Mitigation: Avoid private photos, internal links, signed URLs, confidential prompts, and sensitive audio unless sharing them with Juhe is acceptable. <br>
Risk: Video generation can consume Juhe API quota based on resolution and duration. <br>
Mitigation: Confirm resolution, duration, and estimated quota cost before submitting a generation job. <br>
Risk: The Juhe API key could be exposed if passed directly in shell history or shared logs. <br>
Mitigation: Prefer the JUHE_VIDEO_KEY environment variable or a local .env file and avoid placing keys in commands that may be logged. <br>
Risk: Generated video links are temporary and downloaded files are written to a local output directory. <br>
Mitigation: Confirm the output directory and save required videos promptly before temporary links expire. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-video-generate) <br>
- [Juhe AI Video Creation API documentation](https://www.juhe.cn/docs/api/id/827) <br>
- [Juhe platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_VIDEO_KEY; may return a temporary online video link and optionally save an MP4 locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
