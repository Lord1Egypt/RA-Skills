## Description: <br>
PostQued social media scheduling API integration for uploading content, publishing or drafting posts to TikTok and other platforms, managing platform accounts, and checking publish status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syeddhasnainn](https://clawhub.ai/user/syeddhasnainn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operations teams use this skill to guide agent-driven PostQued API calls for uploading media, preparing TikTok drafts, scheduling posts, publishing content, and checking publishing status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and bearer tokens could be exposed or over-permissioned. <br>
Mitigation: Keep POSTQUED_API_KEY private, scope it for the intended PostQued use, and avoid placing secrets in prompts, logs, or shared files. <br>
Risk: An agent could upload or publish the wrong file, caption, account, privacy setting, intent, or dispatch time. <br>
Mitigation: Confirm the exact file, caption, target account, privacy setting, intent, and schedule before running upload or publish requests. <br>
Risk: Direct publication may post content publicly before final human review. <br>
Mitigation: Prefer draft mode unless the user explicitly requests direct publication. <br>


## Reference(s): <br>
- [PostQued OpenAPI specification](https://api.postqued.com/v1/docs/openapi.json) <br>
- [PostQued console](https://postqued.com/console) <br>
- [ClawHub release page](https://clawhub.ai/syeddhasnainn/postqued-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a POSTQUED_API_KEY bearer token and user confirmation before upload or publish calls.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
