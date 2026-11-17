## Description:

深度调研一个主题，生成100页+书籍级PDF手册，使用模块化HTML片段、语义化版本管理、多Agent并行写作和Playwright渲染PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and documentation teams use this skill to plan, research, write, build, and version long-form PDF manuals, ebooks, orange papers, and reference guides from a topic brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill forces third-party branding into generated documents.

Mitigation: Review or remove default branding before generating or distributing documents.

Risk: The security evidence says the build and update scripts are local code execution tools.

Mitigation: Use the scripts only in a project directory you control, review them before execution, and avoid untrusted titles, changelog messages, or HTML fragments.

Risk: PDF rendering may process local HTML, images, fonts, JavaScript, and network-loaded resources.

Mitigation: Prefer pinned dependencies plus network and JavaScript restrictions during PDF rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiangyu2/skills/huashu-book-pdf)
- [Design system reference](artifact/references/design-system.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTML/CSS/JavaScript templates, and project files for PDF generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project scaffolds, HTML fragments, version metadata, changelog entries, merged HTML, PDF output, and archived PDF versions when the workflow is executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
