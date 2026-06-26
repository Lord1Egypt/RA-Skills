## Description: <br>
Generate videos from text descriptions using AI models through OATDA's unified API, submitting asynchronous requests and polling for completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative teams use this skill to submit text-to-video and image-to-video generation requests to OATDA, select supported providers and models, and poll returned task IDs until video generation completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, model parameters, and public reference image URLs are sent to OATDA and may be shared with downstream model providers. <br>
Mitigation: Avoid confidential prompts and private or signed media URLs; install only if this data sharing is acceptable. <br>
Risk: The skill may read an API key from ~/.oatda/credentials.json when OATDA_API_KEY is not set. <br>
Mitigation: Set OATDA_API_KEY directly when file-based credential access is not desired, and never print the full API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devcsde/oatda-generate-video) <br>
- [OATDA homepage](https://oatda.com) <br>
- [OATDA video models endpoint](https://oatda.com/api/v1/llm/models?type=video) <br>
- [OATDA async video generation endpoint](https://oatda.com/api/v1/llm/generate-video?async=true) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, OATDA_API_KEY, and optionally ~/.oatda/credentials.json.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
