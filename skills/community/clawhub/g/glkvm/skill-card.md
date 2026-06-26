## Description: <br>
Remotely control a target host via GLKVM HTTP API, supporting keyboard/mouse input, screenshot capture, OCR recognition, Fingerbot physical button control, and ATX power management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzefu](https://clawhub.ai/user/duzefu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent administer a trusted GLKVM device and attached host, including screen inspection, keyboard and mouse control, power workflows, firmware operations, and remote ISO media handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad remote control over a GLKVM device and the attached host. <br>
Mitigation: Install only for trusted GLKVM devices on trusted networks, and require explicit approval before power, reset, firmware upgrade, or virtual media actions. <br>
Risk: Screenshots and OCR output may expose sensitive host information. <br>
Mitigation: Treat captured images and recognized text as sensitive data and avoid retaining or sharing them beyond the session need. <br>
Risk: The documented HTTP examples ignore TLS certificate errors. <br>
Mitigation: Verify the device endpoint and network path before use, and avoid using the skill on untrusted networks. <br>
Risk: Firmware and ISO workflows can introduce untrusted software to the device or host. <br>
Mitigation: Verify firmware and ISO sources before download, upload, mounting, or installation. <br>


## Reference(s): <br>
- [ClawHub glkvm page](https://clawhub.ai/duzefu/glkvm) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline bash code blocks and GLKVM HTTP API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots and cookies to local temporary files; GLKVM responses may include JSON, image files, OCR text, or NDJSON progress streams.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
