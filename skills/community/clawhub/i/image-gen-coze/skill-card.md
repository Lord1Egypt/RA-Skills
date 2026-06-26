## Description: <br>
Generates images through a configured Coze workflow from a single prompt, parses the returned image URL, and documents how an agent can save the generated image locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images with a Coze workflow, including prompt submission, result parsing, and optional local image saving. It is suitable for workflows that need one prompt to produce an image URL or saved PNG output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a configured Coze workflow through a dependency skill using an API key and base URL. <br>
Mitigation: Confirm the workflow_id, base_url, API key, and coze-workflow dependency are trusted and intended before running. <br>
Risk: Prompts may be sent to Coze and generated images may be saved in a local generated_images folder. <br>
Mitigation: Avoid sensitive prompts, inspect generated outputs before sharing, and manage retained image files according to local policy. <br>
Risk: The artifact documents a 30-second-per-request limit. <br>
Mitigation: Add call interval checks or queueing before repeated generation requests. <br>


## Reference(s): <br>
- [Coze Homepage](https://www.coze.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/noah-1106/image-gen-coze) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and bash examples; runtime output is an image URL and optional PNG file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one prompt per request, depends on coze-workflow v1.1.1+, and may save images under ./generated_images.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
