## Description: <br>
AI video, image generation. 40+ models — Sora, Veo 3, Kling, Seedance, GPT Image, Hailuo, WAN. Text-to-video, image-to-video, text-to-image,image-to-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tate-kt](https://clawhub.ai/user/tate-kt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure Pixwith MCP, select current image or video generation models, submit schema-valid generation jobs, upload reference images when needed, check credits, and poll asynchronous task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pixwith requests require an API key, and exposed keys could allow unauthorized use. <br>
Mitigation: Keep the API key private, verify the Pixwith endpoint before configuration, and replace placeholders with a valid key only in the MCP host configuration. <br>
Risk: High-resolution image jobs and video jobs can consume Pixwith credits. <br>
Mitigation: Check credits before expensive or long-running jobs and stop if the selected request exceeds the available balance. <br>
Risk: Reference image uploads may send user-provided content to Pixwith for processing. <br>
Mitigation: Avoid uploading sensitive images unless the user is comfortable sending them to Pixwith, and prefer the Pixwith upload flow for local or unreliable images. <br>
Risk: Model availability, options, and pricing can change over time. <br>
Mitigation: Call list_models and get_model_schema before generation, then build requests from the current schema instead of relying on static model lists. <br>


## Reference(s): <br>
- [Pixwith Homepage](https://pixwith.ai) <br>
- [Pixwith Service Contract](references/service-contract.md) <br>
- [Current Model Snapshot](references/model-snapshot.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tate-kt/pixwith-ai-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration examples and Pixwith MCP tool-call sequences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Pixwith API key; media generation is asynchronous and returns task results after polling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
