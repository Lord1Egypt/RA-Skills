## Description: <br>
Helps agents design and verify high-fidelity web, mobile, mini-program, and component UI prototypes using aesthetic genres, design tokens, accessibility checks, and platform-specific starter examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and product teams use this skill to generate polished frontend prototypes, design-system tokens, mobile-native layouts, mini-program starters, and accessibility verification guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation on frontend and design requests may affect sensitive projects. <br>
Mitigation: Review the skill before use in sensitive workspaces and confirm the requested UI generation or verification scope. <br>
Risk: Optional browser and accessibility audits may load external audit tooling such as axe-core from a CDN. <br>
Mitigation: Use the audit route only when CDN loading is acceptable, or run an approved local accessibility scanner instead. <br>
Risk: Multi-genre comparison workflows may produce temporary design drafts that are later deleted. <br>
Mitigation: Confirm which draft should be retained before removing generated comparison files. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/zhaobod1/huo15-openclaw-frontend-design) <br>
- [Self-verification workflow](references/self-verify.md) <br>
- [Accessibility checklist](references/a11y-checklist.md) <br>
- [Design token schema](tokens/_schema.md) <br>
- [Multi-genre comparison guide](references/multi-genre-compare.md) <br>
- [Mini-program starter guide](examples/mini-program/README.md) <br>
- [WeChat developer tools](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) <br>
- [Alipay mini program IDE](https://opendocs.alipay.com/mini/ide/download) <br>
- [Douyin mini app developer tools](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/developer-instrument/installation/developer-instrument-update-and-download) <br>
- [Kuaishou mini program developer tools](https://mp.kuaishou.com/docs/develop/developerTools/downloadPath.html) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with frontend source code, JSON design tokens, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable HTML/CSS/JavaScript, React or Vue components, mini-program starter files, design-token exports, screenshots, and accessibility audit instructions.] <br>

## Skill Version(s): <br>
4.7.0 (source: SKILL.md frontmatter and evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
