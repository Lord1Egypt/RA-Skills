## Description: <br>
Intel Local Windows Computer Use helps an agent interpret Chinese or English requests to query or change supported Windows system state and settings through its local client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makejiang](https://clawhub.ai/user/makejiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators on supported Intel AIPC Windows systems use this skill to query or adjust local settings such as power, devices, display, shell appearance, apps, accounts, privacy, notifications, and localization. The skill is intended for local Windows use through its documented client rather than remote or arbitrary system administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is security-classified as suspicious because it bundles under-disclosed native Windows code, broad local-system capabilities, and a persistent runtime. <br>
Mitigation: Install only when the publisher is trusted, review the bundled artifacts before use, and limit execution to specific, intentional local Windows settings tasks. <br>
Risk: The skill can modify local system, account, privacy, app, network, display, and power settings, and some actions may request administrator privileges. <br>
Mitigation: Approve elevated prompts only for a requested change the user explicitly intends, and avoid using it for unsupported arbitrary PowerShell, registry, or remote-control tasks. <br>
Risk: First run downloads models and creates persistent runtime files under %USERPROFILE%\.openvino that remain after the skill folder is removed. <br>
Mitigation: Use the documented server shutdown command before uninstalling and manually remove %USERPROFILE%\.openvino when a fully clean removal is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makejiang/local-computer-use) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/makejiang) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON messages and concise text guidance, with Windows command examples for invoking the local client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include success, result, and finished fields; some requests require continuation while models download or administrator privileges for specific system changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact meta.json reports packaged runtime version 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
