## Description: <br>
Monitor Minimax Coding Plan usage to stay within API limits, fetch current usage stats, and provide status alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franky0617](https://clawhub.ai/user/franky0617) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check MiniMax Coding Plan prompt usage, remaining quota, and reset timing before continuing API-backed coding work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sources a parent `.env` file rather than the documented same-directory `.env`, which may expose or execute unexpected environment content. <br>
Mitigation: Review the sourced `.env` path before running, keep only the intended MiniMax variables in scope, and prefer changing the script to read a same-directory `.env` or already-exported environment variables. <br>
Risk: The skill requires a MiniMax Coding Plan API key and Group ID to query account usage. <br>
Mitigation: Store credentials outside shared logs and repositories, and restrict the API key to the intended Coding Plan account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/franky0617/minimax-coding-plan-usage) <br>
- [MiniMax Basic Information](https://platform.minimax.com/user-center/basic-information) <br>
- [MiniMax Coding Plan Usage Endpoint](https://platform.minimax.com/v1/api/openplatform/coding_plan/remains?GroupId={GROUP_ID}) <br>
- [MiniMax Coding Plan Payment Page](https://platform.minimax.com/user-center/payment/coding-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output with setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports used prompts, total quota, remaining prompts, reset countdown, and threshold-based status alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
