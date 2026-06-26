## Description: <br>
Professional AI image enhancement for sharpening blurry images, improving thumbnails, and lossless 2x or 4x upscaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steinvenic](https://clawhub.ai/user/steinvenic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit images to an image-enhancement API, poll for completion, and retrieve upscaled or sharpened results. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads user-selected images and an API key to an external provider. <br>
Mitigation: Avoid sensitive images unless the provider's privacy and retention practices are acceptable, and protect the API key from logs and shared transcripts. <br>
Risk: Polling can continue longer than intended when a task remains pending or processing. <br>
Mitigation: Use a practical polling timeout and surface failed, nsfw, or unfinished statuses clearly to the user. <br>


## Reference(s): <br>
- [Image Upscaler ClawHub release](https://clawhub.ai/steinvenic/image-upscaler) <br>
- [Image Upscaler API homepage](https://supabase.00123.fun:22334) <br>
- [OpenAPI specification](artifact/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, URLs] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task IDs, processing statuses, and processed image URLs; callers should poll with a practical timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
