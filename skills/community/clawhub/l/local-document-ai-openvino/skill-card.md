## Description: <br>
Private document AI for Intel hardware that parses PDFs, invoices, screenshots, and diagrams locally with MinerU 2.5 on OpenVINO GenAI, then turns them into structured data or executable notebook and code scaffolds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuo-yoyowz](https://clawhub.ai/user/zhuo-yoyowz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to process private local documents into structured extraction artifacts, reports, and draft implementation assets. It is suited for invoice and receipt extraction, document classification, table and key-value extraction, and screenshot or diagram conversion into code or notebook scaffolds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes full parsed document artifacts to disk, which can expose sensitive document contents if output folders are shared or retained longer than needed. <br>
Mitigation: Use private local output directories for confidential documents and delete generated artifacts after review. <br>
Risk: Generated Jupyter notebooks or code scaffolds may include runnable remote-model code or unsafe assumptions. <br>
Mitigation: Inspect generated code and notebook cells before execution, especially model download steps and any trust_remote_code=True usage. <br>
Risk: The security verdict is suspicious because notebook output can create runnable remote-model code with insufficient warning. <br>
Mitigation: Review dependencies and generated execution paths before production use, and pin or audit dependencies for managed deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuo-yoyowz/skills/local-document-ai-openvino) <br>
- [MinerU OpenVINO model bundle](https://www.modelscope.cn/models/snake7gun/MinerU2.5-Pro-2604-1.2B-int4-ov) <br>
- [Mode guide](references/mode_guide.md) <br>
- [Output contracts](references/output_contracts.md) <br>
- [Structured parse schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus local files such as JSON, Markdown, HTML reports, code scaffolds, and Jupyter notebooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes parse and downstream artifacts to a local output folder with traceability files when downstream modes are used.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
