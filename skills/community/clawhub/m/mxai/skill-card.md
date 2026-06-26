## Description: <br>
Mxai helps an agent use the mxai REST API to generate images and videos, including MJ-style image workflows, from user prompts and supplied image inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure mxai API access, submit image or video generation requests, poll task status, view generated media links, and check account or task information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, pasted or base64 images, image URLs, and generated media requests are sent to the mxai service. <br>
Mitigation: Avoid sensitive or private content unless the user trusts mxai to process it. <br>
Risk: The skill requires a sensitive API key and supports query-string authentication. <br>
Mitigation: Prefer Authorization-header authentication and mask MX_AI_API_KEY or nb_ tokens in all logs and responses. <br>
Risk: Generation requests may consume user credits. <br>
Mitigation: Confirm the requested generation intent and required inputs before submitting image, video, or MJ tasks. <br>
Risk: Failure output may expose prompts, image references, response headers, or service metadata. <br>
Mitigation: Keep detailed error logs masked and avoid sharing logs containing private prompts or image references. <br>


## Reference(s): <br>
- [ClawHub Mxai Skill Page](https://clawhub.ai/tianheihei002/mxai) <br>
- [mxai API Key Setup](https://www.mxai.cn/home/#/mcp) <br>
- [mxai REST API Base](https://mcp.mxai.cn) <br>
- [mxai Skill Version Endpoint](https://mcp.mxai.cn/mcp/skill/version) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown responses with REST API request guidance, JSON response handling, generated media links, and masked error logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_AI_API_KEY; image and video tasks are polled until completion or failure; generated media may consume service credits.] <br>

## Skill Version(s): <br>
1.4.3 (source: SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
