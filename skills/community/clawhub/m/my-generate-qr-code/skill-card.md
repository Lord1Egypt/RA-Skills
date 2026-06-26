## Description: <br>
Generates QR-code images for text, URLs, and WiFi configuration details with configurable size, color, and save path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayXu-D](https://clawhub.ai/user/JayXu-D) <br>

### License/Terms of Use: <br>


## Use Case: <br>
End users and developers use this skill to turn supplied text, URLs, phone numbers, or WiFi settings into a QR-code image saved to a chosen local path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install Python packages when imported, which may change the local Python environment. <br>
Mitigation: Install trusted, pinned versions of qrcode and Pillow in a controlled Python environment before using the skill. <br>
Risk: Generated QR-code files may contain sensitive data such as WiFi passwords, phone numbers, or private URLs. <br>
Mitigation: Choose a private save location and avoid shared or synced folders for QR codes that encode sensitive information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Text status message with a generated local image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a QR-code image to the requested path or the user's desktop by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
