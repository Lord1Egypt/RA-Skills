## Description: <br>
Generate, decode, and beautify QR codes with customizable colors, logos, and formats. Works across all OpenClaw channels including WhatsApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zouyawen](https://clawhub.ai/user/zouyawen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create styled QR code image files, decode QR code images, and adapt QR outputs for messaging channels such as WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommended full setup uses an unverified remote installer piped directly to a shell. <br>
Mitigation: Download and inspect the installer first, pin a trusted release or commit, verify checksums or signatures if available, and run it in a contained environment when trust cannot be established. <br>
Risk: Logo and image handling can expose unintended local files if path controls are bypassed. <br>
Mitigation: Use workspace-relative logo paths only and reject absolute paths or paths containing '..', matching the skill's documented validation rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zouyawen/openclaw-qr-code) <br>
- [Companion plugin repository](https://github.com/zouyawen/openclaw-qrcode) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Markdown responses with generated QR code file paths, media paths, and decoded QR text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [QR code outputs are documented under ~/clawd/qr-codes/; channel compatibility may convert SVG output to PNG or JPG.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
