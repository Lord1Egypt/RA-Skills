## Description: <br>
修复PPT转PDF时的字体缺失和乱码，支持字体嵌入、替换及批量处理，适合个人用户免费使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
个人用户和文档处理人员 use this skill to inspect presentation font usage, repair missing or garbled fonts, and convert PPT files to PDF with fonts preserved. It can guide single-file workflows and limited batch processing where local document tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read presentation files and write repaired or converted outputs. <br>
Mitigation: Grant access only to explicit file paths, keep backups of important presentations, and review generated or modified files before replacing originals. <br>
Risk: PDF conversion or font repair may rely on local tools such as Python libraries or LibreOffice. <br>
Mitigation: Run commands in a trusted local environment and install dependencies from trusted package or system repositories. <br>
Risk: Callback URLs could expose processing status or document-related metadata to an untrusted destination. <br>
Mitigation: Use callback URLs only when the destination is trusted, or omit them for local-only workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pptx-pdf-font-fix-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration examples, and structured JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read PPT files, write repaired or converted outputs, and use local tools such as Python libraries or LibreOffice when the agent is granted those capabilities.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
