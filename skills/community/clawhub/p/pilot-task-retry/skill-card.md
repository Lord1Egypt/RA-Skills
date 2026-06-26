## Description: <br>
Automatic retry with exponential backoff and fallback targets for Pilot Protocol task submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create resilient Pilot Protocol task submission workflows with retries, jitter, and fallback agents for transient failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retries and fallback agents may repeat or reroute a task submission. <br>
Mitigation: Use the skill for idempotent tasks and confirm fallback agents are appropriate before submitting sensitive or side-effecting work. <br>
Risk: The skill depends on the local Pilot Protocol setup and pilotctl daemon. <br>
Mitigation: Install it only when you intentionally use Pilot Protocol and trust the local pilotctl and daemon configuration. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon, jq, and Bash 4.0+.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
