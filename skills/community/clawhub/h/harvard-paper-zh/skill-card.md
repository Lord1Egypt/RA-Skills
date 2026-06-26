## Description: <br>
将中文需求或素材稿整理为中文学术论文，采用 Harvard 参考文献风格并导出 .docx。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and writers use this skill to turn Chinese source notes, informal requirements, or draft material into a structured academic paper with an abstract, keywords, sections, Harvard-style references, and a Word document output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The document generation script reads a selected source file and writes to a chosen output path. <br>
Mitigation: Use only source files intended for conversion, choose the output path deliberately, and review the generated Word file before sharing or submission. <br>
Risk: Generated academic prose and references may not satisfy a specific school, course, or journal requirement. <br>
Mitigation: Verify citations and formatting against the applicable template or submission rules, which should override the skill defaults. <br>
Risk: The script depends on the local Pandoc executable. <br>
Mitigation: Install Pandoc from a trusted source if it is not already available. <br>


## Reference(s): <br>
- [Harvard 引用速查](references/harvard-quick-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Chinese academic prose, Markdown paper structure, shell command examples, and a generated .docx file through Pandoc.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a selected txt/md source path, an output docx path, and a trusted local Pandoc installation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
