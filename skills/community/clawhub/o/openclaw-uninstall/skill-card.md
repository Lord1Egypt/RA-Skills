## Description: <br>
Guides agents and users through confirming, running, and verifying OpenClaw uninstall cleanup on macOS and Linux systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ERerGB](https://clawhub.ai/user/ERerGB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and system administrators use this skill when they need to remove OpenClaw, verify residue, or avoid unnecessary paid cleanup services. It provides confirmation-oriented uninstall guidance, scheduled host execution, manual fallback commands, and read-only cleanup checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled uninstall runs on the real gateway host and can remove OpenClaw state, profiles, services, CLI packages, and the macOS app. <br>
Mitigation: Run the read-only verification script first, confirm the target host and OpenClaw state/profile paths, and proceed only after explicit uninstall confirmation. <br>
Risk: Optional email and ntfy notification values can reach unsafe shell input in the scheduler. <br>
Mitigation: Avoid notification options until scheduler quoting is fixed; run without notification or perform the uninstall manually on a trusted host. <br>
Risk: A delayed scheduled uninstall may be difficult to stop after approval. <br>
Mitigation: Confirm intent before scheduling and review the expected log path and timing before disconnecting the agent session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ERerGB/openclaw-uninstall) <br>
- [OpenClaw uninstall documentation](https://docs.openclaw.ai/install/uninstall) <br>
- [OpenClaw gateway security documentation](https://docs.openclaw.ai/gateway/security) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and procedural uninstall steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes host-execution prerequisites, delayed uninstall scheduling, manual fallback paths, and read-only residue verification output.] <br>

## Skill Version(s): <br>
1.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
