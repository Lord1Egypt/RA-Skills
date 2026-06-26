## Description: <br>
Local-only semantic context filtering for OpenClaw using OMNI that distills shell output without data exfiltration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fajarhide](https://clawhub.ai/user/fajarhide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route local terminal commands through OMNI, receiving distilled command output and retrieving full archived logs when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad shell-like local command execution through OMNI. <br>
Mitigation: Install only when this behavior is intended, keep normal command approvals enabled, and review commands before execution. <br>
Risk: The configured OMNI binary controls command execution and output distillation. <br>
Mitigation: Verify the OMNI binary before use and prefer an absolute omniPath for the expected executable. <br>
Risk: Command output may be stored locally for rewind and log retrieval. <br>
Mitigation: Avoid commands that print secrets, and periodically inspect or clear the local OMNI archive when sensitive output may have been captured. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fajarhide/omni-signal-engine) <br>
- [OMNI repository](https://github.com/fajarhide/omni) <br>
- [OMNI security policy](https://github.com/fajarhide/omni/blob/main/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text command output and JSON-like tool results, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local omni binary; the rewind tool can return archived command output by hash.] <br>

## Skill Version(s): <br>
0.5.9 (source: server release evidence and openclaw.plugin.json; SKILL.md lists 0.5.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
