## Description: <br>
Video Generation and Editing with HappyHorse models. Supports text2video, image2video (first-frame based), reference2video (multi-image character fusion), and video editing capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisyejh](https://clawhub.ai/user/krisyejh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative teams use this skill to submit and check Alibaba DashScope HappyHorse video generation and editing jobs from an agent workflow, including text-to-video, image-to-video, reference-image-to-video, and video-editing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and local images or videos supplied to the helper are sent to Alibaba DashScope for processing. <br>
Mitigation: Use only approved content for that provider, avoid confidential or regulated media unless authorized, and use a limited DashScope API key. <br>
Risk: Generated video URLs and task IDs are temporary but may expose content while valid. <br>
Mitigation: Download needed outputs promptly and avoid sharing task IDs or generated URLs outside the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krisyejh/happyhorse-video-gen-edit) <br>
- [Alibaba ModelStudio model market](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market) <br>
- [HappyHorse text-to-video API documentation](references/happyhorse-t2v-api-doc.md) <br>
- [HappyHorse image-to-video API documentation](references/happyhorse-i2v-api-doc.md) <br>
- [HappyHorse reference-to-video API documentation](references/happyhorse-r2v-api-doc.md) <br>
- [HappyHorse video-edit API documentation](references/happyhorse-videoedit-api-doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and DASHSCOPE_API_KEY. The helper submits asynchronous DashScope jobs and returns task IDs, task status, and temporary generated video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
