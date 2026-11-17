## Description:

Generates styled QR codes from text or URLs, reads QR code contents from image URLs or base64 input, and lists available QR templates through JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create QR code images for text or URLs, decode QR contents from supplied images, and retrieve QR template examples. It is suited for workflows that can send QR payloads and image data to JisuAPI for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR text, QR image URLs, base64 QR images, logo URLs, and the JisuAPI key are sent to JisuAPI for processing.

Mitigation: Use the skill only when that disclosure is acceptable, and avoid QR codes that contain secrets, credentials, tokens, internal links, or private customer data.

Risk: API-key use can expose quota and account access if the key is over-privileged or mishandled.

Mitigation: Use a dedicated least-privileged JISU_API_KEY and monitor quota usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-qrcode)
- [JisuAPI QR Code API](https://www.jisuapi.com/api/qrcode/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Configuration instructions]

**Output Format:** [JSON responses containing base64 QR image data, decoded text, template URLs, or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends QR text, QR image URLs, base64 QR images, logo URLs, and the API key to JisuAPI.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
