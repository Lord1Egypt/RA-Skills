## Description: <br>
Local QR Code Generator creates QR codes locally from text or URLs as PNG images or terminal ASCII art without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alone86136](https://clawhub.ai/user/alone86136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to generate QR codes for links, text, or other content while keeping generation local. It is useful when an agent needs to provide a PNG QR image or terminal-readable ASCII QR output without calling an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts require installing the qrcode and Pillow Python packages. <br>
Mitigation: Install the dependencies only in an environment where adding those Python packages is acceptable. <br>
Risk: Encoded content may be printed to the terminal or saved into a visible QR image. <br>
Mitigation: Avoid encoding secrets or sensitive values unless the resulting terminal output and image file can be handled securely. <br>


## Reference(s): <br>
- [Local QR Code Generator on ClawHub](https://clawhub.ai/alone86136/local-qrcode) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts are PNG files or terminal ASCII text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with the qrcode and Pillow Python packages; PNG output supports configurable box size and border size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
