## Description: <br>
Verify Polymarket MR-V4 trading system deployment health after strategy or configuration updates by running a comprehensive local check script and reporting results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbyw1028](https://clawhub.ai/user/bobbyw1028) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining the local Polymarket MR-V4 trading deployment use this skill to check process counts, duplicate traders, lock files, configuration values, trade activity, process isolation, and data collector health after deployment changes or restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verifier is tailored to a specific local Polymarket MR-V4 deployment and hardcoded local paths. <br>
Mitigation: Install and run it only for the intended deployment, and review the /Users/0xbobby paths before execution. <br>
Risk: The checks inspect local processes, configuration files, PID files, and trading logs that may expose operational details. <br>
Mitigation: Run it in a trusted local shell and avoid sharing raw output unless sensitive deployment details have been reviewed. <br>


## Reference(s): <br>
- [Polymarket Verify on ClawHub](https://clawhub.ai/bobbyw1028/polymarket-verify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with an inline bash command and terminal pass, warning, and fail output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The verifier exits with the number of failed checks and prints a concise status summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
