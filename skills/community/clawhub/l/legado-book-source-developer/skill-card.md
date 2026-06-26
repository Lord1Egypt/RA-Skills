## Description: <br>
Helps developers create, debug, validate, and manage Legado book source JSON by analyzing authorized website HTML, encoding, selectors, and Legado rules for search, book info, tables of contents, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuluoxci](https://clawhub.ai/user/yuluoxci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, debug, validate, and manage Legado book source JSON for websites they own or are authorized to test. It helps analyze real HTML, encoding, selectors, search rules, table-of-contents rules, content extraction rules, and related Legado source fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide scraping-oriented network requests and local HTML snapshot storage. <br>
Mitigation: Use it only on websites the user owns or is authorized to test, and review generated requests before execution. <br>
Risk: The skill includes material related to cookie/session handling and anti-bot bypass. <br>
Mitigation: Do not provide passwords, MFA codes, live cookies, or Authorization headers, and avoid anti-bot bypass workflows. <br>
Risk: The skill includes upload tooling that can send book source content to an external destination. <br>
Mitigation: Review the upload destination and payload before running upload tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuluoxci/legado-book-source-developer) <br>
- [Legado development guide](artifact/references/legado_development_guide.md) <br>
- [Legado data structures](artifact/references/legado_data_structures.md) <br>
- [Comprehensive Legado book source guide](artifact/references/Legado书源开发完整指南.md) <br>
- [Encoding handling guide](artifact/references/Legado书源编码处理指南.md) <br>
- [Tool usage guide](artifact/references/工具使用说明.md) <br>
- [No Python workflow](artifact/references/no_python_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce complete Legado book source JSON arrays and validation or upload commands for user-approved targets.] <br>

## Skill Version(s): <br>
2.3.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
