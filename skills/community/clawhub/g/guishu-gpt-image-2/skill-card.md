## Description: <br>
Generate images with Guishu Token gpt-image-2 through an OpenAI-compatible images endpoint and save local outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quqi1599](https://clawhub.ai/user/quqi1599) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create Guishu gpt-image-2 images from prompts, test prompt-to-image workflows, and produce local galleries of generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and bearer tokens are sent to the configured image-generation endpoint. <br>
Mitigation: Use a dedicated Guishu Token API key, avoid sensitive prompts, and only set a custom endpoint when it is trusted to receive prompts and credentials. <br>
Risk: Generated output folders include request logs that may reveal prompts or workflow details. <br>
Mitigation: Review generated request and prompt JSON files before sharing the output directory or HTML gallery. <br>
Risk: Long-running generation requests can time out while upstream processing may still continue and incur cost. <br>
Mitigation: Avoid automatic retries after long timeouts and ask before resubmitting requests that may have already been processed. <br>


## Reference(s): <br>
- [GPT Image 2 API Notes](references/gpt-image-2-api.md) <br>
- [Guishu Token Images API Endpoint](https://api.llm-token.cn/v1/images/generations) <br>
- [Guishu GPT Image 2 Web UI](https://image2.gpt-agent.cc/) <br>
- [ClawHub Skill Page](https://clawhub.ai/quqi1599/guishu-gpt-image-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated image files, request JSON, prompt JSON, and an HTML gallery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment-based API keys, supports prompt files, dry runs, image size, quality, response format, timeout, endpoint, and output directory options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
