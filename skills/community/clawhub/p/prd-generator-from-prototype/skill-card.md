## Description: <br>
读取产品原型图/页面描述，按预设模板自动生成标准PRD文档，完成后自检一致性，不扩展需求范围 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosscui-chy](https://clawhub.ai/user/rosscui-chy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and business analysts use this skill to turn prototype text or page descriptions into scoped Chinese PRD documents, with consistency checks for missing, mismatched, and out-of-scope content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prototype descriptions may include sensitive proprietary product or business details. <br>
Mitigation: Only provide prototype content that is appropriate for the agent environment and redact confidential details when possible. <br>
Risk: A generated PRD may omit or misclassify prototype details when scope input is vague or incomplete. <br>
Mitigation: Provide explicit page, module, function, and out-of-scope boundaries, then review the consistency self-check before using the PRD. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rosscui-chy/prd-generator-from-prototype) <br>
- [template_business.md](artifact/template_business.md) <br>
- [template_analysis.md](artifact/template_analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown PRD document with a consistency self-check report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses formal Chinese, fixed PRD sections, scope boundaries, and template-specific formatting constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
