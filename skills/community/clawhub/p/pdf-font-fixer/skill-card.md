## Description:

PDF 中文字体乱码与「能显示但打印不出来」的体检与修复工具。导出前检测字体风险，交付前逐字符审计并做交付门禁，也能直接修复已有 PDF 的方块字、缺字、文字消失。支持 PDF 字体检测、字体字典结构校验、字体修复、PPT 转 PDF 递进导出、缺字兜底；不内嵌任何字体，自动发现本机可用的 TrueType 中文字体。其它 skill 导出 PDF 后必须调用 gate.py 作为交付门禁。当用户提到 PDF 乱码、方块字、问号、字体缺失、打印异常、打印机报错（如佳能「未导入太大的图像或格式不受支持的文件」）、手机预览异常、PPT 导出 PDF、PDF 字体检查时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people preparing PDFs use this skill to detect Chinese font rendering or printing problems, audit PDF text, and repair affected PDFs or check slide exports before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies may be installed automatically from unpinned packages.

Mitigation: Review the dependencies and installation sources before running the skill, and control package installation in your environment.

Risk: Delivery checks may fail open or remain incomplete when a check cannot run.

Mitigation: Review the check output and confirm every required check completed before delivering a PDF.

Risk: Repairs may exceed the requested scope or remove document features such as text selection or accessibility structure.

Mitigation: Keep the original PDF, compare repaired output, and confirm the required document features before replacing or sharing it.

Risk: Security scan coverage is partial because some local references could not be resolved.

Mitigation: Review unresolved local references before installing or executing the skill.

## Reference(s):

- [Noto Sans SC specimen](https://fonts.google.com/noto/specimen/Noto+Sans+SC)
- [Noto CJK releases](https://github.com/notofonts/noto-cjk/releases)
- [WenQuanYi Zen Hei](https://wenq.org/wqy2/index.cgi?ZenHei)
- [Ghostscript downloads](https://ghostscript.com/releases/gsdnld.html)
- [LibreOffice downloads](https://www.libreoffice.org/download/)

## Skill Output:

**Output Type(s):** [Files, Analysis, Shell commands, Guidance]

**Output Format:** [PDF files with concise text reports and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide native, vector-outline, or scanned PDF variants; some repair paths can reduce copying, searching, or accessibility features.]

## Skill Version(s):

1.1.1 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
