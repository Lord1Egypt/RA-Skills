## Description:

将 Markdown 标题大纲转换为 KMind 导图，并导出 SVG 或 PNG 图片，支持主题、布局、连线、深浅色和彩虹分支配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[suka233](https://clawhub.ai/user/suka233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and Chinese-speaking users use this skill to turn Markdown heading outlines for meetings, notes, brainstorming, and project plans into local KMind mind map images or editable KMind files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a local Chromium browser and briefly runs a local 127.0.0.1 render server without render-endpoint authentication.

Mitigation: Use it only in trusted local sessions, avoid highly sensitive Markdown, and prefer environments where the browser and localhost access are controlled.

Risk: Automatic PNG or SVG export may fail when a compatible local Chromium browser is unavailable.

Mitigation: Use the documented manual browser mode or export editable .kmindz.svg when browser rendering is not available.

## Reference(s):

- [KMind Zen](https://kmind.app)
- [ClawHub skill page](https://clawhub.ai/suka233/skills/kmind-markdown-to-mindmap-cn)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Shell command guidance plus PNG, SVG, or editable .kmindz.svg files with JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatic PNG and SVG export depends on Node.js and an available local Chromium browser; editable .kmindz.svg export does not require browser rendering.]

## Skill Version(s):

0.1.1 (source: frontmatter, package.json, changelog, server release evidence; released 2026-05-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
