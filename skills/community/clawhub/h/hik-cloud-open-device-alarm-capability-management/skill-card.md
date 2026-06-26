## Description: <br>
Manages Hik-Cloud Open Platform device alarm capabilities by listing alarm abilities, updating alarm status, and controlling the intelligence detection switch while handling OAuth token acquisition and refresh internally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect and change Hik-Cloud device alarm capability settings, including motion detection, video tampering, intrusion detection, and intelligence detection switch controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Hik-Cloud device alarm settings. <br>
Mitigation: Verify deviceSerial, channelId, abilityCode, type, enable, and status values before running mutating commands. <br>
Risk: The helper requires sensitive Hik-Cloud OAuth credentials and may cache an access token. <br>
Mitigation: Use least-privileged credentials and protect or clear ~/.cache/hik_open/token.json on shared systems. <br>
Risk: A custom base URL can redirect requests away from the intended Hik-Cloud endpoint. <br>
Mitigation: Use only trusted Hik-Cloud base URLs and avoid untrusted custom base URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-device-alarm-capability-management) <br>
- [Hik-Cloud Device Alarm Capability API Reference](https://pic.hik-cloud.com/opencustom/apidoc/online/open/f8cbf864c4ca4395909dad225902a6ee.html) <br>
- [Authentication Reference](references/auth.md) <br>
- [Device Alarm Capability Management Reference](references/device-alarm-capability-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and Hik-Cloud credentials from environment variables or OpenClaw configuration; command output may summarize or return raw API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
