## Description: <br>
Controls Hik-Cloud Open Platform device operations, including arm and disarm status, PTZ movement, remote capture, OSD configuration, device time and NTP settings, and storage-card initialization while handling access-token refresh internally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and device operations teams use this skill to ask an agent to operate Hik-Cloud cameras and security devices through approved command flows. It is intended for authenticated device-control tasks such as PTZ movement, capture, OSD updates, time synchronization, arm/disarm checks, and storage initialization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact actions on real Hik-Cloud security devices, including PTZ movement, capture, arm/disarm, OSD changes, time or NTP changes, and storage initialization. <br>
Mitigation: Require manual confirmation for device-changing commands and use least-privileged Hik-Cloud credentials scoped only to the intended devices. <br>
Risk: The skill uses sensitive OAuth credentials and may cache access tokens. <br>
Mitigation: Protect the token cache location, avoid exposing raw tokens in agent output or logs, and disable or isolate caching where the deployment environment supports it. <br>
Risk: A custom base URL can redirect authentication and device-control traffic away from the expected Hik-Cloud endpoint. <br>
Mitigation: Allow only trusted base URLs and review any `HIK_OPEN_BASE_URL` or `--base-url` override before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-device-control) <br>
- [Authentication Reference](artifact/references/auth.md) <br>
- [Device Arm/Disarm Reference](artifact/references/device-arm-disarm.md) <br>
- [PTZ Control Reference](artifact/references/ptz-control.md) <br>
- [Remote Capture Reference](artifact/references/remote-capture.md) <br>
- [Device OSD Reference](artifact/references/device-osd.md) <br>
- [Time Sync Reference](artifact/references/time-sync.md) <br>
- [Storage Card Initialization Reference](artifact/references/storage-card-init.md) <br>
- [Hik-Cloud Time Sync API Page](https://pic.hik-cloud.com/opencustom/apidoc/online/open/7093bbc2db7a427ca5b60001caff338d.html) <br>
- [Hik-Cloud Storage Initialization API Page](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a9efdfc48a2f4ab5bd7c44ba325b6642.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and optional text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Hik-Cloud credentials supplied through environment variables or an explicit access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
