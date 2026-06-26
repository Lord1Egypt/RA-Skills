## Description: <br>
Safe OpenClaw config change workflow with backup, minimal edits, validation, health checks, and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1987566643](https://clawhub.ai/user/1987566643) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route OpenClaw configuration changes through a backup, validation, health-check, and rollback workflow. It is intended for single-instance changes by default, with optional secondary-instance validation for higher-risk updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A change script can alter OpenClaw configuration in a way that fails validation or disrupts the gateway. <br>
Mitigation: Create timestamped backups before edits, run OpenClaw validation immediately, and restore backups with a gateway restart on failure. <br>
Risk: Unreviewed edit scripts could make broader configuration changes than intended. <br>
Mitigation: Review edit-main.sh and edit-secondary.sh before running the wrapper and keep changes limited to necessary keys. <br>
Risk: Secondary-instance validation requires a token and could expose credentials if handled carelessly. <br>
Mitigation: Provide SECONDARY_TOKEN only through the environment when secondary validation is intentionally enabled, and do not hardcode secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1987566643/openclaw-safe-change-flow) <br>
- [Publisher profile](https://clawhub.ai/user/1987566643) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow guidance and script-file commands for OpenClaw configuration changes; no structured API output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
