## Description:

图片格式转换与二维码生成工具，支持 PNG、JPEG、WebP、SVG、BMP 格式转换和自定义二维码生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert image formats and generate QR codes through a remote image utility service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User images and QR-code text are sent to an external service.

Mitigation: Review the service provider's logging and retention practices before use, and avoid private photos, confidential documents, internal URLs, credentials, payment data, or other secrets.

Risk: QR-code text may be transmitted with a GET request before falling back to POST.

Mitigation: Avoid sensitive QR payloads and prefer a reviewed implementation that does not place QR contents in URLs.

Risk: The skill uses an admin-style credential for service access.

Mitigation: Deploy only with a narrowly scoped service credential and rotate or revoke credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebang-tools/skills/jiebang-image-toolkit)
- [Publisher profile](https://clawhub.ai/user/jiebang-tools)
- [Jiebang image service](https://www.jiebang.site)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses containing converted image URLs, base64 image data, or QR code image data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image conversion accepts image data or a public image URL, source and target formats, and optional quality; QR generation accepts text, size, and error correction level.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
