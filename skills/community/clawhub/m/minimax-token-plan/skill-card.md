## Description:

Queries remaining balances for a MiniMax Token Plan subscription, including M2.7 requests and TTS, image, video, and music quotas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superuser-fank](https://clawhub.ai/user/superuser-fank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MiniMax Token Plan users use this skill to configure a MiniMax API key and check remaining subscription quota across text, speech, image, video, and music generation allowances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste a MiniMax API key into chat while following the skill's setup flow.

Mitigation: Configure the key locally instead, use a least-privilege Token Plan key, and rotate any key that has already been shared in a conversation.

Risk: The skill encourages local credential storage with limited disclosure about where OpenClaw stores the key.

Mitigation: Review OpenClaw's local configuration storage before saving the key and remove or rotate the credential when it is no longer needed.

Risk: The query script returns raw MiniMax API output rather than the polished report shown in the skill text.

Mitigation: Inspect returned values before sharing them and treat the response as direct quota endpoint output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superuser-fank/skills/minimax-token-plan)
- [MiniMax platform](https://platform.minimaxi.com)
- [MiniMax Token Plan page](https://platform.minimaxi.com/user-center/payment/token-plan)
- [MiniMax interface key management](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [MiniMax Token Plan remains endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal output, with raw JSON returned by the query script on successful API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax Token Plan API key in the MINIMAX_API_KEY environment variable.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
