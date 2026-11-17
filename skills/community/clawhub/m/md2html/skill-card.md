## Description:

Markdown 与 HTML 互转，并支持 Markdown 转 PDF。当用户说：把这篇 MD 转成 HTML、导出 PDF，或类似文档格式转换时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Markdown into standalone HTML or base64-encoded PDF output, and to convert HTML files or snippets back into editable Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted document inputs or paths could read unintended local files or produce active generated content.

Mitigation: Use only trusted documents and paths, avoid attacker-supplied project folders, symlinks, Markdown, HTML, or titles, and render generated HTML/PDF in an isolated viewer.

Risk: The conversion flow depends on path handling, title handling, HTML rendering, and Python package behavior.

Mitigation: Prefer a hardened release that resolves real paths under the project root, rejects symlinks, escapes titles, sanitizes HTML, and pins dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/md2html)
- [Publisher profile](https://clawhub.ai/user/jisuapi)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [JSON responses containing HTML, Markdown, or base64-encoded PDF content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and optional Python packages markdown, xhtml2pdf, and html2text for conversion commands.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
