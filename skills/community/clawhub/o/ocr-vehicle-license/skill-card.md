## Description:

识别机动车行驶证的号牌号码、车辆类型、所有人、住址、品牌型号、发动机号码、车辆识别代号等信息，支持自动方向检测和主副页过滤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract structured vehicle-license fields from an image URL or base64-encoded image through the XiaoBenYang OCR API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle-license images or base64 contents may contain sensitive personal and vehicle-registration data and are sent to the XiaoBenYang API.

Mitigation: Use only when users understand that document data is sent to the external API, and add a clear privacy notice before processing real documents.

Risk: The service API key may be stored in a local .env file in plaintext.

Mitigation: Prefer a runtime secret store or environment-managed secret, restrict file permissions, and avoid committing .env files.

Risk: The configurable external API endpoint and unpinned dependencies can increase supply-chain or data-routing risk.

Mitigation: Pin dependencies, restrict or remove base_url overrides, and review endpoint configuration before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-vehicle-license)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an image URL or base64-encoded image and a configured XBY_APIKEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
