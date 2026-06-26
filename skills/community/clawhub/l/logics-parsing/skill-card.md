## Description: <br>
阿里文档智能解析工具 - 将PDF/图片转结构化HTML。支持复杂布局、公式识别、化学结构、代码块、流程图、乐谱等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to set up and apply Alibaba Logics-Parsing to convert PDFs or document images into structured outputs, including HTML, tables, formulas, chemical structures, flowcharts, sheet music, and code blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsing PDFs or images can expose confidential document content when results are saved or moved into another knowledge base. <br>
Mitigation: Review input sensitivity before parsing and avoid sending or storing extracted content in unapproved systems. <br>
Risk: The skill points users to install and run dependencies from a referenced external repository. <br>
Mitigation: Install in an isolated Python or conda environment, review the repository and requirements before running them, and avoid elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/smseow001/logics-parsing) <br>
- [Referenced Alibaba Logics-Parsing repository](https://github.com/alibaba/Logics-Parsing.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell and Python code blocks; parsed document outputs are described as structured HTML or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external model setup and may process local PDFs or images containing confidential content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
