## Description: <br>
通用中国专利挖掘发现与交底书生成全流程：扫描项目文档挖掘专利点、讨论融合、基于脱敏模版生成技术交底书、联网查新、生成后自检含逻辑闭环与公式参数一致性。| Patent mining, disclosure drafting, prior-art search, and consistency self-check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handsomestwei](https://clawhub.ai/user/handsomestwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, inventors, and patent-support teams use this skill to scan project materials, identify patentable ideas, perform prior-art checks, and draft Chinese patent disclosure materials with self-checks for logic, terminology, formulas, and consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan project files that may contain confidential invention material. <br>
Mitigation: Review the skill before installing and run it only against user-confirmed project paths that are appropriate for patent drafting. <br>
Risk: The skill can run local shell tooling and document conversion utilities. <br>
Mitigation: Prefer explicit invocation with user-confirmed input and output paths, and use a dedicated output directory. <br>
Risk: Processing untrusted Office files may expose the environment to document parsing dependency risk. <br>
Mitigation: Avoid untrusted DOCX/PPTX inputs and pin or upgrade dependencies such as mammoth to fixed versions. <br>
Risk: Generated patent drafts and iteration logs may persist sensitive technical details locally. <br>
Mitigation: Store outputs in a dedicated controlled directory and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/handsomestwei/patent-disclosure-skill) <br>
- [Publisher profile](https://clawhub.ai/user/handsomestwei) <br>
- [China National Intellectual Property Administration patent publication search](http://epub.cnipa.gov.cn/) <br>
- [Python](https://www.python.org/) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, generated local files, shell command snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce timestamped Markdown and DOCX patent disclosure files, Mermaid diagrams rendered to images, prior-art notes, correction summaries, and iteration logs.] <br>

## Skill Version(s): <br>
1.8.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
