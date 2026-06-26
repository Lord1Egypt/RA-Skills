## Description: <br>
Monitors dual Claude Max accounts' 5-hour and 7-day usage, shows a local real-time dashboard, and can switch accounts when utilization exceeds 80%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Takao-Mochizuki](https://clawhub.ai/user/Takao-Mochizuki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users with two Claude Max accounts use this skill to monitor remaining capacity, view local usage status, and configure account switching before rate limits interrupt work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Claude account tokens and can change the active OpenClaw Anthropic account. <br>
Mitigation: Review the scripts before installation, protect or avoid tokens.json, back up auth-profiles.json, and test manually before enabling cron. <br>
Risk: The dashboard launch behavior can terminate local processes on port 18800. <br>
Mitigation: Remove or modify the automatic port-kill behavior if port 18800 may be used by other local software. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Takao-Mochizuki/openclaw-usage-manager) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [1Password CLI documentation](https://developer.1password.com/docs/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, configuration steps, and JSON usage output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and operating guidance for a browser dashboard and account-switching script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
