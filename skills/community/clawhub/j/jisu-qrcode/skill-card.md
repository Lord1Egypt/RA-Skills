## Description: <br>
Generates styled QR codes from text as base64, reads QR code contents from image URLs or base64 images, and lists available JisuAPI QR templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create QR code images, decode QR code contents, and retrieve template samples through the JisuAPI QR code service. QR contents and images are sent to the external JisuAPI provider, so avoid private, login, payment, or otherwise sensitive QR data unless external processing is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-qrcode) <br>
- [JisuAPI QR Code API](https://www.jisuapi.com/api/qrcode/) <br>
- [JisuAPI home](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and JISU_API_KEY; generated QR codes are returned as base64 and decoded QR contents are returned as text.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
