## Description: <br>
Check MiniMax Token Plan remaining quota, usage window reset time, and per-model remaining limits, especially for the China mainland Token Plan flow on minimaxi.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MiniMax users use this skill to check Token Plan remaining quota, reset timing, and per-model limits without manually calling the MiniMax quota endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MiniMax API key to query MiniMax quota endpoints. <br>
Mitigation: Use an existing environment variable or a one-off key for temporary checks, and rotate the key if it may have been exposed. <br>
Risk: The fallback credential file ~/.openclaw/.env stores the API key in local plaintext. <br>
Mitigation: Restrict filesystem access to ~/.openclaw/.env and avoid storing long-lived keys there when an environment variable is sufficient. <br>


## Reference(s): <br>
- [MiniMax Token Plan Quota on ClawHub](https://clawhub.ai/alex-shen1121/minimax-token-plan-quota) <br>
- [MiniMax China Token Plan quota endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>
- [MiniMax Global Token Plan quota endpoint](https://www.minimax.io/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown table or normalized JSON, with concise setup guidance when credentials are missing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key supplied through MINIMAX_API_KEY, a one-off argument, or ~/.openclaw/.env.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
