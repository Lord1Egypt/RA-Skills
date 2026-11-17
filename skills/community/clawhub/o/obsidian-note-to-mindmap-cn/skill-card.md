## Description:

将用户明确提供的 Obsidian 笔记或 Markdown 大纲默认转换为 KMind 导图 PNG，或在明确要求时输出可编辑的 KMind 导图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[suka233](https://clawhub.ai/user/suka233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and Obsidian users use this skill to turn pasted Markdown, pasted Obsidian notes, or a single explicitly named note file into a KMind mind map. It defaults to PNG output and delegates conversion to the referenced core KMind skill after explicit approval if installation is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask to install and delegate to an unpinned third-party core skill that was not included in this artifact review.

Mitigation: Install only after explicit user approval, verify the referenced publisher and registry resolution, and prefer a digest-pinned or immutable release when available.

Risk: The wrapper depends on the delegated core skill and its runtime requirements for actual mind-map generation.

Mitigation: Review the delegated core skill before use and surface any missing Node.js, browser, ClawHub CLI, or network requirements without substituting another installer or skill.

## Reference(s):

- [ClawHub skill page: obsidian-note-to-mindmap-cn](https://clawhub.ai/suka233/skills/obsidian-note-to-mindmap-cn)
- [Delegated core skill: suka233/kmind-markdown-to-mindmap](https://clawhub.ai/suka233/kmind-markdown-to-mindmap)
- [KMind Zen](https://kmind.app)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell command and generated PNG, SVG, or .kmindz.svg file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to PNG; emits editable .kmindz.svg or SVG only when explicitly requested.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
