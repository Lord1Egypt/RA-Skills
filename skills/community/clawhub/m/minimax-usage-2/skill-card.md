## Description: <br>
Check MiniMax coding plan usage/credits remaining. Requires MINIMAX_API_KEY environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check MiniMax coding plan credits and optionally emit an alert only when remaining usage falls below a configured threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script uses MINIMAX_API_KEY to query MiniMax usage. <br>
Mitigation: Provide the key only through a trusted local environment or cron environment, and do not expose it in shared logs or command history. <br>
Risk: Cron or webhook usage can forward usage balance details outside the local machine. <br>
Mitigation: Send output only to private, trusted destinations and review webhook configuration before enabling automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khaney64/minimax-usage-2) <br>
- [MiniMax coding plan remains API](https://www.minimax.io/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Discord-formatted Markdown text emitted by a Bash script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May exit with no output when a threshold is configured and remaining usage is above that threshold.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
