## Description: <br>
AI video and image generation with Pixwith models for text-to-video, image-to-video, text-to-image, and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tate-kt](https://clawhub.ai/user/tate-kt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to Pixwith through MCP, select current image or video models, submit generation tasks, upload reference images when needed, and poll asynchronous results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pixwith API keys are required for every request and could be exposed if copied into shared files or messages. <br>
Mitigation: Store the API key only in local MCP settings, use the documented Api-Key header, and direct users to rotate or replace invalid keys through Pixwith. <br>
Risk: Video and high-resolution image jobs can consume significant credits and take time to complete. <br>
Mitigation: Check credits before expensive jobs, inspect the selected model schema for final credit cost, and do not retry automatically when credits are insufficient. <br>
Risk: User prompts and uploaded reference images are sent to Pixwith for processing. <br>
Mitigation: Avoid uploading sensitive images or prompts unless the user is comfortable sending them to Pixwith, and prefer Pixwith-hosted uploads for local or unreliable image inputs. <br>
Risk: Model availability and options are dynamic, so static model snapshots can become stale. <br>
Mitigation: Call list_models and get_model_schema before generation, and validate image counts, options, and enum values against the current schema. <br>


## Reference(s): <br>
- [Pixwith](https://pixwith.ai) <br>
- [Pixwith Skill Release](https://clawhub.ai/tate-kt/pixwith-ai-video-generation) <br>
- [Pixwith Service Contract](references/service-contract.md) <br>
- [Current Model Snapshot](references/model-snapshot.md) <br>
- [Example: Text to Image](examples/text-to-image.md) <br>
- [Example: Image to Video](examples/image-to-video.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and tool-call payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions, schema-based request guidance, and asynchronous task polling guidance; generated media is returned by the Pixwith service through result URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
