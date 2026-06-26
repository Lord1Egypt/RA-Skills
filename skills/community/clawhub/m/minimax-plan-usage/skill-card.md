## Description: <br>
Queries MiniMax Token Plan remaining usage and reset times for text, speech, video, image, and music models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-zxyz](https://clawhub.ai/user/alex-zxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MiniMax Token Plan subscribers use this skill to check remaining model usage and reset timing from an agent or Discord slash command without opening the MiniMax web console. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A MiniMax Token Plan API key is used to query account usage. <br>
Mitigation: Install only where MINIMAX_API_KEY is intentionally available and avoid exposing command output or environment variables in shared logs. <br>
Risk: The optional MINIMAX_API_HOST setting could direct the request away from the expected MiniMax endpoint. <br>
Mitigation: Leave MINIMAX_API_HOST unset or set it only to an official MiniMax endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alex-zxyz/minimax-plan-usage) <br>
- [MiniMax Token Plan](https://platform.minimax.io/subscribe/token-plan) <br>
- [MiniMax Token Plan remains API](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown usage summary by default; JSON when requested by the script option.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax Token Plan API key and can query an alternate API host if MINIMAX_API_HOST is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
