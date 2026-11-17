## Description:

小程序选题共创（小程序选题与共创落地）。当用户说做小程序、收集选题、有点子想推到可落地SOP、问小程序开发方向或选题规则，或给小程序点子想梳理可执行方案时触发。不适用于已有小程序的代码编写、调试，或纯小程序技术问答。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninebirds01-crypto](https://clawhub.ai/user/ninebirds01-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn early WeChat mini-program ideas into a searched, filtered, and actionable product specification. It guides topic expansion, feasibility screening, compliance-aware judgment, and SOP-style planning without writing or debugging mini-program code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires web-search-driven brainstorming, which can expose confidential product ideas or business context if users include sensitive details.

Mitigation: Avoid entering confidential business details during brainstorming; sanitize examples before search-based topic expansion.

Risk: The included example specifications may involve location, photos, AI processing, or _openid-linked cloud records if implemented as real mini-programs.

Mitigation: Add clear privacy notices, retention limits, delete/export controls, and explicit consent for location, photos, AI processing, and linked cloud records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninebirds01-crypto/skills/miniprogram-topic-cocreation)
- [case-ask-social-trade.md](references/case-ask-social-trade.md)
- [case-item-locator.md](references/case-item-locator.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown tables and structured prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language planning output; may include product specification sections, compliance checkpoints, and implementation task breakdowns.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
