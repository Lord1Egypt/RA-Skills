## Description: <br>
面向产品经理和产品协作者的产品需求评审沙盘工作流，帮助澄清模糊需求、共创产品需求文档、准备评审材料、模拟多角色质询并收敛一期范围。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whisperbot](https://clawhub.ai/user/whisperbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product collaborators use this skill to clarify product requirements, define problems, draft review-ready PRD materials, rehearse cross-functional review questions, and identify scope, metric, dependency, and risk gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated requirement or review materials may expose confidential product plans if written to an unintended path or shared into the wrong collaboration document. <br>
Mitigation: Confirm input paths, output paths, and the target Feishu account or document before generating PDFs or Feishu content. <br>
Risk: Incomplete product context can lead to speculative requirements, metrics, business rules, or system assumptions. <br>
Mitigation: Keep unknowns marked as known information, reasonable assumptions, and questions to confirm before using the materials for decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whisperbot/pm-requirement-review-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Chinese Markdown, PDF-ready documents, Feishu-ready Markdown, and local PDF files when the renderer is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to PDF for document-generation requests; may also produce Markdown source and Feishu-ready content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
