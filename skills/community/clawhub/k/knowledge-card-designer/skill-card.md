## Description:

生成小绿书风格知识卡片的专家技能。当用户需要创建读书笔记、知识总结、概念解释、书籍分享等视觉内容时触发。支持设计规范应用、色彩心理学、CRAP原则排版。适用于微信读书小绿书、小红书、知识分享等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and agents use this skill to design Chinese Xiaolvshu/WeChat-style knowledge cards for reading notes, summaries, concept explanations, and book-sharing content. It guides content analysis, template selection, visual design, and local export of HTML previews, text drafts, and image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include unescaped topic or card text.

Mitigation: Do not use secrets or untrusted HTML/JavaScript in topic or card text, and review generated HTML before rendering or sharing outputs.

Risk: Local rendering depends on Chrome or Playwright and writes files under the OpenClaw workspace.

Mitigation: Run the scripts in a controlled workspace with expected browser dependencies installed, and review generated HTML, TXT, and PNG outputs before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentforge-cyber/skills/knowledge-card-designer)
- [Design Principles](artifact/references/design-principles.md)
- [Color Psychology](artifact/references/color-psychology.md)
- [Content System](artifact/references/content-system.md)
- [Visual System](artifact/references/visual-system.md)
- [Viral Content Research Notes](artifact/references/爆款研究笔记.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with optional local HTML, TXT, PNG, and PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates fixed-size card assets such as 900x383 cover images and 1080x1350 content cards; PNG export depends on local Chrome or Playwright.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
