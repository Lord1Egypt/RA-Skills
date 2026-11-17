## Description: <br>
将纯文本或已有 Markdown 文件格式化为结构清晰、易读的 Markdown，并支持 frontmatter 生成、标题层级整理、列表优化和排版修正。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
个人作者、博客写作者和开发者可用此技能整理单个 Markdown 或纯文本文件，生成更清晰的标题、摘要、列表、frontmatter 和排版。适用于个人博客、技术笔记和已有文档的可读性提升。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the skill suspicious because it requests broad command execution and file-writing authority without tight boundaries. <br>
Mitigation: Review before installing, use it only on Markdown or text files intentionally selected by the user, and prefer writing to a new output file. <br>
Risk: Formatting requests that allow arbitrary shell commands or broad document conversion can affect unintended files. <br>
Mitigation: Inspect the exact command or script before execution and avoid broad conversion requests unless the target paths and behavior are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/markdown-format-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with example commands and JSON-style completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write formatted Markdown or analysis files when the user chooses input and output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
