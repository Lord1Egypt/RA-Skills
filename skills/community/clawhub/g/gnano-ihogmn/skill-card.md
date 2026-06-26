## Description: <br>
GNano Ihogmn 图片生成技能 - 支持动态 API 配置，根据 Token 自动获取可用功能，支持文生图和图生图 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielchen59](https://clawhub.ai/user/danielchen59) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure GNano image-generation access, discover account-specific model capabilities from a token, and run text-to-image or image-to-image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles user-provided GNano API tokens. <br>
Mitigation: Use a limited, revocable token and delete any local task state containing token-derived configuration when finished. <br>
Risk: Tokens and prompts are sent to the configured GNano API endpoint. <br>
Mitigation: Use the default endpoint unless a custom API URL is trusted, and assume submitted data is visible to that service. <br>
Risk: Reference images may contain sensitive content and are uploaded for image-to-image generation. <br>
Mitigation: Do not submit sensitive reference images; review image paths and size limits before running generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielchen59/gnano-ihogmn) <br>
- [GNano API service](https://gnano.ihogmn.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command results, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated image files to a requested output path and may emit JSON progress or result details.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
