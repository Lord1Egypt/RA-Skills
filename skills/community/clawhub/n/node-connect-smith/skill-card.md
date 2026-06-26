## Description: <br>
Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw gateway route, pairing, and authentication failures across local, LAN, Tailscale, and public URL topologies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approving the wrong device or node could grant access to an unintended OpenClaw client. <br>
Mitigation: Verify the current pending request ID and device identity before approving devices or nodes. <br>
Risk: Authentication tokens may be displayed during token repair or drift recovery. <br>
Mitigation: Treat displayed auth tokens as sensitive and avoid sharing them in logs, screenshots, or chat. <br>
Risk: Changing routes before confirming topology can lead to misleading troubleshooting or unreachable gateways. <br>
Mitigation: Confirm the intended topology first, then apply one targeted route fix and verify the relevant route selectors once. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ciklopentan/node-connect-smith) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposes a sequential troubleshooting path and targeted OpenClaw configuration checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
