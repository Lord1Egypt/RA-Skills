## Description: <br>
Hik-Connect for Teams (HCT) Developer Skills integrate resource management, access control, device capture, video streaming, and alarm push for HCT devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hikconnectteam](https://clawhub.ai/user/hikconnectteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operations teams use this skill to manage Hik-Connect for Teams devices, query resources, retrieve snapshots or live-stream URLs, configure alarm webhooks, and perform access-control actions through HCTOpen scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remotely unlock doors or set doors to normally open. <br>
Mitigation: Require explicit user confirmation before every access-control action, especially open and normally-open operations, and use dedicated least-privilege HCT credentials. <br>
Risk: Alarm webhook deployment can expose an externally reachable endpoint. <br>
Mitigation: Run webhook receivers only behind HTTPS, enable HMAC signature verification, and scope the OpenClaw notification target tightly. <br>
Risk: Cached tokens, stream URLs, capture URLs, and alarm messages are sensitive. <br>
Mitigation: Protect the runtime environment, prefer environment variables for credentials, restrict cache file access, clear caches in high-security environments, and avoid sharing generated media URLs. <br>
Risk: The release is third-party and the security verdict requires review. <br>
Mitigation: Install only after reviewing the publisher and source evidence, and scan the artifact before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hikconnectteam/hik-connect-team-skill) <br>
- [Publisher profile](https://clawhub.ai/user/hikconnectteam) <br>
- [README](artifact/README.md) <br>
- [Main skill definition](artifact/SKILL.md) <br>
- [Token manager documentation](artifact/lib/README_TOKEN_MANAGER.md) <br>
- [Access control module](artifact/modules/Hik-Connect_Team_ACS/SKILL.md) <br>
- [Alarm module](artifact/modules/Hik-Connect_Team_Alarm/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sensitive tokens, stream URLs, capture URLs, alarm payloads, and access-control operation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
