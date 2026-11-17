## Description:

视频去除水印解析 Skill，支持抖音、快手、小红书、微博、西瓜视频、豆包、云雀、B站等 20+ 平台的短视频去水印解析。

This skill is for research and development only.

## Publisher:

[mackjosn](https://clawhub.ai/user/mackjosn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to parse supported short-video or social-media share links and retrieve de-watermarked media metadata and temporary media URLs. It supports command-line parsing and an optional local HTTP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTTP service could expose video parsing functionality if bound beyond localhost or deployed without access controls.

Mitigation: Keep service mode bound to localhost, avoid public exposure, and add authentication before any shared deployment.

Risk: The documented workflow depends on platform binaries that are referenced by the skill but absent from the submitted artifact.

Mitigation: Verify the supplied package includes trusted binaries for the intended platform before installation or execution.

Risk: Parsed media links are temporary third-party network data and may expire or change behavior as platforms update.

Mitigation: Use parsed links promptly, validate results before relying on them, and expect periodic breakage from upstream platform changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mackjosn/skills/midea-nomark)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful parses may return temporary third-party media links, titles, author information, cover URLs, and image counts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
