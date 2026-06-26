## Description: <br>
Creates and manages isolated OpenClaw rescue Gateway instances with automatic port allocation and batch creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangkai258](https://clawhub.ai/user/yangkai258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create backup, testing, or environment-isolated OpenClaw Gateway instances on macOS. It helps manage per-instance configuration, state directories, ports, logs, and LaunchAgent services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent macOS LaunchAgent services keep OpenClaw Gateway instances running in the background. <br>
Mitigation: Install only when persistent background gateways are intended, and review created LaunchAgent plist files before loading them. <br>
Risk: Deletion behavior can remove rescue instance service files and directories. <br>
Mitigation: Require confirmation for delete operations and restrict instance names to a safe pattern such as rescue followed by digits. <br>
Risk: Copied OpenClaw configuration may include credentials or account settings. <br>
Mitigation: Review copied configuration before starting a rescue instance and remove secrets or account settings that should not be reused. <br>
Risk: Hard-coded Node and OpenClaw paths may not match the user's machine. <br>
Mitigation: Verify and adjust runtime paths before loading LaunchAgent services. <br>


## Reference(s): <br>
- [OpenClaw Rescue Instances release page](https://clawhub.ai/yangkai258/openclaw-rescue-instances) <br>
- [Quick Reference](artifact/references/quick-reference.md) <br>
- [Multiple Gateways](/gateway/multiple-gateways) <br>
- [Gateway Configuration](/gateway/configuration) <br>
- [CLI Gateway](/cli/gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates or invokes shell workflows that create directories, copy OpenClaw configuration, allocate ports, and manage macOS LaunchAgent services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
