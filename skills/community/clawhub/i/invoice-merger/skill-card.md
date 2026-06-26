## Description: <br>
合并发票文件。PDF 按两两上下排版，图片按四宫格排版，统一裁剪线与安全边距，输出到 YYYYMMDD--已合并 目录，重复执行会自动跳过历史合并文件并按编号继续生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdk1025](https://clawhub.ai/user/cdk1025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to merge invoice PDFs and images from a selected local folder into printable PDF layouts with cut lines and safe margins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads PDFs and images from a user-selected local folder and writes merged PDFs nearby. <br>
Mitigation: Use a dedicated folder containing only files intended for merging before running the skill. <br>
Risk: The skill may open generated PDFs in the system default viewer after creating them. <br>
Mitigation: Run it only in environments where opening local preview files is acceptable, or review this behavior before deployment. <br>
Risk: The skill depends on pypdf and Pillow at runtime. <br>
Mitigation: Install dependencies in a Python virtual environment when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cdk1025/invoice-merger) <br>
- [Publisher profile](https://clawhub.ai/user/cdk1025) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates merged PDF files in a dated local output directory and may open them in the default system viewer.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
