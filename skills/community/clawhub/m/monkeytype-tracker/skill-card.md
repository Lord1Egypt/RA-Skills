## Description: <br>
Track and analyze Monkeytype typing statistics with improvement tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qrucio](https://clawhub.ai/user/Qrucio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve Monkeytype stats, review recent typing history, compare progress, check leaderboards, and receive practice advice after configuring a Monkeytype ApeKey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Monkeytype ApeKey can be exposed if pasted into chat or stored in plaintext configuration. <br>
Mitigation: Prefer MONKEYTYPE_APE_KEY and avoid sharing the key in chat; delete ~/.openclaw/workspace/config/monkeytype.json and rotate the key when uninstalling or if exposure is suspected. <br>
Risk: Optional daily or weekly reports can leave recurring background jobs after setup. <br>
Mitigation: Enable reports only when wanted, document the created schedule, and remove the related cron entries when disabling automation or uninstalling the skill. <br>
Risk: Monkeytype API access can fail because of inactive keys, invalid keys, rate limits, or network errors. <br>
Mitigation: Validate the key during setup, surface API errors clearly, and retry later when rate limits or network failures occur. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Qrucio/monkeytype-tracker) <br>
- [Monkeytype API base URL](https://api.monkeytype.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update user configuration and optional scheduled report jobs when the user enables automation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
