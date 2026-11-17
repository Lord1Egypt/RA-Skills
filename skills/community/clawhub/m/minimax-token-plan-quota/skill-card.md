## Description:

Check MiniMax Token Plan remaining quota, usage window reset time, and per-model remaining limits, especially for the China mainland Token Plan flow on minimaxi.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MiniMax Token Plan users use this skill to check remaining plan quota, reset timing, and per-model limits from MiniMax endpoints. It is useful when a user wants a compact quota table or normalized JSON for the China mainland or global Token Plan flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a MiniMax API key to check quota.

Mitigation: Prefer MINIMAX_API_KEY in a protected environment or secret manager, and use pasted or CLI-provided keys only transiently.

Risk: Storing the key in ~/.openclaw/.env can expose it if file permissions are too broad.

Mitigation: Create ~/.openclaw with 0700 permissions and the .env file with 0600 permissions before adding the key.

Risk: Passing real keys in inline shell commands or --api-key arguments can leave secrets in shell history or logs.

Mitigation: Avoid inline secrets and rotate any key that may have been saved in history or logs.

## Reference(s):

- [MiniMax China mainland Token Plan quota endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)
- [MiniMax global Token Plan quota endpoint](https://www.minimax.io/v1/api/openplatform/coding_plan/remains)
- [MiniMax Token Plan Quota on ClawHub](https://clawhub.ai/alex-shen1121/skills/minimax-token-plan-quota)
- [alex-shen1121 ClawHub publisher profile](https://clawhub.ai/user/alex-shen1121)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown table or normalized JSON, with concise setup guidance when credentials are missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key supplied through MINIMAX_API_KEY, ~/.openclaw/.env, or a transient --api-key argument.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
