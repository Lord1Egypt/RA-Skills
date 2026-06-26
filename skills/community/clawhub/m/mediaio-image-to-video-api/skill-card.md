## Description: <br>
Animate static images into dynamic AI-generated videos with realistic motion using Media.io OpenAPI and an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation teams use this skill to route agent requests to Media.io APIs for checking credits, submitting image-to-video generation jobs, and retrieving task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media.io API credentials are required for use. <br>
Mitigation: Store the API key in the agent runtime secret mechanism and avoid exposing it in prompts, logs, or generated examples. <br>
Risk: Image-to-video generation requests may consume Media.io credits and produce externally hosted synthetic media outputs. <br>
Mitigation: Confirm generation parameters before submitting jobs and review returned results before publishing or downstream reuse. <br>


## Reference(s): <br>
- [Media.io OpenAPI Documentation](https://platform.media.io/docs/) <br>
- [Bundled Media.io API Definitions](artifact/scripts/c_api_doc_detail.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON API responses and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key supplied through API_KEY or an explicit api_key parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
