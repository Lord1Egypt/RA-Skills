## Description: <br>
将 Markdown 标题大纲转换为 KMind 导图，并导出 SVG 或 PNG 图片。支持主题、布局、连线、深浅色和彩虹分支配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suka233](https://clawhub.ai/user/suka233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and agents use this skill to turn Markdown heading outlines, notes, meeting agendas, reading notes, brainstorming lists, and project plans into KMind mind maps. It can generate PNG or SVG images and editable .kmindz.svg project files for continued editing in KMind Zen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local renderer reads user-provided Markdown or KMind content and writes output files where requested. <br>
Mitigation: Use trusted input paths and avoid sensitive notes when local file processing is not acceptable. <br>
Risk: PNG and SVG image export can open a temporary localhost render session in a Chromium-family browser. <br>
Mitigation: Use the skill only when this local browser workflow is acceptable; otherwise use editable .kmindz.svg export or manual review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suka233/kmind-markdown-to-mindmap-cn) <br>
- [KMind Zen](https://kmind.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated files are PNG, SVG, or .kmindz.svg.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Automatic PNG or SVG export requires an available local Chromium-family browser; editable .kmindz.svg export does not require browser rendering.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter, package.json, CHANGELOG, released 2026-05-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
