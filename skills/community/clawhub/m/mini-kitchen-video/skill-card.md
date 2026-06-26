## Description: <br>
生成迷你厨房烹饪短视频，支持从文字描述或公开 HTTPS 图片生成强调微型厨具、真实烹饪细节和治愈感的短视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social video teams use this skill to turn mini-kitchen cooking ideas or public product images into short vertical WeryAI video-generation requests. Agents use it to build prompts, confirm video settings, run the bundled Node.js helper, and return generated video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WERYAI_API_KEY to submit prompts and optional public image URLs to WeryAI. <br>
Mitigation: Install and invoke it only when you trust the publisher and are comfortable sharing the prompt and image URLs with WeryAI. <br>
Risk: Generation requires public HTTPS image URLs for image-to-video workflows; local files are not accepted. <br>
Mitigation: Use only images intended for upload to a public host and avoid sensitive or private visual content. <br>
Risk: WeryAI requests can fail because of unsupported model parameters, rate limits, content safety filtering, insufficient credits, or service errors. <br>
Mitigation: Review the proposed model, duration, aspect ratio, and prompt before execution, then revise parameters or retry according to the returned API error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/mini-kitchen-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video API endpoint](https://api.weryai.com) <br>
- [WeryAI model registry endpoint](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON request parameters, shell commands, and generated video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js 18+, WERYAI_API_KEY, optional public HTTPS image URLs, and WeryAI polling for completion.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
