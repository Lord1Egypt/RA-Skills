## Description: <br>
捷帮图片工具 converts images between PNG, JPEG, WebP, SVG, and BMP formats and generates customizable QR codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert image formats or generate QR codes from image URLs, base64 images, and text payloads. It is best suited for non-sensitive content because requests are sent to an external JieBang service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image inputs and QR payloads to an external service. <br>
Mitigation: Use only non-sensitive images, public image URLs, and QR contents that are appropriate to share with the JieBang service. <br>
Risk: The security scan reports use of an admin-key credential without clear user-facing disclosure. <br>
Mitigation: Review the credential scope before installation and prefer a release that clearly discloses remote processing and uses a narrowly scoped API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-image-toolkit) <br>
- [JieBang service](https://www.jiebang.site) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, image URLs, base64 image data] <br>
**Output Format:** [JSON objects containing conversion results, image metadata, image URLs, or base64-encoded QR code images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image conversion accepts source and target formats plus optional quality; QR generation accepts text, size, and error correction level.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
