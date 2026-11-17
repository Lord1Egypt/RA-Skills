## Description: <br>
Nano PDF工具（免费版） helps agents read, create, edit, and extract text from PDFs for everyday personal document tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect PDF contents, create simple PDFs, extract text, and perform basic page operations such as rotation for personal document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to read and write PDFs in the workspace and run Python PDF tooling, which can overwrite documents or process unintended files if paths are vague. <br>
Mitigation: Use exact input and output paths, keep originals separate from generated files, review PDF changes before relying on them, and use callback URLs only for trusted endpoints. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Python PDF tooling and file path inputs for read, write, extraction, and page operation tasks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
