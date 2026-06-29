## Description: <br>
ISO20000辅助认证助手 (ISO20000 Certification Assistant) helps organizations prepare for ISO 20000-1:2018 IT Service Management System certification with document gap analysis, compliance checking, and bilingual document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External consultants, IT service organizations, and certification teams use this skill to parse ISO 20000-1:2018 ITSM documents, identify gaps, check high-priority compliance practices, and draft bilingual remediation documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client ISO/ITSM documents may contain confidential business data, personal data, or other sensitive content that the skill parses into analysis artifacts and generated drafts. <br>
Mitigation: Use only necessary source documents, remove secrets or unrelated personal data before analysis, and review generated outputs before sharing. <br>
Risk: Legacy .doc conversion has higher document-parsing risk when a local converter is used. <br>
Mitigation: Prefer .docx or .txt inputs for sensitive work; if .doc conversion is required, run a patched converter in a sandboxed local environment. <br>
Risk: Generated ISO 20000 compliance materials are drafts and may not fully satisfy an auditor or the organization's real operating context. <br>
Mitigation: Have qualified ISO/ITSM reviewers validate recommendations and generated procedures before certification use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/iso20000-certificate-assistant) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Example interactions](artifact/examples/example_interaction.md) <br>
- [ISO 20000-1:2018 framework data](artifact/knowledge/iso20000_framework.json) <br>
- [Generic ISO 20000 templates](artifact/knowledge/generic_templates.json) <br>
- [Bilingual ISO 20000 templates](artifact/knowledge/bilingual_templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON analysis results, and local document or text files produced through Python script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON, text output files, converted .doc text, and parser or analyzer log files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact notes internal Version 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
