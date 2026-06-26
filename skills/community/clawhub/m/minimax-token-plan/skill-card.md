## Description: <br>
查询 MiniMax Token Plan 订阅套餐余额。引导用户配置 API Key（通过 openclaw config set 保存到本地环境变量），查询 M2.7 请求次数、TTS 字符、视频/图片生成配额等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superuser-fank](https://clawhub.ai/user/superuser-fank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External MiniMax Token Plan users use this skill to configure a MiniMax API key and check remaining quotas for M2.7 requests, TTS characters, image generation, video generation, and music generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a MiniMax Token Plan API key to query quota. <br>
Mitigation: Use a limited, revocable key, prefer secure local configuration over pasting secrets into general chat, and revoke or remove the key when it is no longer needed. <br>
Risk: Quota output depends on live MiniMax API responses and correct Token Plan key type. <br>
Mitigation: Confirm the key is valid, Token Plan scoped, and still active if the query fails or returns unexpected quota data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/superuser-fank/minimax-token-plan) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [MiniMax Token Plan](https://platform.minimaxi.com/user-center/payment/token-plan) <br>
- [MiniMax Interface Key Management](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [MiniMax Token Plan Remains API](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and quota query text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a MiniMax Token Plan API key from local configuration or environment.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
