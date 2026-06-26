## Description: <br>
Quickly shorten URLs and generate QR codes via PicSee (picsee.io), with access to analytics and history after login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PicSeeInc](https://clawhub.ai/user/PicSeeInc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and teams use this skill to shorten long URLs through PicSee and optionally create QR codes for sharing. Logged-in PicSee users can also use it to inspect link analytics and history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs submitted for shortening are sent to PicSee. <br>
Mitigation: Use the skill only for links you are comfortable processing through PicSee. <br>
Risk: If the browser profile is logged into PicSee, shortened links may be associated with that account. <br>
Mitigation: Use a separate browser profile or log out when account association is not desired. <br>
Risk: Optional QR-code generation creates a local Python virtual environment and installs qrcode and pillow. <br>
Mitigation: Request QR codes only when local package installation is acceptable. <br>


## Reference(s): <br>
- [PicSee website](https://picsee.io/) <br>
- [ClawHub skill page](https://clawhub.ai/PicSeeInc/picsee-url-shortener-web) <br>
- [Publisher profile](https://clawhub.ai/user/PicSeeInc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown text with an optional generated PNG QR-code file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a shortened URL by default; QR-code generation is opt-in and may create /tmp/picsee_qr.png.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
