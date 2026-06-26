## Description: <br>
Provides operating guardrails for agents working on Omarchy systems, steering local system tasks toward Omarchy-native wrappers and cautious review of high-impact commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AchalS-iglu](https://clawhub.ai/user/AchalS-iglu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when asking an agent to help with local system work on an Omarchy host. It helps the agent choose Omarchy-specific status, refresh, restart, package, theme, update, and setup workflows before proposing broader Linux commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to propose Omarchy commands that affect packages, updates, setup, reset, password, power, or log-upload behavior. <br>
Mitigation: Confirm the host is Omarchy and review any high-impact command before approving execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AchalS-iglu/omarchy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no API keys or MCP tools are required.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
