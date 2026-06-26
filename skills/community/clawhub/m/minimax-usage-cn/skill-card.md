## Description: <br>
Monitor Minimax Coding Plan usage to stay within API limits, fetch current usage stats, and provide status alerts for the 5-hour sliding window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanhaixuan](https://clawhub.ai/user/lanhaixuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Minimax Coding Plan users use this skill to check remaining API quota, inspect 5-hour window status, and decide whether to proceed before large AI tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MINIMAX_API_KEY to call the Minimax usage endpoint. <br>
Mitigation: Use a dedicated or least-privilege key where possible, keep it out of shared logs, and provide it only in the environment where the quota check runs. <br>
Risk: The optional cron example can create recurring background quota checks and log output. <br>
Mitigation: Add cron scheduling only when intentional, and review the log path and any alert destination before enabling recurring checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanhaixuan/minimax-usage-cn) <br>
- [Minimax homepage](https://www.minimaxi.com) <br>
- [Minimax Coding Plan usage endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text status output or JSON from a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MINIMAX_API_KEY; supports --json/-j for programmatic output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
