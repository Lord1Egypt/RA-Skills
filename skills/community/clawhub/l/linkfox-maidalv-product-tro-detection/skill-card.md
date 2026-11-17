## Description:

Checks product images and optional text through LinkFox's Maidalu TRO and IP-risk service to return risk levels, possible trademark, patent, or copyright matches, TRO plaintiff details, and an AI-generated legal assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and compliance reviewers use this skill to screen product images and listing text for TRO and intellectual-property infringement risk before listing or reviewing products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, descriptions, IP keywords, and session metadata are sent to LinkFox services for analysis.

Mitigation: Use only images and listing data that may be shared with LinkFox; avoid confidential, unreleased, or customer-sensitive product material unless sharing is approved.

Risk: Local image upload creates a publicly reachable image URL for a limited period.

Mitigation: Review each local-image upload before running it, prefer non-sensitive images, and treat generated public URLs as shareable links.

Risk: Authentication, SMS login, billing, and payment order flows can expose credentials or create charges.

Mitigation: Require explicit user approval before collecting phone/SMS details, changing API keys, selecting a paid plan, or submitting a payment order.

Risk: The scanner verdict is suspicious because feedback reporting and persistent local records give users limited control.

Mitigation: Inform users where response files are saved, avoid unnecessary feedback submission, and review saved LinkFox data before sharing or committing workspace files.

## Reference(s):

- [卖大律 产品侵权 TRO 风险检测 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-maidalv-product-tro-detection)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results and saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns overall risk level, check ID, high-risk matches, lower-risk IP items, TRO plaintiff details when available, numeric risk scores, and an AI-generated legal report; larger responses are summarized while full JSON is saved locally.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
