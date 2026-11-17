## Description:

Generates high-fidelity frontend design guidance and prototype assets for web pages, mobile H5 or app interfaces, mini-programs, design systems, accessibility checks, motion tokens, and multi-style visual comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and product teams use this skill to turn frontend UI requests into visually opinionated prototypes, platform-specific mobile or mini-program starters, design-token guidance, and accessibility verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification guidance can lead users to run mutable third-party browser or shell tooling.

Mitigation: Review verification steps before use and run audits against local prototypes or a dedicated browser profile without production logins.

Risk: Examples reference CDN-hosted axe-core and unpinned npx tooling.

Mitigation: Replace CDN and unpinned examples with pinned or lockfile-managed local tooling before using them in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-frontend-design)
- [Accessibility and WCAG 2.2 AA checklist](references/a11y-checklist.md)
- [Self-verification workflow](references/self-verify.md)
- [Multi-style comparison workflow](references/multi-genre-compare.md)
- [Design token schema](tokens/_schema.md)
- [Design token comparison matrix](tokens/_compare-matrix.md)
- [CSS variables exporter](tokens/exporters/to-css-vars.md)
- [Tailwind exporter](tokens/exporters/to-tailwind.md)
- [Figma exporter](tokens/exporters/to-figma.md)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design 3](https://m3.material.io/)
- [HarmonyOS Design Guidelines](https://developer.huawei.com/consumer/cn/design/)
- [WeChat Mini Program Design Guidelines](https://developers.weixin.qq.com/miniprogram/design/)
- [Alipay Mini Program Design Guidelines](https://opendocs.alipay.com/mini/design)
- [Douyin Mini App Developer Documentation](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/component/)
- [Kuaishou Mini Program Developer Documentation](https://mp.kuaishou.com/docs/develop/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, JSON design tokens, and prototype source files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific starter files, design token exports, accessibility audit steps, and short design rationale.]

## Skill Version(s):

4.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
