## Description: <br>
Markdown 转 Word/PDF/HTML 文档转换器。支持 6 种样式模板（商务蓝、技术灰、简洁白、产品红、学术风、默认），自动生成封面、目录、页眉页脚。当用户需要将 Markdown 转成 Word、PDF 或 HTML，生成带样式的文档，或提到文档导出、格式转换时，使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glory904649854](https://clawhub.ai/user/glory904649854) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to convert Markdown files into styled Word, PDF, or HTML documents with optional covers, tables of contents, headers, footers, images, tables, and code block styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown documents can reference remote images, which may trigger network requests from the user's environment during conversion. <br>
Mitigation: Review or remove remote image URLs before converting third-party Markdown, and run the converter in a virtual environment or sandbox when appropriate. <br>
Risk: Generated HTML from untrusted Markdown may contain content that should not be treated as trusted when opened in a browser. <br>
Mitigation: Treat generated HTML from untrusted Markdown as untrusted output and review it before sharing or opening in a privileged context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glory904649854/md2doc) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX, PDF, and HTML files plus concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF export requires Microsoft Word or LibreOffice; image handling can fetch remote image URLs referenced by the input Markdown.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
