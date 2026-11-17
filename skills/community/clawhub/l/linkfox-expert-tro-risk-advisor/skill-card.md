## Description:

TRO风险提示专家 helps cross-border POD sellers and ecommerce operators quickly triage copyright, trademark, celebrity, brand, sports, university, religious, and platform infringement risk from product images or text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and agent users use this skill to assess TRO and intellectual-property risk for POD product images or titles before listing. It returns a concise risk level, the key risk points, and handling advice, with optional routing to deeper copyright, trademark, or patent checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send product images, prompts, detection inputs, feedback content, account tokens, and billing-related operations to LinkFox services.

Mitigation: Install only when LinkFox is trusted with those materials, and avoid submitting sensitive or non-public assets unless that sharing is acceptable.

Risk: Security evidence flags endpoint override, credential, and persistence patterns that users should review before installation.

Mitigation: Use reviewed default endpoints, do not use unreviewed LINKFOX_* endpoint overrides, and avoid storing API keys in shell startup files.

Risk: Generated HTML reports and automatic feedback behavior may expose or preserve user content in ways users do not expect.

Mitigation: Treat generated HTML as untrusted until sanitized, and review feedback behavior because it can send user statements or inferred intent to LinkFox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-tro-risk-advisor)
- [Main skill instructions](SKILL.md)
- [AIGC text generation API](skills/linkfox-aigc-textgen/references/api.md)
- [Copyright detection API](skills/linkfox-ruiguan-copyright-detection/references/api.md)
- [Graphic trademark detection API](skills/linkfox-ruiguan-trademark-graphic-detection/references/api.md)
- [Text trademark detection API](skills/linkfox-ruiguan-text-trademark-detection/references/api.md)
- [Design patent detection API](skills/linkfox-ruiguan-detection-patent-design/references/api.md)
- [Utility patent detection API](skills/linkfox-ruiguan-utility-patent-detection/references/api.md)
- [Patent image search API](skills/linkfox-zhihuiya-patent-image-search/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Concise Chinese Markdown with a fixed risk level, core risk points, and handling advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call supporting LinkFox visual analysis, copyright, trademark, patent, upload, and report skills when deeper verification or URL-based inputs are needed.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
