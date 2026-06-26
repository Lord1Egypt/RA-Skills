## Description: <br>
Markdown 与 HTML 互转，并支持 Markdown 转 PDF。当用户说：把这篇 MD 转成 HTML、导出 PDF，或类似文档格式转换时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert intentionally supplied Markdown or HTML content into editable Markdown, standalone HTML, or PDF output for reports and document handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Markdown, text, or HTML files selected by path. <br>
Mitigation: Use it only on files or content you intentionally provide, and keep path inputs scoped to the current project. <br>
Risk: Generated HTML or PDFs may carry unsafe or misleading content from the source document. <br>
Mitigation: Review generated HTML before opening it in sensitive contexts and validate converted reports before sharing or relying on them. <br>
Risk: The skill text mentions JisuAPI AppKey usage as an optional external workflow. <br>
Mitigation: Ignore the JisuAPI/AppKey material unless you separately choose to use that external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/md2html) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON responses containing HTML, Markdown, PDF base64, or structured error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and optional Python packages markdown, xhtml2pdf, and html2text.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
