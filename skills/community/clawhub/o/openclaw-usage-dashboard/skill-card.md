## Description: <br>
Interactive local dashboard for OpenClaw API usage that reads local session logs to show token consumption, request counts, model and agent activity, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanhuelsing](https://clawhub.ai/user/vanhuelsing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local token usage, request volume, model activity, agent activity, and basic system health without sending data to an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dashboard reads OpenClaw session history across agents, which may expose sensitive local usage metadata. <br>
Mitigation: Run with the default localhost binding, avoid using --host to expose it on a network, and stop the Node server when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vanhuelsing/openclaw-usage-dashboard) <br>
- [OpenClaw rate limits tracking issue](https://github.com/openclaw/openclaw/issues/55934) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local dashboard usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill starts a localhost dashboard and presents aggregated OpenClaw usage and system health information.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
