## Description: <br>
Generates API and technical documentation from source code, including comment extraction, Chinese documentation templates, OpenAPI 3.0 output, and optional Feishu document workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penghang1223](https://clawhub.ai/user/penghang1223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect selected Python, JavaScript/TypeScript, or Go source files and generate API documentation, technical documentation, OpenAPI specs, or Feishu-ready Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation may expose secrets, credentials, or internal-only implementation details found in selected source files. <br>
Mitigation: Specify narrow source paths and review generated documentation before saving, sharing, or exporting it. <br>
Risk: Feishu export workflows may send generated documentation content to a Feishu workspace. <br>
Mitigation: Use Feishu publication only for content that is approved for that workspace. <br>
Risk: Extracted API details may be incomplete or inaccurate when comments, type hints, or route patterns are missing or non-standard. <br>
Mitigation: Review generated Markdown, JSON, or OpenAPI YAML against the source code before relying on it as authoritative documentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/penghang1223/oc-doc-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/penghang1223) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, OpenAPI YAML, and Lark-flavored Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated documentation to a requested output file; Feishu publication is described as a follow-on workflow using a separate Feishu document tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
