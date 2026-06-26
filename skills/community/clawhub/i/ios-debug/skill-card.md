## Description: <br>
Helps developers debug iOS apps on an iPhone 14 by collecting stdout logs, capturing QuickTime-mirrored screenshots, building, installing, launching, uninstalling apps, and checking device status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sougannkyou](https://clawhub.ai/user/sougannkyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill on a trusted macOS development machine to inspect logs, capture device screenshots, deploy debug builds, and troubleshoot connection or signing issues for an attached iPhone 14. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local device-control commands can install, uninstall, launch, or provision an app on a connected iPhone. <br>
Mitigation: Run commands only on a trusted macOS development machine and verify the device ID, bundle ID, project, and scheme before execution. <br>
Risk: Logs and screenshots may expose sensitive app or device information. <br>
Mitigation: Capture and review logs or phone screens locally only when intended, and avoid collecting sensitive screens or logs unnecessarily. <br>
Risk: Background console or log streams can continue running after debugging. <br>
Mitigation: Stop background log streams and launched console processes when the debugging session is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sougannkyou/ios-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes device-specific commands and placeholders for project, scheme, app name, and bundle ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
