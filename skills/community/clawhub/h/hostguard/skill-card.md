## Description: <br>
Check whether OpenClaw is listening beyond localhost or running with elevated privileges, then offer a conservative lockdown fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check local OpenClaw host binding, listener state, and elevated-privilege status, then receive conservative lockdown guidance when a risky configuration is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest changing HOST or OPENCLAW_HOST to 127.0.0.1, which can intentionally disable LAN or remote OpenClaw access. <br>
Mitigation: Review the proposed edit before approving it and confirm that local-only access is the intended operating mode. <br>
Risk: Listener and privilege checks inspect local configuration and process state, so results depend on the current host environment and available system tools. <br>
Mitigation: Treat findings as local diagnostic guidance and verify important exposure decisions with the target deployment's own network and process controls. <br>


## Reference(s): <br>
- [ClawHub HostGuard skill page](https://clawhub.ai/tobewin/hostguard) <br>
- [ToBeWin publisher profile](https://clawhub.ai/user/tobewin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and security assessment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose configuration edits only after explicit user approval; intended checks are conservative and local.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
