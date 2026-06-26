## Description: <br>
Paired: Phone Agent bridges an OpenClaw agent to a user-owned phone over Bluetooth and ADB for SMS, calls, contacts, media control, file transfer, PAN tethering, and optional local voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nj070574-gif](https://clawhub.ai/user/nj070574-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers running OpenClaw use this skill to let an agent operate their own paired phone for messaging, calls, device status, media, contacts, file transfer, tethering, and local voice-note or speech generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic SMS and call behaviors can act on a real phone, and server evidence reports incomplete trust gating on some SMS paths. <br>
Mitigation: Review automation paths before installation, keep trusted-numbers.conf empty until deliberate, require explicit confirmation for high-impact actions, and do not enable SMS or call watcher services until their behavior is understood. <br>
Risk: The skill can use sensitive local material such as a phone PIN, API keys, HMAC inbox key, phone identifiers, and a user voice reference. <br>
Mitigation: Avoid storing a phone PIN unless necessary, keep secret files mode 0600, use user-supplied credentials only, and delete unused voice or paired configuration material when no longer needed. <br>
Risk: Persistent services and Telegram relay paths expand the control surface for phone actions. <br>
Mitigation: Enable only the services needed, restrict dispatch to HMAC-signed inbox messages from trusted sources, and stop or disable persistent services when not actively used. <br>
Risk: A voice service exposed beyond the local host could expose local voice-cloning functionality. <br>
Mitigation: Bind voice services to localhost or protect them with firewall rules. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nj070574-gif/paired) <br>
- [Voice cloning setup](artifact/docs/VOICE-SETUP.md) <br>
- [Third-party software attribution](artifact/THIRD_PARTY.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [BlueZ](http://www.bluez.org/) <br>
- [Android Debug Bridge](https://developer.android.com/tools/adb) <br>
- [OpenBMB VoxCPM](https://github.com/OpenBMB/VoxCPM) <br>
- [openbmb/VoxCPM2 model](https://huggingface.co/openbmb/VoxCPM2) <br>
- [coqui XTTS-v2 model](https://huggingface.co/coqui/XTTS-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration paths, and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing wrappers are intended to return JSON-clean status or action results; high-impact phone actions may require confirmation or trusted-number allowlist checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and CHANGELOG-v2.0.0.md, released 2026-05-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
