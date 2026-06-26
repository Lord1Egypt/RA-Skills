## Description: <br>
Diagnose and recover OpenClaw node connectivity over SSH tunnel. Use for pairing-required errors, tunnel conflicts, wrong remote endpoint, and ssh target mismatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyezir](https://clawhub.ai/user/xyezir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and recover OpenClaw node connectivity over SSH tunnels, including pairing-required errors, local port conflicts, remote endpoint mismatches, and unstable node status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH targets, API endpoints, gateway credentials, real IPs, domains, and paths can expose sensitive infrastructure details if copied into chat or reports. <br>
Mitigation: Use placeholders for network, identity, path, and credential values, and avoid pasting long-lived secrets into agent conversations or external reports. <br>
Risk: Incorrect tunnel endpoint, SSH target, or credential guidance can leave a node disconnected or routed through the wrong endpoint. <br>
Mitigation: Verify the tunnel-local endpoint, SSH target mapping, and gateway credential auth mode, then re-run probe and status checks before treating recovery as complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with root cause, ordered fixes, verification evidence, residual risk, and next action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for sensitive network, identity, path, and credential fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
